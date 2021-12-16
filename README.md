# Webseite des AN
[![Deploy](https://github.com/asozialesnetzwerk/an-website/actions/workflows/deploy.yml/badge.svg)](https://github.com/asozialesnetzwerk/an-website/actions/workflows/deploy.yml)
[![Check code](https://github.com/asozialesnetzwerk/an-website/actions/workflows/check.yml/badge.svg)](https://github.com/asozialesnetzwerk/an-website/actions/workflows/check.yml)
[![Check emoji](https://github.com/asozialesnetzwerk/an-website/actions/workflows/emoji-in-commit.yml/badge.svg)](https://github.com/asozialesnetzwerk/an-website/actions/workflows/emoji-in-commit.yml)
[![Code coverage](https://asozialesnetzwerk.github.io/an-website/coverage/badge.svg)](https://asozialesnetzwerk.github.io/an-website/coverage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## How to develop
You need:
- python3.10
- packages from requirements.txt (`pip install -r requirements.txt`)
- packages from requirements-dev.txt (`pip install -r requirements-dev.txt`)

### How to check
- `./check.sh`

### How to format
- `python -m black an_website tests`

### How to run
- `python -X dev -m an_website` (-X dev is for debugging)


## How to run (production)
### Linux (tested with arch):
You need:
- python3.10
- packages from requirements.txt
- supervisord
- redis (+ redis-cell) for ratelimits
- uwufetch

How
- clone this repo in the home directory of a user
- (if necessary) add the following at the end of /etc/supervisord.conf
```
  [include]
  files = /etc/supervisor.d/*.ini
```
- (if necessary) create /etc/supervisor.d/
- run restart.sh as the user of the home directory

### Windows
Why?

### FreeBSD
should work similar to linux
`/etc/supervisord.conf`   -> `/usr/local/etc/supervisord.conf`
`/etc/supervisor.d/*.ini` -> `/usr/local/etc/supervisor.d/*.ini`
`/etc/supervisor.d/`      -> `/usr/local/etc/supervisor.d/`
restart.sh: `/etc/supervisor.d/$SERVICE_FILE_NAME` -> `/usr/local/etc/supervisor.d/$SERVICE_FILE_NAME`

### MacOS
Why? (same as FreeBSD, probably)
