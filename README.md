# Installation

```bash
git clone https://github.com/swasun/copyright-updater
cd copyright-updater
sudo python3 setup.py install

copyright-updater --help
usage: copyright-updater [-h] [-f PATH] [-d PATH] [-l LIST [LIST ...]]
                         [-a [APACHE2|GPL3|MIT] PROJECT AUTHOR DATE]
                         [-r CURRENT_PATH NEW_PATH] [-u [AUTHOR|DATE|PROJECT]
                         CURRENT NEW] [-e] [--backup] [--surround] [--force]

optional arguments:
  -h, --help            show this help message and exit
  -f PATH, --file PATH
  -d PATH, --dir PATH
  -l LIST [LIST ...], --list LIST [LIST ...]
  -a [APACHE2|GPL3|MIT] PROJECT AUTHOR DATE, --add [APACHE2|GPL3|MIT] PROJECT AUTHOR DATE
  -r CURRENT_PATH NEW_PATH, --replace CURRENT_PATH NEW_PATH
  -u [AUTHOR|DATE|PROJECT] CURRENT NEW, --update [AUTHOR|DATE|PROJECT] CURRENT NEW
  -e, --erase
  --backup
  --surround
  --force
```
