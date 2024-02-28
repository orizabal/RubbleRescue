from dao.db import TransactionHandler
from .NeighbourDao import NeighbourDao

class NeighbourDaoImpl(NeighbourDao):
    def get_all_neighbours(self, id):
        with TransactionHandler() as cursor:
            query = f"SELECT * FROM neighbours WHERE module_id = {id};"
            cursor.execute(query)
            return cursor.fetchall()
