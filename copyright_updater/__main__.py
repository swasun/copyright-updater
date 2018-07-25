 #####################################################################################
 # MIT License                                                                       #
 #                                                                                   #
 # Copyright (C) 2018 Charly Lamothe                                                 #
 #                                                                                   #
 # This file is part of copyright-updater.                                           #
 #                                                                                   #
 #   Permission is hereby granted, free of charge, to any person obtaining a copy    #
 #   of this software and associated documentation files (the "Software"), to deal   #
 #   in the Software without restriction, including without limitation the rights    #
 #   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       #
 #   copies of the Software, and to permit persons to whom the Software is           #
 #   furnished to do so, subject to the following conditions:                        #
 #                                                                                   #
 #   The above copyright notice and this permission notice shall be included in all  #
 #   copies or substantial portions of the Software.                                 #
 #                                                                                   #
 #   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      #
 #   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        #
 #   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     #
 #   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          #
 #   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   #
 #   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   #
 #   SOFTWARE.                                                                       #
 #####################################################################################

from .utils import chunkify, list_target_files, read_lines
from .console_logger import ConsoleLogger
from .update import update_copyright_date, update_copyright_author, update_copyright_project_name
from .comment import comment_copyright
from .uncomment import uncomment_copyright
from .find import find_copyright
from .add import add_copyright
from .replace import replace_copyright
from .erase import erase_copyright

import sys
import os
import argparse
from concurrent import futures
import pkg_resources

JOBS_NUMBER = 5

def job_add(copyright_lines, chunk, with_backup=False, with_surround=False, force=False):
    for target_file_name in chunk:
        add_copyright(target_file_name, copyright_lines, with_backup, with_surround, force)

def job_replace(current_copyright_content, new_copyright_content, chunk, with_backup=False):
    for target_file_name in chunk:
        replace_copyright(target_file_name, current_copyright_content, new_copyright_content, with_backup)

def job_update(category, chunk, current, new, with_backup=False):
    for target_file_name in chunk:        
        with open(target_file_name, 'r') as f:
            file_lines = f.readlines()
        
        try:
            copyright = find_copyright(file_lines)
        except:
            ConsoleLogger.error("Failed to find copyright in file '" + target_file_name + "'")
            continue

        uncommented_copyright = uncomment_copyright(copyright)

        if category == 'AUTHOR':
            if not update_copyright_author(uncommented_copyright, current, new):
                ConsoleLogger.error("Failed to update copyright author")
        elif category == 'DATE':
            if not update_copyright_date(uncommented_copyright, current, new):
                ConsoleLogger.error("Failed to update copyright date")
        elif category == 'PROJECT':
            if not update_copyright_project_name(uncommented_copyright, current, new):
                ConsoleLogger.error("Failed to update copyright project name")

        new_copyright = comment_copyright(uncommented_copyright)

        replace_copyright(target_file_name, ''.join(copyright.lines), ''.join(new_copyright.lines), with_backup)

def job_erase(chunk, with_backup=False):
    for target_file_name in chunk:
        erase_copyright(target_file_name, with_backup)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', nargs=1, metavar=('PATH'))
    parser.add_argument('-d', '--dir', nargs=1, metavar=('PATH'))
    parser.add_argument('-a', '--add', nargs=4, metavar=('[APACHE2|GPL3|MIT]', 'PROJECT', 'AUTHOR', 'DATE'))
    parser.add_argument('-r', '--replace', nargs=2, metavar=('CURRENT_PATH', 'NEW_PATH'))
    parser.add_argument('-u', '--update', nargs=3, metavar=('[AUTHOR|DATE|PROJECT]', 'CURRENT', 'NEW'))
    parser.add_argument('-e', '--erase', action='store_true')
    parser.add_argument('-b', '--backup', action='store_true')
    parser.add_argument('-s', '--surround', action='store_true')
    parser.add_argument('--force', action='store_true')
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.error('One of --file or --dir must be given')

    mode_count = sum([1 if arg else 0 for arg in (args.add, args.replace, args.update, args.erase)])
    if mode_count == 0:
        parser.error('One of --add or --replace or --update or --erase must be given')
    elif mode_count > 1:
        parser.error('Only one of --add or --replace or --update or --erase must be given')

    if args.update and args.update[0] not in ('AUTHOR', 'DATE', 'PROJECT'):
        parser.error("Unsupported category '" + args.update[0] + "'")

    if args.add and args.add[0] not in ('APACHE2', 'GPL3', 'MIT'):
        parser.error("Unsupported copyright preface '" + args.add[0] + "'")

    if args.file and not os.path.isfile(args.file[0]):
        raise FileNotFoundError("File '" + args.file[0] + "' not found")

    if args.dir and not os.path.isdir(args.dir[0]):
        raise FileNotFoundError("Directory '" + args.file[0] + "' not found")

    if args.add:
        file_name = pkg_resources.resource_filename(__name__, 'templates/' + str(args.add[0]).lower() + '_copyright_preface_template')
        with open(file_name, 'r') as f:
            file_content = f.read()
        copyright_content = file_content.format(project=args.add[1], author=args.add[2], date=args.add[3])

        copyright_lines = copyright_content.split('\n')

        if args.file:
            job_add(copyright_lines, [args.file[0]], args.backup, args.surround, args.force)
        else:
            target_files = list_target_files(args.dir[0])
            target_files = [item for item in target_files if os.path.splitext(item)[1] in ('.c', '.h', '.py')]

            chunks = chunkify(target_files, JOBS_NUMBER)

            with futures.ProcessPoolExecutor(JOBS_NUMBER) as executor:
                list(f.result() for f in futures.as_completed(executor.submit(job_add, copyright_lines,
                    chunk, args.backup, args.surround, args.force) for chunk in chunks))
    elif args.replace:
        with open(args.replace[0], 'r') as current_copyright_file:
            current_copyright_content = current_copyright_file.read()

        with open(args.replace[1], 'r') as new_copyright_file:
            new_copyright_content = new_copyright_file.read()

        if args.file:
            job_replace(current_copyright_content, new_copyright_content, [args.file[0]], args.backup)
        else:
            target_files = list_target_files(args.dir[0])
            target_files = [item for item in target_files if os.path.splitext(item)[1] in ('.c', '.h', '.py')]

            chunks = chunkify(target_files, JOBS_NUMBER)

            with futures.ProcessPoolExecutor(JOBS_NUMBER) as executor:
                list(f.result() for f in futures.as_completed(executor.submit(job_replace, current_copyright_content,
                    new_copyright_content, chunk, args.backup) for chunk in chunks))
    elif args.update:
        if args.file:
            job_update(args.update[0], [args.file[0]], args.update[1], args.update[2], args.backup)
        else:
            target_files = list_target_files(args.dir[0])
            target_files = [item for item in target_files if os.path.splitext(item)[1] in ('.c', '.h', '.py')]

            chunks = chunkify(target_files, JOBS_NUMBER)

            with futures.ProcessPoolExecutor(JOBS_NUMBER) as executor:
                list(f.result() for f in futures.as_completed(executor.submit(job_update, args.update[0], chunk,
                    args.update[1], args.update[2], args.backup) for chunk in chunks))
    elif args.erase:
        if args.file:
            job_erase([args.file[0]], args.backup)
        else:
            target_files = list_target_files(args.dir[0])
            target_files = [item for item in target_files if os.path.splitext(item)[1] in ('.c', '.h', '.py')]

            chunks = chunkify(target_files, JOBS_NUMBER)

            with futures.ProcessPoolExecutor(JOBS_NUMBER) as executor:
                list(f.result() for f in futures.as_completed(executor.submit(job_erase,  chunk,
                    args.backup) for chunk in chunks))

if __name__ == '__main__':
    sys.exit(main())