from .replace import replace_copyright
from .utils import chunkify, list_target_files, read_lines
from .console_logger import ConsoleLogger
from .update import update_copyright_date, update_copyright_author, update_copyright_project_name
from .comment import comment_copyright
from .uncomment import uncomment_copyright
from .find import find_copyright

import sys
import os
import argparse
from concurrent import futures

JOBS_NUMBER = 5

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

        if args.update[0] == 'AUTHOR':
            if not update_copyright_author(uncommented_copyright, current, new):
                ConsoleLogger.error("Failed to update copyright author")
        elif args.update[0] == 'DATE':
            if not update_copyright_date(uncommented_copyright, current, new):
                ConsoleLogger.error("Failed to update copyright date")
        elif args.update[0] == 'PROJECT':
            if not update_copyright_project_name(uncommented_copyright, current, new):
                ConsoleLogger.error("Failed to update copyright project name")

        new_copyright = comment_copyright(uncommented_copyright)

        replace_copyright(target_file_name, ''.join(copyright.lines), ''.join(new_copyright.lines), with_backup)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', nargs=1, metavar=('PATH'))
    parser.add_argument('-d', '--dir', nargs=1, metavar=('PATH'))
    parser.add_argument('-r', '--replace', nargs=2, metavar=('CURRENT_PATH', 'NEW_PATH'))
    parser.add_argument('-u', '--update', nargs=3, metavar=('[AUTHOR|DATE|PROJECT]', 'CURRENT', 'NEW'))
    parser.add_argument('-e', '--erase', action='store_true')
    parser.add_argument('-b', '--backup', action='store_true')
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.error('One of --file or --dir must be given')

    mode_count = sum([1 if arg else 0 for arg in (args.replace, args.update, args.erase)])
    if mode_count == 0:
        parser.error('One of --replace or --update or --erase must be given')
    elif mode_count > 1:
        parser.error('Only one of --replace or --update or --erase must be given')

    if args.update and args.update[0] not in ('AUTHOR', 'DATE', 'PROJECT'):
        parser.error("Unsupported category '" + args.update[0] + "'")

    if args.file and not os.path.isfile(args.file[0]):
        raise FileNotFoundError("File '" + args.file[0] + "' not found")

    if args.dir and not os.path.isdir(args.dir[0]):
        raise FileNotFoundError("Directory '" + args.file[0] + "' not found")

    if args.replace:
        with open(args.replace[0], 'r') as current_copyright_file:
            current_copyright_content = current_copyright_file.read()

        with open(args.replace[1], 'r') as new_copyright_file:
            new_copyright_content = new_copyright_file.read()

        if args.file:
            job_replace(current_copyright_content, new_copyright_content, [args.file[0]], args.backup)
        else:
            target_files = list_target_files(args.dir[0])
            target_files = [item for item in target_files if os.path.splitext(item)[1] not in ('.c', '.h', '.py')]

            chunks = chunkify(target_files, JOBS_NUMBER)

            with futures.ProcessPoolExecutor(JOBS_NUMBER) as executor:
                list(f.result() for f in futures.as_completed(executor.submit(job_replace, current_copyright_content,
                    new_copyright_content, chunk, args.backup) for chunk in chunks))
    elif args.update:
        if args.file:
            job_update(args.update[0], [args.file[0]], args.update[1], args.update[2], args.backup)
        else:
            target_files = list_target_files(args.dir[0])
            target_files = [item for item in target_files if os.path.splitext(item)[1] not in ('.c', '.h', '.py')]

            chunks = chunkify(target_files, JOBS_NUMBER)

            with futures.ProcessPoolExecutor(JOBS_NUMBER) as executor:
                list(f.result() for f in futures.as_completed(executor.submit(job_update, args.update[0], chunk,
                    args.update[1], args.update[2], args.backup) for chunk in chunks))


if __name__ == '__main__':
    sys.exit(main())