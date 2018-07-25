from .console_logger import ConsoleLogger

from shutil import copyfile
import os

def replace_copyright(target_file_name, current_copyright_content, new_copyright_content, with_backup):
    with open(target_file_name, 'r') as target_file:
        target_content = target_file.read()
        if (target_content.find(current_copyright_content) == -1):
            ConsoleLogger.warn("Specified copyright doesn't match in " + target_file_name)
            return False
    if with_backup:
        copyfile(target_file_name, target_file_name + '.backup')
    os.remove(target_file_name)
    with open(target_file_name, 'w') as new_file:
        new_file.write(target_content.replace(current_copyright_content, new_copyright_content))
    ConsoleLogger.success('Copyright replaced in ' + target_file_name)
    return True