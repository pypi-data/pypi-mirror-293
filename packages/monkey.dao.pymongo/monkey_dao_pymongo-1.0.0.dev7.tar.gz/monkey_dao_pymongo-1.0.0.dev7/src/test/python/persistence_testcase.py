import unittest
import datetime
import os
from pymongo import MongoClient
from pymongo.database import Database
from monkey.dao.pymongo.core import PyMongoDAO, _SEQ_COLLECTION_NAME


class PersistenceTestCase(unittest.TestCase):
    COLLECTION_NAME: str = 'tests'

    connection: MongoClient
    database: Database
    dao: PyMongoDAO

    @classmethod
    def setUpClass(cls):
        print('setUpClass')
        db_name = os.environ['DB_NAME']
        connection_str = os.environ['CONNECT_STR']
        cls.connection = MongoClient(connection_str)
        cls.database = cls.connection.get_database(db_name)
        cls.dao = PyMongoDAO(cls.database, cls.COLLECTION_NAME)

    @classmethod
    def tearDownClass(cls):
        del cls.dao
        collection = cls.database[cls.COLLECTION_NAME]
        # collection.delete_many({})
        collection.drop()
        sequences = cls.database[_SEQ_COLLECTION_NAME]
        sequences.delete_one({'_id': cls.COLLECTION_NAME})
        del cls.database
        cls.connection.close()
        del cls.connection

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @staticmethod
    def _auditable_doc(cls) -> None:
        ts = datetime.datetime.utcnow()
        auditable = {'creation_date': ts, 'modification_date': ts}
        return auditable


if __name__ == '__main__':
    unittest.main()
