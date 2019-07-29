import os
import socket
import logging
import datetime
import dns.resolver
import git

CUR_DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
PARENT_DIR_PATH = os.path.join(CUR_DIR_PATH, os.pardir)
IP_FILE_PATH = os.path.join(PARENT_DIR_PATH, "IP")

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# Fetch public IP
ip = None
try:
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers=[socket.gethostbyname('resolver1.opendns.com')]
    ip = str(resolver.query('myip.opendns.com')[0])
except Exception as e:
    logging.exception(e)
    logging.fatal("Couldn't resolve IP address")
    raise e

# Write public IP to file
try:
    if not os.path.exists(IP_FILE_PATH):
        os.mknod(IP_FILE_PATH)
    with open(IP_FILE_PATH, "r+") as f:
        if f.read() != ip:
            f.seek(0)
            f.write(ip)
            f.truncate()
            logging.info("Writing new IP to file: %s" % ip)
        else:
            exit(0)
except Exception as e:
    logging.exception(e)
    logging.fatal("Couldn't write ip to file")
    raise e

# Commit new IP file and push to server
try:
    rep = git.Repo(PARENT_DIR_PATH)
    rep.index.add([IP_FILE_PATH])
    origin = rep.remote()
    origin.pull()
    rep.index.commit("New IP as of %s" % str(datetime.datetime.now()))
    origin.push()
except Exception as e:
    logging.exception(e)
    logging.fatal("Couldn't commit to git")
    raise e

