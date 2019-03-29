import os
import shutil
import schedule
import time
import smtplib
import ssl
from datetime import datetime

# Scheduled booleans
scheduled = False
scheduled_hourly = False
scheduled_daily = False
scheduled_intervals = False

# Copy/Delete options
delete_files = False
delete_folders = False
copy_new = True

# Reporting functionality
console_report = True
text_report = False
email_report = False

# Set source/destination
source_directory = 'C:/Users/braden.richardson/Documents/Testing/Test 1'
destination_directory = "C:/Users/braden.richardson/Documents/Testing/Test 2"

# Core timing variables
datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
schedule_minute_intervals = 1
schedule_daily_time = "15:18"

# Create reporting arrays to produce reports
reporting_array_copied = []
reporting_array_copied_to = []
reporting_array_deleted = []

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
def backup_directory(source, destination):
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
def delete_directory(source):
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


# Set schedules if they are set to True
if scheduled_intervals:
    schedule.every(schedule_minute_intervals).minutes.do(backup_directory, source_directory, destination_directory)
    if delete_files:
        schedule.every(schedule_minute_intervals).minutes.do(delete_directory, source_directory)

if scheduled_hourly:
    schedule.every().hour.do(backup_directory, source_directory, destination_directory)
    if delete_files:
        schedule.every().hour.do(delete_directory, source_directory)

if scheduled_daily:
    schedule.every().day.at(schedule_daily_time).do(backup_directory, source_directory, destination_directory)
    if delete_files:
        schedule.every().day.at(schedule_daily_time).do(delete_directory, source_directory, destination_directory)

# Run scheduled functions, checking for reporting functions
while scheduled:
    schedule.run_pending()
    if console_report:
        console_report_copied(reporting_array_copied, reporting_array_copied_to)
        if delete_files:
            console_report_deleted(reporting_array_deleted)
    if text_report:
        text_report_copied(reporting_array_copied, reporting_array_copied_to, destination_directory)
        if delete_files:
            text_report_deleted(reporting_array_deleted, destination_directory)
    if email_report:
        email_report_copied(reporting_array_copied, reporting_array_copied_to)
    time.sleep(1)

# If not scheduled, run once, checking if files need to be deleted after and if reporting is needed
if not scheduled:
    backup_directory(source_directory, destination_directory)
    if delete_files:
        delete_directory(source_directory)
    if console_report:
        console_report_copied(reporting_array_copied, reporting_array_copied_to)
        if delete_files:
            console_report_deleted(reporting_array_deleted)
    if text_report:
        text_report_copied(reporting_array_copied, reporting_array_copied_to, destination_directory)
        if delete_files:
            text_report_deleted(reporting_array_deleted, destination_directory)
    if email_report:
        email_report_copied(reporting_array_copied, reporting_array_copied_to)
        if delete_files:
            email_report_deleted(reporting_array_deleted)
