import os
import shutil
from datetime import datetime
import ssl
import smtplib
import argparse

# Implement if __name__ == __main__
# Implement passing arguments through command line using argparse or click
# Implement ease of use, IE calling this function from anywhere with CMD - Document

# Create reporting arrays to produce reports
reporting_array_copied = []
reporting_array_copied_to = []
reporting_array_deleted = []

# Argparse variables
parser = argparse.ArgumentParser(description='Backup files/folders from one location to another')
parser.add_argument('s', '--source', type=str, metavar='', required=True, help='Source directory to be copied')
parser.add_argument('d', '--destination', type=str, metavar='', required=True,
                    help='Destination directory for copied files')
parser.add_argument('cn', '--copy_new', type=bool, help='Copy newly modified files')
parser.add_argument('dfi', '--delete_files', type=bool, help='Delete files afterwards')
parser.add_argument('dfo', '--delete_folders', type=bool, help='Delete folders afterwards')
parser.add_argument('rc', '--report_console', type=bool, help='Console output report')
parser.add_argument('rt', '--report_text', type=bool, help='Text output report')
parser.add_argument('re', '--report_email', type=bool, help='Email output report')
args = parser.parse_args()


# Core timing variables
datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Specify email details
reporting_email = ""
port = 465
password = 'rjvswsakmeocayrm'
sender_email = "braden.richardson13@gmail.com"
context = ssl.create_default_context()


def copy_file_and_report(item_path, destination_path, item, destination):
    shutil.copy2(item_path, destination_path)
    reporting_array_copied.append(item)
    reporting_array_copied_to.append(destination)


def copy_folder_and_report(item_path, destination_path, item, destination):
    shutil.copytree(item_path, destination_path)
    reporting_array_copied.append(item)
    reporting_array_copied_to.append(destination)


def delete_file_and_report(item_path, item):
    os.remove(item_path)
    reporting_array_deleted.append(item)


def delete_folder_and_report(item_path, item):
    shutil.rmtree(item_path)
    reporting_array_deleted.append(item)


# Iterate through both folder arrays, compare and copy as needed
def backup_directory(source, destination, copy_new=False):
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if item not in os.listdir(destination):
            if os.path.isdir(item_path):
                copy_folder_and_report(item_path, destination_path, item, destination)
            else:
                copy_file_and_report(item_path, destination_path, item, destination)
        if os.path.isdir(item_path):
            backup_directory(item_path, destination_path)
        if copy_new and item in os.listdir(destination) and not os.path.isdir(item_path) and \
                os.stat(item_path).st_mtime - os.stat(destination_path).st_mtime > 0:
            copy_file_and_report(item_path, destination_path, item, destination)
    return True


# Iterate through source folder array and delete files
def delete_directory(source, delete_folders=False):
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        if os.path.isdir(item_path) and not delete_folders:
            delete_directory(item_path)
        elif os.path.isdir(item_path) and delete_folders:
            delete_folder_and_report(item_path, item)
        else:
            delete_file_and_report(item_path, item)
    return True


def console_report_copied(copied_from, copied_to):
    if not copied_from and not copied_to:
        return None
    else:
        for index in range(len(copied_from)):
            print(datetime_now, "- Copied:", copied_from[index], "to", copied_to[index])
    copied_from.clear()
    copied_to.clear()
    return True


def console_report_deleted(deleted):
    if not deleted:
        return None
    else:
        for index in range(len(deleted)):
            print(datetime_now, "- Deleted:", deleted[index])
    deleted.clear()
    return True


def text_report_copied(copied_from, copied_to, destination):
    if not copied_from and not copied_to:
        return None
    else:
        os.chdir(destination)
        with open("Copy Report.txt", "a+") as text_copy_report:
            for index in range(len(copied_from)):
                text_copy_report.write(str(datetime_now))
                text_copy_report.write(" - Copied: ")
                text_copy_report.write(copied_from[index])
                text_copy_report.write(" to ")
                text_copy_report.write(copied_to[index])
                text_copy_report.write("\n")
    copied_from.clear()
    copied_to.clear()
    return True


def text_report_deleted(deleted, destination):
    if not deleted:
        return None
    else:
        os.chdir(destination)
        with open("Deleted Report.txt", "a+") as deleted_report:
            for index in range(len(deleted)):
                deleted_report.write(str(datetime_now))
                deleted_report.write(" - Deleted: ")
                deleted_report.write(deleted[index])
                deleted_report.write("\n")
    deleted.clear()
    return True


def send_report_email(string_join_list):
    message = ''.join(string_join_list)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reporting_email, message)
    return True


def email_report_copied(copied_from, copied_to):
    if not copied_from and not copied_to:
        return None
    else:
        string_join_list = ["Subject: Pivot Backup Copy Report\n\n"]
        for index in range(len(copied_from)):
            string_join_list.append(str(datetime_now))
            string_join_list.append(" - Copied: ")
            string_join_list.append(copied_from[index])
            string_join_list.append(" to ")
            string_join_list.append(copied_to[index])
            string_join_list.append("\n")
        send_report_email(string_join_list)
    return True


def email_report_deleted(deleted):
    if not deleted:
        return None
    else:
        string_join_list = ["Subject: Pivot Backup Deleted Report\n\n"]
        for index in range(len(deleted)):
            string_join_list.append(str(datetime_now))
            string_join_list.append(" - Deleted: ")
            string_join_list.append(deleted[index])
            string_join_list.append("\n")
        send_report_email(string_join_list)
    return True

# This works
if __name__ == '__main__':
    backup_directory(args.source, args.destination)
