import configparser
import sys

from module.file_folder_manipulation import get_word_list, create_files_and_directories
from module.compression import apply_compression_pipeline
from module.database import apply_db_pipeline

config_file_path = r"configs\config.ini"


def main(sys_argv):
    config = configparser.ConfigParser()
    temp = config.read(config_file_path)

    dictionary_filepath = config['PATHS']['input_dictionary']
    output_folder = config['PATHS']['output_directory']
    db_name = config['Database']['database_name']
    table_name = config['Database']['table_name']

    word_list = get_word_list(dictionary_filepath)
    print("Success in Reading Dictionary File")

    curated = create_files_and_directories(word_list, output_folder)
    print("Success in Creating Required Files and Directories")

    print("Compressing Files and Reporting Compression Ratios")
    apply_compression_pipeline(output_folder)

    # apply_db_pipeline(db_file=db_name, table_name=table_name, word_list=word_list)


if __name__ == "__main__":
    main(sys.argv)
