# ListLongNew (lln)

List all new files in a directory tree.

Writen in Python 3.

### Installation
Download the lln.py file and put it in a executable folder. Tested on Ubuntu but should work on all platforms.

### Usage
```
$ lln --help
usage: lln [-h] [-d DAYS_BACK] [-a] [-v] [-l] [-f]
           [-s {filename,created,size,user,group}]
           [dir]

List Long New (lln) - List new files in directory tree

positional arguments:
  dir                   file path, leave empty for current working directory

optional arguments:
  -h, --help            show this help message and exit
  -d DAYS_BACK, --days-back DAYS_BACK
                        files from the last N days
  -a, --all             do not ignore entries starting with .
  -v, --debug           show errors and warnings
  -l, --show-symbolic   show symbolic links
  -f, --no-recursion    do not list subdirectories recursively
  -s {filename,created,size,user,group}, --sort-by {filename,created,size,user,group}
                        specify filelist sort
```

### Example Output
```bash
~/code/ListLongNew$ lln
Files from last 3 days
-rw-rw-r-- lennart lennart 2016-03-20 10:18     35K /home/user/code/ListLongNew/LICENSE
-rw-rw-r-- lennart lennart 2016-03-20 23:33      1K /home/user/code/ListLongNew/README.md
-rwxrwxr-x lennart lennart 2016-03-20 23:34      5K /home/user/code/ListLongNew/lln.py
```

Same effect could also be archieved with this single line command, but that does not show the output so nicely:
$ find ${1} -type f | xargs stat --format '%Y :%y %n' 2>/dev/null | sort -nr | cut -d: -f2- | head -5