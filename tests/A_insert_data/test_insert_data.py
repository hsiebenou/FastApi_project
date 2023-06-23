import os
from sqlalchemy import create_engine
from conf_test_db import logger, connection_string


def insert_data_in_bdd():
    """

    :return:
    """
    logger.info("insert the reference data")
    # connect to de database and insert the necessary element for unit test
    cnx = create_engine(connection_string)

    # We import required data for our unit tests
    with open(
        os.path.join(os.path.dirname(__file__), "unit_tests_data.sql"),
        "rb"
    ) as file:
        files_read = file.read()

    sql_statements = files_read.decode("latin-1").split(";")

    for query in sql_statements:
        if query == "":
            continue
        cnx.execute(query)

    return "all data has been inserted !"


def test_insert():
    result = insert_data_in_bdd()
    assert result == "all data has been inserted !"
