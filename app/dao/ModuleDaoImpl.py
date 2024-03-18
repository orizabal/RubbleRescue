from .ModuleDao import ModuleDao
from dao.db import TransactionHandler
from models import Module

class ModuleDaoImpl(ModuleDao):
    def find_by_id(self, id):
        with TransactionHandler() as cursor:
            query = f"SELECT * FROM modules WHERE id = {id};"
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                return None
            else:
                return result[0]


    def get_all(self):
        with TransactionHandler() as cursor:
            query = "SELECT * FROM modules;"
            cursor.execute(query)
            return cursor.fetchall()


    def insert(self, module: Module):
        with TransactionHandler() as cursor:
            query = "INSERT INTO modules (reference_point, x_coordinate, y_coordinate) VALUES (?, ?, ?);"
            cursor.execute(query, (module.referencePoint, module.xCoordinate, module.yCoordinate))
            return cursor.lastrowid


    def update(self, module: Module):
        # Confirm that module exists
        if self.find_by_id(module.id) is None:
            print (f"ERROR: Module {module.id} does not exist in the database and cannot be updated.")
            return None
        else:
            with TransactionHandler() as cursor:
                query = "UPDATE modules SET reference_point = ?, x_coordinate = ?, y_coordinate = ? WHERE id = ?;"
                # TODO: try catch
                cursor.execute(query, (module.referencePoint, module.xCoordinate, module.yCoordinate, module.id))


    def delete(self, module: Module):
        # Confirm that module exists
        if self.find_by_id(module.id) is None:
            print (f"ERROR: Module {module.id} does not exist in the database and cannot be deleted.")
            return None
        else:
            with TransactionHandler() as cursor:
                query = f"DELETE FROM modules WHERE id = {module.id};"
                # TODO: try catch
                cursor.execute(query)
