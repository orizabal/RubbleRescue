from .AudioItemDao import AudioItemDao
from dao.db import TransactionHandler
from models import AudioItem

class AudioItemDaoImpl(AudioItemDao):
    def find_by_id(self, id):
        with TransactionHandler() as cursor:
            query = f"SELECT * FROM audio_items WHERE id = {id};"
            cursor.execute(query)
            result = cursor.fetchall()
            if not result:
                return None
            else:
                return result[0]

    def get_all(self):
        with TransactionHandler() as cursor:
            query = "SELECT * FROM audio_items;"
            cursor.execute(query)
            return cursor.fetchall()

    def insert(self, audioItem: AudioItem):
        with TransactionHandler() as cursor:
            query = "INSERT INTO audio_items (module_id, victim_id, recorded_at, ref) VALUES (?, ?, ?, ?);"
            # TODO: try catch
            cursor.execute(query, (audioItem.moduleId, audioItem.victimId, audioItem.recordedAt, audioItem.ref))

    def update(self, audioItem: AudioItem):
        # Confirm that the audio item exists
        if self.find_by_id(audioItem.id) is None:
            print(f"ERROR: Audio Item {audioItem.id} does not exist in the database and cannot be updated.")
            return None
        else:
            with TransactionHandler() as cursor:
                query = "UPDATE audio_items SET module_id = ?, victim_id = ?, recorded_at = ?, ref = ? WHERE id = ?;"
                # TODO: try catch
                cursor.execute(query, (audioItem.moduleId, audioItem.victimId, audioItem.recordedAt, audioItem.ref, audioItem.id))


    def delete(self, audioItem: AudioItem):
        with TransactionHandler() as cursor:
            # Confirm that the audio item exists
            if self.find_by_id(audioItem.id) is None:
                print(f"ERROR: Audio Item {audioItem.id} does not exist in the database and cannot be deleted.")
                return None
            else:
                query = f"DELETE FROM audio_items WHERE id = {audioItem.id};"
                cursor.execute(query)
