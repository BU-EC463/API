import boto3
import re

def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        print(e)
        return False
    return True

def delete_file(bucket, object_name):
    """
    Delete a file from an S3 bucket

    :param bucket: Bucket of the file
    :param object_name: S3 object name
    :return: True if file was deleted, else False
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_object(Bucket=bucket, Key=object_name)
    except Exception as e:
        print(e)
        return False
    return True

def download_file(bucket, object_name, file_name=None):
    """
    Download a file from an S3 bucket

    :param bucket: Bucket to download from
    :param object_name: S3 object name
    :param file_name: File name to download the object to. 
                      If not specified, object_name is used.
    :return: True if file was downloaded, else False
    """
    # If file_name was not specified, use object_name
    if file_name is None:
        file_name = object_name

    # Download the file
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket, object_name, file_name)
    except Exception as e:
        print(e)
        return False
    return True

def find_object_with_highest_number(bucket_name):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    max_number = -1
    object_with_max_number = None
    
    if 'Contents' in response:
        for obj in response['Contents']:
            object_name = obj['Key']
            # Assuming the number is at the end and is preceded by a non-numeric character
            # For example: 'file-123', 'image_456.png'
            match = re.search(r'(\d+)(?!.*\d)', object_name)
            if match:
                number = int(match.group())
                if number > max_number:
                    max_number = number
                    object_with_max_number = object_name
    
    return object_with_max_number



# Replace 'my_bucket' with your S3 bucket name
# Replace 'my_file.txt' with the path to your file
# Replace 'my_object_name' with the desired object name in S3 (optional)

# if upload_file('Analysis/Daily Snapshot.csv', 'dailysupplysnapshot', 'snapshot_1'):
#     print("Upload successful")
# else:
#     print("Upload failed")

# if download_file('dailysupplysnapshot', 'snapshot_1', 'snapshot.csv'):
#     print("Download successful")
# else:
#     print("Download failed")

# To delete the file you just uploaded
# if delete_file('my_bucket', 'my_object_name'):
#     print("Deletion successful")
# else:
#     print("Deletion failed")

highest_number_object = find_object_with_highest_number('dailysupplysnapshot')
if highest_number_object:
    print(f"The object with the highest number: {highest_number_object}")
else:
    print("No objects found or no numeric endings detected.")
