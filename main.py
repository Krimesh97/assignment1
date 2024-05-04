import configparser
import sys

from module.file_folder_manipulation import get_word_list, create_files_and_directories
from module.compression import apply_compression_pipeline
config_file_path = r"configs\config.ini"


def main(sys_argv):
    config = configparser.ConfigParser()
    temp = config.read(config_file_path)

    dictionary_filepath = config['PATHS']['input_dictionary']
    output_folder = config['PATHS']['output_directory']

    print("Reading Dictionary File")
    word_list = get_word_list(dictionary_filepath)
    curated = create_files_and_directories(word_list, output_folder)


if __name__ == "__main__":
    main(sys.argv)