#!/usr/bin/python3
 
import re
import logging
import time
import datetime
import os
import sys
from google.cloud import storage

auth_file = "/home/homelab-266121-2d848d8d72d7.json"

print("Starting UploadFiles.py")


# ------------------
# Setup Google Logging
# ------------------
try:
    import google.cloud.logging
    # Instantiates a client
    logging_client = google.cloud.logging.Client.from_service_account_json(auth_file)
    # Connects the logger to the root logging handler; by default this captures
    logging_client.setup_logging()
    #logging.basicConfig(level=logging.INFO)
except:
    logging.basicConfig(filename='/var/log/UploadFiles_backup.log', level=logging.INFO)

# ------------------
# Define Functions 
# ------------------

def find_files(working_dir, x):
    pattern = re.compile(x)
    file_list = []
    try:
        for file in os.listdir(working_dir):
            if re.match(pattern=pattern, string=file):
                file_list.append(file)
        return(file_list)
    except:
        file_list = []
        return(file_list)

def rm_files(file_list, working_dir):
    for file in file_list:
        try:
            to_rm = os.path.join(working_dir, file)
            os.remove(to_rm)
            print("Removed {0}".format(to_rm))
        except Exception as e:
            dt = datetime.datetime.now()
            logging.log(msg="Could not Remove{0}  MSG:{1}".format(to_rm, e), level=logging.WARNING)

            
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client.from_service_account_json(auth_file)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    try:
        blob.upload_from_filename(source_file_name)
        return("200")
    except Exception as e:
        return("File Write Error {0}".format(e))
    
def upload_rm_files(local_dir, remote_dir, search_string):
    upload_count = 0
    file_list = find_files(local_dir, search_string)
    file_count = len(file_list)
    for files in file_list:
        print("Processing: {0}".format(files))
        dt = datetime.datetime.now()
        dt2 = dt.strftime("%Y-%m-%d_%H-%M")
        try:
            old = os.path.join(local_dir, files)
            new = os.path.join(remote_dir, dt2, files)
            status = upload_blob(data_store, old, new)
        except Exception as e:
            dt = datetime.datetime.now()
            logging.log(msg="Could not Upload{0}  MSG:{1}".format(old, e), level=logging.WARNING)
            status = "0"
        if status == "200":
            os.remove(old)
            upload_count += 1
        else:
            logging.log(msg="Did not remove{0}  Status:{1}".format(old, status), level=logging.WARNING)
    #if upload_count > 0:
    logging.log(msg="Uploaded {0} of {1} files".format(upload_count, file_count), level=logging.INFO)

            
# ------------------
# Run main program
# ------------------

data_store = "lab_data_repo"

local_dir = "/home/sftp/upload"
remote_dir = "sftp/upload"
search_string = ".*"

print("Running upload_rm_files")
upload_rm_files(local_dir, remote_dir, search_string)
#time.sleep(20)

