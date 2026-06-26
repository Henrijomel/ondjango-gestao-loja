# repositories/base_repository.py
import mysql.connector
from mysql.connector import Error

class BaseRepository:
    def __init__(self, connection):
        self.connection = connection

    def create(self, entity):
        raise NotImplementedError

    def read(self, entity_id):
        raise NotImplementedError

    def update(self, entity):
        raise NotImplementedError

    def delete(self, entity_id):
        raise NotImplementedError
