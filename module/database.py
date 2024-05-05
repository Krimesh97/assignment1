import sqlite3


def setup_db(db_file, table_name):
    """
    create a database connection to a SQLite database
    :param db_file: database file
    :param table_name: Table name for insertion of words
    """
    db_connection = None
    try:
        db_connection = sqlite3.connect(db_file)
        print("Connection to db successful:", sqlite3.version)

        # cursor object
        cursor_obj = db_connection.cursor()

        # Drop the GEEK table if already exists.
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
    finally:
        if db_connection:
            db_connection.close()


def insert_word_records(db_file, table_name, word_list):
    """
    Insert Word Records into table
    :param db_file: database file
    :param table_name: Table name for insertion of words
    :param word_list: Dictionary word list to be added to table
    """
    db_connection = None
    try:
        db_connection = sqlite3.connect(db_file)
        cursor_obj = db_connection.cursor()
        # print("Connected to SQLite")

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
    finally:
        if db_connection:
            db_connection.close()
            print("The SQLite connection is closed")



def apply_db_pipeline(db_file: str, table_name: str, word_list: [list, tuple]):
    """
    Creates SQLite Database and Reports Word Analytics
    :param db_file: database file
    :param table_name: Table name for insertion of words
    :param word_list: Dictionary word list to be added to table
    """
    setup_db(db_file, table_name)
    insert_word_records(db_file, table_name, word_list)
