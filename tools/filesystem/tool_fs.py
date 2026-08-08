from langchain_core.tools import tool

from .service import FileService

file_service = FileService()


@tool
def filesystem_read_file(path: str):
    """
    Reads and returns the text content of a file. 
    Use this tool when you need to view, analyze, or extract information from a specific file.

    Parameters:
    - path: The full path (absolute or relative) to the file to be read.
    """
    return file_service.read_file(path)


@tool
def filesystem_delete_file(path: str):
    """
    Permanently deletes a file from the system. 
    Use this tool to remove a file. Note: This tool cannot be used to delete folders.

    Parameters:
    - path: The full path to the file that needs to be deleted.
    """
    return file_service.delete_file(path)


@tool
def filesystem_move_file(source: str, destination: str):
    """
    Moves a file from a source location to a destination. 
    Automatically creates the destination directory if it does not exist.

    Parameters:
    - source: The full path of the file to move.
    - destination: The full path of the destination, INCLUDING the new filename.
    """
    return file_service.move_file(source, destination)


@tool
def filesystem_copy_file(source: str, destination: str):
    """
    Copies a file from a source location to a destination. 
    The original file remains intact. Automatically creates the destination directory if it does not exist.

    Parameters:
    - source: The full path of the file to copy.
    - destination: The full path of the destination, INCLUDING the new filename for the copied file.
    """
    return file_service.copy_file(source, destination)


@tool
def filesystem_rename_file(path: str, filename):
    """Renames a file. The file remains in its original directory.

    Parameters:
    - path: The full path to the file that needs to be renamed.
    - filename: The NEW name for the file ONLY (e.g., 'new_name.txt'). Do NOT include the directory path here.
    """
    return file_service.rename_file(path, filename)


@tool
def filesystem_create_file(path: str, filename: str):
    """ 
    Creates a new empty file. Automatically creates parent directories if they do not exist. 
    Will raise an error if the file already exists at the specified location.

    Parameters:
    - path: The directory path where the file will be created.
    - filename: The name of the file to create, including its extension (e.g., 'data.txt').
    """
    return file_service.create_file(path, filename)


@tool
def filesystem_find_file(path: str, filename: str):
    """
    Recursively searches for files within a directory and all its subdirectories based on a filename or glob pattern.

    Parameters:
    - path: The root directory path to start the search from.
    - filename: The exact filename or a glob pattern to search for (e.g., '*.txt', 'report_*.pdf').
    """
    return file_service.find_file(path, filename)


@tool
def filesystem_create_folder(path: str, nameFolder: str):
    """
    Creates a new directory (folder). Will not raise an error if the folder already exists.
    
    Parameters:
    - path: The parent directory path where the new folder will be created.
    - nameFolder: The name of the new folder to create (e.g., 'Backups').
    """
    return file_service.create_folder(path, nameFolder)


@tool
def filesystem_read_folder(path: str):
    """
    Lists the immediate contents (files and subdirectories) of a specified folder. 
    Does not search recursively into subdirectories.
    
    Parameters:
    - path: The full path to the directory to list.
    """
    return file_service.read_folder(path)


@tool
def filesystem_get_folder_size(path: str):
    """
    Calculates the total size of a folder and all its contents recursively. 
    Returns the total size broken down into bytes, KB, MB, and GB.
    
    Parameters:
    - path: The full path to the directory to calculate the size for.
    """
    return file_service.check_size_folder(path)
