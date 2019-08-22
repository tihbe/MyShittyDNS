MyShittyDns
===========

A terrible yet conveniently easy way of tracking the dynamic public IP of my home server.

# Installation
1. Create a repository somewhere private and clone locally
    1. The remote name must be `origin` (default value).
2. Add this repository as submodule
    1. `git submodule add git@github.com:tihbe/MyShittyDNS.git`
3. Install python dependencies `pip3 install -r ./MyShittyDNS/requirements.txt`
3. Execute the script `python3 ./MyShittyDNS/fetchip.py`
4. You should have your public IP address in your private git repository.
5. Cronjob the python script
    1. `echo "*/5 * * * * $USER $(which python) $(pwd)/MyShittyDNS/fetchip.py >> $(pwd)/cron.log 2>&1" | sudo tee /etc/cron.d/myshittydns`
