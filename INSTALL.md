Installation Guide
==================
There are two installation guides, development and production.
Both guides were tested on Ubuntu Server 18.04.


Development
===========
1.  Install system dependencies:
    `sudo apt install python3 python3-dev python3-venv git build-essential`
2.  Install latest LTS version of NodeJS:
    1.  Download and extract archive
        * `cd ~`
        * `wget https://nodejs.org/dist/v10.15.3/node-v10.15.3-linux-x64.tar.xz`
        * `tar -xJf node-v10.15.3-linux-x64.tar.xz`
        * `mv node-v10.15.3-linux-x64 node`
    2.  Create and apply symlinks to Node commands
        * `mkdir ~/bin`
        * `cd bin`
        * `ln -s ~/node/bin/node`
        * `ln -s ~/node/bin/npm`
    3.  Apply profile config and check Node and NPM versions
        * `cd ~`
        * `source .profile`
        * `node -v`
        * `npm -v`
4.  Create Python virtual environment and install project requirements:
    * `cd ~/hexchan-engine`
    * `python3 -m venv python_modules`
    * `source python_modules/bin/activate`
    * `pip install --upgrade pip`
    * `pip install -r requirements.txt`
5.  Install project's NodeJS dependencies:
    * `cd ~/hexchan-engine`
    * `npm install`
6.  Create development storage directories:
    * `cd ~/hexchan-engine/generators`
    * `python dirmaker.py`
7.  Create SQLite database and apply migrations:
    * `cd ~/hexchan-engine/src`
    * `./manage.py migrate`
8.  Create superuser
    * `cd ~/hexchan-engine/src`
    * `./manage.py createsuperuser`
9.  Generate a pool of 100 CAPTCHAs:
    * `cd ~/hexchan-engine/src`
    * `./manage.py makecaptchas 100`
10. Build frontend:
    * `cd ~/hexchan-engine`
    * `./build_frontend.sh`
11. This step is optional, take it if you want to prepopulate your installation with some fake content:
    1.  `cd ~/hexchan-engine/generators`
    2.  You'll need a directory with some images. 
        If you don't have one, you can install `ubuntu-wallpapers` system package.
        This script will collect images' data into JSON file and generate thumbnails for them.
        Image data will be used later to generate fake threads and posts.
        * `python imagemaker.py /usr/share/backrounds`
    3.  Generate fake posts with random Latin text and images. It can take a while.
        * `python partymaker.py`
    4.  
        * `cd ~/hexchan-engine/src`
        * `./manage.py loaddata boards threads posts images`
12. Run dev server:
    * `cd ~/hexchan-engine/src`
    * `./manage.py runserver`
    Open https://localhost:8000 in your browser. 
    You can login as superuser at https://localhost:8000/admin


Production
==========
TODO
