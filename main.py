import configparser
import sys
import time

from module.file_folder_manipulation import get_word_list, create_files_and_directories
from module.compression import apply_compression_pipeline
from module.database import apply_db_pipeline
from module.pdf_generation import apply_pdf_pipeline
config_file_path = r"configs/config.ini"


def main(sys_argv):
    start_time = time.time()
    config = configparser.ConfigParser()
    temp = config.read(config_file_path)

    dictionary_filepath = config['PATHS']['input_dictionary']
    output_folder = config['PATHS']['output_directory']
    directory_candidates = config['module']['directory_candidates']
    db_name = config['Database']['database_name']
    table_name = config['Database']['table_name']

    word_list = get_word_list(dictionary_filepath)
    print("Success in Reading Dictionary File")

    directory_candidates = list(directory_candidates)
    curated = create_files_and_directories(word_list, output_folder, directory_candidates)
    print("Success in Creating Required Files and Directories")

    print("Compressing Files and Reporting Compression Ratios")
    apply_compression_pipeline(output_folder)

    apply_db_pipeline(db_file=db_name, table_name=table_name, word_list=word_list)
    apply_pdf_pipeline(config['Database'], config['PDF'])
    end_time = time.time()
    proecess_time = end_time - start_time

    print("Process completed in :", proecess_time)


if __name__ == "__main__":
    main(sys.argv)
