import sqlite3
import os


def setup_connection(db_file: str | os.PathLike) -> sqlite3.Connection:
    """
    Sets up Database and returns connection to it
    :param db_file: path to database file
    :return: db connection object
    """
    db_connection = None
    try:
        db_connection = sqlite3.connect(db_file)
        print("Connection to db successful:", sqlite3.version)
    except sqlite3.Error as error:
        print('Failed to setup database:', error)
    return db_connection


def setup_tables(db_connection: sqlite3.Connection, table_name: str):
    """
    creates required tables
    :param db_connection: connection to database
    :param table_name: Table name for insertion of words
    """
    try:
        # cursor object
        cursor_obj = db_connection.cursor()
        cursor_obj.execute("DROP TABLE IF EXISTS {}".format(table_name))
        table = """
                    CREATE TABLE {} (
                    Word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Word CHAR(512) NOT NULL
                   );
                """.format(table_name)
        cursor_obj.execute(table)
        print("Table is Ready")

    except sqlite3.Error as error:
        print('Failed to setup database:', error)


def insert_word_records(db_connection: sqlite3.Connection, table_name: str, word_list: list | tuple):
    """
    Inserts Word Records into table
    :param db_connection: connection to database
    :param table_name: Table name for insertion of words
    :param word_list: Dictionary word list to be added to table
    """
    try:
        cursor_obj = db_connection.cursor()
        for word in word_list:
            word = word.lower()
            sqlite_insert_with_param = """INSERT INTO {} (Word) VALUES (?);""".format(table_name)
            data_tuple = (word,)
            cursor_obj.execute(sqlite_insert_with_param, data_tuple)
        db_connection.commit()
        print("Dictionary Word records inserted successfully into WORDS_DICTIONARY table")
        cursor_obj.close()

    except sqlite3.Error as error:
        print("Failed to insert Dictionary Word into sqlite table:", error)


def run_analytics_simple(word_list: list | tuple):
    num_length_GT_5 = 0
    num_has_dup_chars = 0
    num_same_start_end = 0
    for word in word_list:
        num_length_GT_5 += int(len(word) > 5)
        num_has_dup_chars += int(len(word) > len(set(word)))
        num_same_start_end += int(word[0] == word)
    return num_length_GT_5, num_has_dup_chars, num_same_start_end


def update_table_make_upper(db_connection: sqlite3.Connection, table_name: str):
    """
    Updates Words to UPPER case in target table
    :param db_connection: connection to database
    :param table_name: Table name for insertion of words

    """
    try:
        cursor_obj = db_connection.cursor()
        update_statement = """UPDATE {} SET Word = UPPER(Word);""".format(table_name)
        cursor_obj.execute(update_statement)
        db_connection.commit()
        print("Successfully updated words to upper case")
        cursor_obj.close()

    except sqlite3.Error as error:
        print("Failed to update table:", error)


def apply_db_pipeline(db_file: str, table_name: str, word_list: [list, tuple]):
    """
    Creates SQLite Database and Reports Word Analytics
    :param db_file: database file
    :param table_name: Table name for insertion of words
    :param word_list: Dictionary word list to be added to table
    """

    db_connection = setup_connection(db_file)
    if db_connection is None:
        print("Skipping Database Operations as connection was not established")
        return
    setup_tables(db_connection, table_name)
    insert_word_records(db_connection, table_name, word_list)
    num_length_GT_5, num_has_dup_chars, num_same_start_end = run_analytics_simple(word_list)

    print("The number of words with more than 5 chars: ", num_length_GT_5)
    print("The number of words with duplicate chars: ", num_has_dup_chars)
    print("The number of words with same start and end chars: ", num_same_start_end)
    update_table_make_upper(db_connection, table_name)

    if db_connection:
        db_connection.close()
