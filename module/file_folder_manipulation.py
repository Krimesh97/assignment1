import os
import sys
import re

# import string
# import enchant
# word_checker = enchant.Dict("en_US")


def get_word_list(file_path: str | os.PathLike, encoding: str = 'utf-8') -> list:
    """
    function to read words in a text file
    :param file_path: [type str] path of text file, the words in the text should be delimited by carriage return
    :param encoding: [type str] encoding used in the text file
    :return: [type list] list of words in the text file
    """

    try:
        f = open(file_path, 'r', encoding=encoding)
        word_list = f.read().splitlines()

        # curated_word_list = list(filter(lambda token: token not in string.punctuation, word_list))
        # curated_word_list = [word for word in curated_word_list if '//' not in word]
        # return curated_word_list

        return word_list
    except OSError:
        print("Could not open/read file:", file_path)
        sys.exit()


def create_directories(out_folder_root: str | os.PathLike, directory_candidates: list):
    """
    Creates Directories a-z up to 2 levels
    """
    for level_one_dir in directory_candidates:
        for level_two_dir in directory_candidates:
            folder_path = os.path.join(out_folder_root, level_one_dir, level_two_dir)
            os.makedirs(folder_path, exist_ok=True)


def create_files_and_directories(word_list: list | tuple, out_folder_root: str | os.PathLike,
                                 directory_candidates: list):
    """
    Creating Directories Levels based on word characters and Files with content = 100 x word
    :param directory_candidates:  [type: list] list of directories to be created
    :param word_list: [type:list, tuple] list of words for processing
    :param out_folder_root: root output folder where directories are created
    :return: pass
    """
    print("Creating Directories and files ...")
    create_directories(out_folder_root, directory_candidates)
    curated_word_list = []
    for word in word_list:
        word = word.lower()

        alpha_only = re.sub(r'[^\w\s]', '', word)
        first_letter = alpha_only[0]
        second_letter = alpha_only[1] if len(alpha_only) > 1 else ''
        out_file_name = word + '.txt'
        out_folder = os.path.join(out_folder_root, first_letter, second_letter)
        out_file_path = os.path.join(out_folder, out_file_name)

        try:
            with open(out_file_path, "w") as file:
                to_write = '\n'.join([word] * 100)
                file.write(to_write)
            curated_word_list.append(word)
        except Exception as error:
            print('error occurred when writing files: ', word, ':', error)
    return curated_word_list
