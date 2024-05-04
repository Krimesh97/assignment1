import os
import shutil
from prettytable import PrettyTable


def get_dir_size(path: str) -> float:
    """
    Returns the size of target directory in KB
    :param path: [type: str] Path to target directory
    :return: [type:float] total size of directory in KB
    """
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size / 1024
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def get_file_size(path: str) -> float:
    """
    Returns the size of target file in KB
    :param path: [type: str] Path to target file
    :return: [type:float] total size of file in KB
    """
    return os.path.getsize(path) / 1024


def create_compression(path: str, out_path) -> float:
    """
    Creates compression file for input file
    :param path: Path to target file/folder
    :param out_path: Path where compressed file is saved
    :return: size after compression
    """
    shutil.make_archive(out_path, 'zip', path)
    return get_file_size(out_path+'.zip')


def apply_compression_pipeline(root_folder):
    """
    Creates compressed file for directories[a~z] inside root_folder and reports compression ratio
    :param root_folder: path to directory containing [a~z] folder created py processing dictionary
    :return: None
    """
    valid_folders = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z']
    target_folders = [os.path.basename(f.path) for f in os.scandir(root_folder) if
                      f.is_dir() and os.path.basename(f.path) in valid_folders]
    original_size_dict = {}
    original_size_dict['Alpahbet'] = {'Original Size(KB)', 'Compressed Size(KB)', 'Compression Ratio'}
    print('Reporting Folder Sizes')

    for target_folder in target_folders:
        original_size = get_dir_size(os.path.join(root_folder, target_folder))
        original_size_dict[target_folder] = original_size
        print("'{alphabet}' -> {original_size} KB".format(alphabet=target_folder, original_size=original_size))

    print('Compression Folders and Reporting Compression Ratio')
    table = PrettyTable()
    table.field_names = ['Alphabet', 'Original Size', 'Compressed Size', 'Compression Ratio']
    for target_folder in target_folders:
        target_folder_path = os.path.join(root_folder, target_folder)
        output_path = os.path.join(root_folder, target_folder)

        original_size = original_size_dict[target_folder]
        compressed_size = create_compression(target_folder_path, output_path)
        table.add_row([target_folder,original_size, compressed_size, original_size / compressed_size])
    print(table)
