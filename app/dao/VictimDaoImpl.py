
from .VictimDao import VictimDao
from dao.db import TransactionHandler
from models import Victim

class VictimDaoImpl(VictimDao):
    def find_by_id(self, id):
        with TransactionHandler() as cursor:
            query = f"SELECT * FROM victims WHERE id = {id};"
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                return None
            else:
                return result[0]

    def get_all(self):
        with TransactionHandler() as cursor:
            query = "SELECT * FROM victims;"
            cursor.execute(query)
            return cursor.fetchall()

    def insert(self, victim: Victim):
        with TransactionHandler() as cursor:
            query = "INSERT INTO victims (x_coordinate, y_coordinate, true_positive, location_checked) VALUES (?, ?, ?, ?);"
            # TODO: try catch
            cursor.execute(query, (victim.xCoordinate, victim.yCoordinate, victim.truePositive, victim.locationChecked))
            return cursor.lastrowid

    def update(self, victim: Victim):
        # Confirm that the victim exists
        if self.find_by_id(victim.id) is None:
            print(f"ERROR: Victim {victim.id} does not exist in the database and cannot be updated.")
            return None
        else:
            with TransactionHandler() as cursor:
                query = "UPDATE victims SET x_coordinate = ?, y_coordinate = ?, true_positive = ?, location_checked = ? WHERE id = ?;"
                # TODO: try catch
                cursor.execute(query, (victim.xCoordinate, victim.yCoordinate, victim.truePositive, victim.locationChecked))

    def delete(self, victim: Victim):
        # Confirm that the victim exists
        if self.find_by_id(victim.id) is None:
            print(f"ERROR: Victim {victim.id} does not exist in the database and cannot be deleted.")
            return None
        else:
            with TransactionHandler() as cursor:
                query = f"DELETE FROM victims WHERE id = {victim.id};"
                # TODO: try catch
                cursor.execute(query)
