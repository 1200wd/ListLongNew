#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    ProgrammingPython List Long New Files
#    Copyright (C) 2016 March
#    1200 Web Development
#    http://1200wd.com/
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import stat
import time
from pwd import getpwuid
from grp import getgrgid
import argparse


class ListLongNew:
    def __init__(self, recursive=True, show_hidden=False, days_back=3, sort_by='filename', skip_symbolic=True, debug=False):
        self.recursive = recursive
        self.show_hidden = show_hidden
        self.days_back = days_back
        self.sort_by = sort_by
        self.skip_symbolic = skip_symbolic
        self.debug = debug
        self.filelist = []
        self._max_user_size = 0
        self._max_grp_size = 0
        self._max_size_size = 0
        self._recursion_level = 0

    def _parse_file(self, path):
        try:
            filestat = os.stat(path)
            if filestat.st_mtime < (time.time()-(self.days_back*24*60*60)):
                return
            created = time.strftime("%Y-%m-%d %H:%M", time.localtime(filestat.st_mtime))

            user = getpwuid(filestat.st_uid).pw_name
            group = getgrgid(filestat.st_gid)[0]
            if len(user)>self._max_user_size: self._max_user_size=len(user)
            if len(group)>self._max_grp_size: self._max_grp_size=len(group)

            filemode = stat.filemode(filestat.st_mode)
            sizemb = int(filestat.st_size/1000)

            if sizemb: size = str(sizemb).rjust(6) + 'K'
            else: size = '    <1K'
            if len(size)>self._max_size_size: self._max_size_size=len(size)

            return {'filename': path, 'filemode': filemode, 'created': created, 'user': user, 'group': group, 'size': size}
        except FileNotFoundError:
            return
        except Exception as e:
            if self.debug:
                print("Error: %s" % e.args)

    def parse_path(self, path):
        filename = os.path.split(path)[1]
        if filename and not self.show_hidden and os.path.basename(filename)[0] == '.':
            return
        if self.skip_symbolic and os.path.islink(path):
            return

        if os.path.isdir(path):
            if not self.recursive and self._recursion_level:
                return
            self._recursion_level += 1
            try:
                files = os.listdir(path)
                for file in files:
                    if path[-1:] != "/": path += "/"
                    self.parse_path(path + file)
            except PermissionError:
                if self.debug:
                    print("Permission error on path %s" % path)
        else:
            r = self._parse_file(path)
            if r:
                self.filelist.append(r)

    def show(self):
        filelist = sorted(self.filelist , key=lambda elem: "%s%s" % (elem['filemode'][0].replace('-',chr(255)), elem[self.sort_by]))

        print("Files from last %s days" % self.days_back)
        if not filelist: print("None found...")
        for file in filelist:
            print("%-10s %s %s %-16s %s %s" % (
                file['filemode'],
                file['user'].ljust(self._max_user_size),
                file['group'].ljust(self._max_grp_size),
                file['created'],
                file['size'].rjust(self._max_size_size),
                file['filename']))


def parse_args():
    parser = argparse.ArgumentParser(description='List Long New (lln) - List new files in directory tree')
    parser.add_argument('dir', help='file path, leave empty for current working directory', nargs='?', default=os.getcwd())
    parser.add_argument('-d', '--days-back', help='files from the last N days', type=int, default=3)
    parser.add_argument('-a', '--all', help='do not ignore entries starting with .', action='store_true')
    parser.add_argument('-v', '--debug', help='show errors and warnings', action='store_true')
    parser.add_argument('-l', '--show-symbolic', help='show symbolic links', action='store_false')
    parser.add_argument('-f', '--no-recursion', help='do not list subdirectories recursively', action='store_false')
    parser.add_argument('-s', '--sort-by', help='specify filelist sort', choices=['filename','created','size','user','group'], default='filename')
    return parser.parse_args()



if __name__ == '__main__':
    args = parse_args()
    lln = ListLongNew(days_back=args.days_back, show_hidden=args.all, debug=args.debug,
                      skip_symbolic=args.show_symbolic, recursive=args.no_recursion,
                      sort_by=args.sort_by)
    lln.parse_path(args.dir)
    lln.show()
