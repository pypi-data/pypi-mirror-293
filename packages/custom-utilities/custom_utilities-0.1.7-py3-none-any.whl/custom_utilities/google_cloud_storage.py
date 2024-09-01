import os
import re

from google.cloud import storage
from multiprocessing import cpu_count, Pool
from tqdm import tqdm
from typing import Tuple, Union

def get_gcs_url(gcs_bucket_name:str, gcs_file_path:str) -> str:
    """Return Google Cloud Storage (URL) for given file path in a specific bucket.

    Args:
        gcs_bucket_name (`str`, Mandatory): The name of GCS Bucket which the file exists in.
        gcs_file_path (`str`, Mandatory): The complete path of requested file (must include extension).
    """
    return 'gs://'+gcs_bucket_name+'/'+gcs_file_path

def _traverse_folder(
    source_folder_path:str,
    bucket_name:str,
    bucket_folder_path:str,
    upload_to_single_folder:bool
):
    """Recursive function to traverse inside a given folder then upload all the files inside it to GCS Bucket.

    Args:
        source_folder_path (`str`, Mandatory): path of the folder to be traversed.
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file will be uploaded to.
        bucket_folder_path (`str`, Mandatory): Folder path to which any files in specific folder will be uploaded to in the bucket.
        upload_to_single_folder (`bool`, Optional): Will upload all files inside a folder and all subfolder into a single folder in GCS Bucket.
    """

    # * Function logic
    entries = list(os.scandir(source_folder_path))
    file_tasks:list[Tuple] = []
    for entry in entries:
        if entry.is_file():
            if upload_to_single_folder:
                bucket_file_path:str = f"{bucket_folder_path}/{entry.name}"
            else:
                bucket_file_path = re.sub(r'^.*?/', f"{bucket_folder_path}/", entry.path.replace('\\', '/'))
            file_tasks.append((entry.path, bucket_name, bucket_file_path))
        elif entry.is_dir():
            file_tasks.extend(_traverse_folder(entry.path, bucket_name, bucket_folder_path, upload_to_single_folder))
    return file_tasks

def _upload_file_to_bucket(source_file_path:str, bucket_name:str, bucket_file_path:str):
    """Private function to upload a single file to a GCS Bucket.

    Args:
        source_file_path (`str`, Mandatory): Path of the to be uploaded file.
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file will be uploaded to.
        bucket_file_path (`str`, Mandatory): Designated path of the uploaded file in the GCS Bucket.
    """

    # * Function Logic
    file_blob = storage.Client().bucket(bucket_name).blob(bucket_file_path)
    if not file_blob.exists():
        file_blob.upload_from_filename(source_file_path)

def _upload_file_task(args) -> str:
    """Wrapper function for multiprocessing."""
    _upload_file_to_bucket(*args)

def _process_file_tasks(
    file_tasks:list[Tuple],
    use_multiprocessing:bool,
    num_workers:int
):
    """Private function to handle the uploading of files to a Google Cloud Storage (GCS) Bucket.

    Args:
        file_tasks (`list[Tuple]`, Mandatory): A list of tuples, where each tuple contains the arguments required by the `_upload_file_to_bucket` function.
        use_multiprocessing (`bool`, Mandatory): Flag indicating whether to use multiprocessing for parallel uploads.
        num_workers (`int`, Optional): The number of worker processes to use for multiprocessing. If not set and multiprocessing is enabled, the number of CPU cores will be used.

    Raises:
        RuntimeError: If multiprocessing is enabled and an error occurs during the process.

    Behaviors:
        - If the operating system is Windows, multiprocessing is disabled with a message, and the upload proceeds in single-threaded mode.
        - If an error occurs during multiprocessing, the function falls back to single-threaded uploads.
        - If multiprocessing is not enabled or an error occurs, files are uploaded sequentially.
    """

    # * Function Logic
    if use_multiprocessing:
        # * Check the OS
        if os.name == 'nt':
            # * Disable multiprocessing for windows OS
            print('Multiprocessing feature is not yet available for Windows OS in this version.\nFalling back to single-threaded upload.')
            use_multiprocessing = False
        else:  # Linux or other OS
            try:
                num_workers = num_workers if num_workers else cpu_count()
                with Pool(num_workers) as pool:
                    for _ in tqdm(pool.imap_unordered(_upload_file_task, file_tasks), total=len(file_tasks), desc="Uploading files"):
                        pass
            except RuntimeError as e:
                print(f"Multiprocessing failed with error: {e}.\nFalling back to single-threaded upload.")
                use_multiprocessing = False

    if not use_multiprocessing:
        for file_task in tqdm(file_tasks, desc="Uploading files"):
            _upload_file_to_bucket(*file_task)

def upload_file(
    source_file_paths:Union[list[str], str] = None,
    bucket_name:str = None,
    bucket_folder_path:str = None,
    use_multiprocessing:bool = False,
    num_workers:int = None
):
    """Public function to upload a single file or multilpe files to a GCS Bucket.
    If `source_file_paths` is a string (indicating a single file), this will be turned into single-element list.

    Args:
        source_file_paths (`list[str]` or `str`, Mandatory): Path of the to be uploaded file (can be a str for single file or list[str] for multiple files).
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the file will be uploaded to.
        bucket_file_path (`str`, Mandatory): Designated folder path of the uploaded file in the GCS Bucket.
        use_multiprocessing (`bool`, Optional): Enables the use of multiprocessing to upload files in parallel, potentially speeding up the upload process. Defaults to `False`.
        num_workers (`int`, Optional): Specifies the number of worker processes to use for multiprocessing. If not set, the default is the number of CPU cores available.

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
    file_tasks = [(source_file_path, bucket_name, f"{bucket_folder_path}/{os.path.basename(source_file_path)}") for source_file_path in source_file_paths]
    _process_file_tasks(file_tasks, use_multiprocessing, num_workers)

def upload_folder(
    source_folder_paths:Union[list[str], str] = None,
    bucket_name:str = None,
    bucket_folder_path:str = None,
    upload_to_single_folder:bool = False,
    use_multiprocessing:bool = False,
    num_workers:int = None
):
    """Public function to upload a single folder or multiple folders and all its contets to a GCS Bucket.
    If `source_folder_paths` is a string (indicating a single folder), this will be turned into single-element list.

    Args:
        source_folder_paths (`list[str]` or `str`, Mandatory): Path of the to be uploaded folder (can be a str for single folder or list[str] for multiple folders).
        bucket_name (`str`, Mandatory): The name of the GCS Bucket where the folder will be uploaded to.
        bucket_folder_path (`str`, Mandatory): Designated folder path of the uploaded folder in the GCS Bucket.
        upload_to_single_folder (`bool`, Optional): Will upload all files inside a folder and all subfolder into a single folder in GCS Bucket.
        use_multiprocessing (`bool`, Optional): Enables the use of multiprocessing to upload files in parallel, potentially speeding up the upload process. Defaults to `False`.
        num_workers (`int`, Optional): Specifies the number of worker processes to use for multiprocessing. If not set, the default is the number of CPU cores available.

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
    file_tasks:list[Tuple] = []
    for source_folder_path in source_folder_paths:
        file_tasks.extend(_traverse_folder(source_folder_path, bucket_name, bucket_folder_path, upload_to_single_folder))
    _process_file_tasks(file_tasks, use_multiprocessing, num_workers)