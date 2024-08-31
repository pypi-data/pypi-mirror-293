import os
import re

from google.cloud import storage
from time import time
from typing import Union

from .output import clear_line
from .time import parse_duration

def get_gcs_url(gcs_bucket_name:str, gcs_file_path:str) -> str:
    """Return Google Cloud Storage (URL) for given file path in a specific bucket.

    Args:
        gcs_bucket_name (`str`, Mandatory): The name of GCS Bucket which the file exists in.
        gcs_file_path (`str`, Mandatory): The complete path of requested file (must include extension).
    """
    return 'gs://'+gcs_bucket_name+'/'+gcs_file_path

def _create_upload_summary(
    directories_count:int,
    uploaded_directories_count:int,
    files_count:int,
    uploaded_files_count:int,
    source_folder_path:str,
    elapsed_time:float
) -> str:
    """Return text of upload process summary included count of uploaded object(s), source folder, and elapsed time.

    Args:
        directories_count (`int`, Mandatory): The amount of directories existing in the source folder.
        uploaded_directories_count (`int`, Mandatory): The amount of directories uploaded from the source folder.
        files_count (`int`, Mandatory): The amount of files existing in the source folder.
        uploaded_files_count (`int`, Mandatory): The amount of files uploaded from the source folder.
        source_folder_path (`str`, Mandatory): The source folder which the contents will be uploaded from.
        elapsed_time (`float`, Mandatory): Total elapsed time to upload whole content of the source folder (in seconds).

    Returns:
        str: The upload process summary text
    """

    # * Function logic
    if directories_count == 0 and files_count == 0: 
        return 'No directories/files to be uploaded'
    else:
        uploaded_summary:list = [] # * Create empty upload summary
        # * Create folder(s) upload summary
        if uploaded_directories_count == directories_count:
            uploaded_directories_summary:str = str(uploaded_directories_count)
        else:
            f"{uploaded_directories_count} out of {directories_count}"
        if directories_count == 1:
            uploaded_directories_summary += ' directory'
        else:
            uploaded_directories_summary += ' directories'
        if directories_count > 0:
            uploaded_summary.append(uploaded_directories_summary)
        # * Create file(s) upload summary
        if uploaded_files_count == files_count:
            uploaded_files_summary:str = str(uploaded_files_count)
        else:
            f"{uploaded_files_count} out of {files_count}"
        if files_count == 1:
            uploaded_files_summary += ' file'
        else:
            uploaded_files_summary += ' files'
        if files_count > 0:
            uploaded_summary.append(uploaded_files_summary)
        return f"Successfully uploaded {' and '.join(uploaded_summary)} from '{source_folder_path}', Elapsed time: {parse_duration(elapsed_time)}"

def _traverse_folder(
    source_folder_path:str,
    storage_bucket:storage.Bucket,
    bucket_folder_path:str,
    upload_to_single_folder:bool = False
) -> None:
    """Recursive function to traverse inside a given folder then upload all the files inside it to GCS Bucket.

    Args:
        source_folder_path (`str`, Mandatory): path of the folder to be traversed.
        storage_bucket (`storage.Bucket`, Mandatory): GCS Bucket instance where the files inside the folder will be uploaded to.
        bucket_folder_path (`str`, Mandatory): Folder path to which any files in specific folder will be uploaded to in the bucket.
        upload_to_single_folder (`bool`, Optional): Will upload all files inside a folder and all subfolder into a single folder in GCS Bucket.
    """

    # * Function logic
    entries = list(os.scandir(source_folder_path))
    entries_count:int = len(entries)
    directories_count:int = len([entry for entry in entries if entry.is_dir()])
    files_count:int = len([entry for entry in entries if entry.is_file()])

    uploaded_directories_count:int = 0
    uploaded_files_count:int = 0

    elapsed_time:float = 0
    average_time:float = 0
    remaining_time:float = 0

    for index,entry in enumerate(entries, 1):
        if entry.is_file():
            uploaded_files_count += 1
            start_time:float = time()
            if upload_to_single_folder:
                bucket_file_path:str = bucket_folder_path + '/' + entry.name
            else:
                re.sub(r'^.*?/', bucket_folder_path + '/', entry.path.replace('\\', '/'))
            print(f"Current directory: '{os.path.dirname(entry.path)}', Uploading file: '{entry.name}', Uploaded file count: {index}/{entries_count} ({f"{(index / entries_count) * 100:.2f}"}%)")
            print(f"Uploading file to: '{bucket_file_path}'")
            print(f"Elapsed time: {parse_duration(elapsed_time)}, Average time: {parse_duration(average_time)}, Remaining time: {parse_duration(remaining_time)}")
            _upload_file_to_bucket(entry.path, storage_bucket, bucket_file_path)
            finish_time:float = time()
            elapsed_time += finish_time - start_time
            average_time = elapsed_time / index
            remaining_time = average_time * (entries_count - index)
            clear_line(3)

        elif entry.is_dir():
            uploaded_directories_count += 1
            _traverse_folder(entry.path, storage_bucket, bucket_folder_path)

    upload_summary:str = _create_upload_summary(directories_count, uploaded_directories_count, files_count, uploaded_files_count, source_folder_path, elapsed_time)
    print(upload_summary)

def _upload_file_to_bucket(source_file_path:str, storage_bucket:storage.Bucket, bucket_file_path:str) -> None:
    """Private function to upload a single file to a GCS Bucket.

    Args:
        source_file_path (`str`, Mandatory): Path of the to be uploaded file.
        storage_bucket (`storage.Bucket`, Mandatory): GCS Bucket instance where the file will be uploaded to.
        bucket_file_path (`str`, Mandatory): Designated path of the uploaded file in the GCS Bucket.
    """

    # * Function Logic
    file_blob = storage_bucket.blob(bucket_file_path)
    file_blob.upload_from_filename(source_file_path)

def upload_file(
    source_file_paths:Union[list[str],str]=None,
    bucket_name:str=None,
    bucket_folder_path:str=None
) -> None:
    """Public function to upload a single file or multilpe files to a GCS Bucket.
    If `source_file_paths` is a string (indicating a single file), this will be turned into single-element list.

    Args:
        source_file_paths (`list[str]` or `str`, Mandatory): Path of the to be uploaded file (can be a str for single file or list[str] for multiple files).
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file will be uploaded to.
        bucket_file_path (`str`, Mandatory): Designated folder path of the uploaded file in the GCS Bucket.

    Raises:
        ValueError: If `source_file_paths` is not given.
        TypeError: If `source_file_paths` is not a file.
        ValueError: If `bucket_name` is not given.
        ValueError: If `bucket_folder` path is not given.
    """

    # * Function arguments validation
    if not source_file_paths: raise ValueError('Source file paths is not given')
    if isinstance(source_file_paths, str): source_file_paths = [source_file_paths]
    for source_file_path in source_file_paths:
        if not os.path.isfile(source_file_path): raise TypeError(f"'{source_file_path}' is not a file")
    if not bucket_name: raise ValueError('Bucket name is not given')
    if not bucket_folder_path: raise ValueError('Bucket folder path is not given')

    # * Function Logic
    storage_bucket = storage.Client().bucket(bucket_name)
    for source_file_path in source_file_paths:
        source_file_name:str = source_file_path.split('/')[-1]
        bucket_file_path:str = bucket_folder_path + '/' + source_file_name
        _upload_file_to_bucket(source_file_path, storage_bucket, bucket_file_path)

def upload_folder(
    source_folder_paths:Union[list[str],str]=None,
    bucket_name:str=None,
    bucket_folder_path:str=None,
    upload_to_single_folder:bool=False
) -> None:
    """Public function to upload a single folder or multiple folders and all its contets to a GCS Bucket.
    If `source_folder_paths` is a string (indicating a single folder), this will be turned into single-element list.

    Args:
        source_folder_paths (`list[str]` or `str`, Mandatory): Path of the to be uploaded folder (can be a str for single folder or list[str] for multiple folders).
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the folder will be uploaded to.
        bucket_folder_path (`str`, Mandatory): Designated folder path of the uploaded folder in the GCS Bucket.
        upload_to_single_folder (`bool`, Optional): Will upload all files inside a folder and all subfolder into a single folder in GCS Bucket.

    Raises:
        ValueError: If `source_folder_paths` is not given.
        TypeError: If `source_folder_paths` is not a folder.
        ValueError: If `bucket_name` is not given.
        ValueError: If `bucket_folder` path is not given.
    """

    # * Function arguments validation
    if not source_folder_paths:
        raise ValueError('Source folder path is not given')
    if isinstance(source_folder_paths, str):
        source_folder_paths = [source_folder_paths]
    for source_folder_path in source_folder_paths:
        if not os.path.isdir(source_folder_path):
            raise TypeError(f"'{source_folder_path}' is not a folder")
    if not bucket_name:
        raise ValueError('Bucket path is not given')
    if not bucket_folder_path:
        raise ValueError('Bucket folder path is not given')
    
    # * Function logic
    storage_bucket = storage.Client().bucket(bucket_name)
    for source_folder_path in source_folder_paths:
        _traverse_folder(source_folder_path, storage_bucket, bucket_folder_path, upload_to_single_folder)