# Transactions
Transactions and transaction handlers are crucial for managing data integrity and consistency, especially when dealing with relational databases.
- Transactions ensure that database operations are atomic, so they either all succeed or all fail
- Transactions provide isolation guarantees - they ensure that database operations do not interfere with each other, ensuring the database remains in a consistent state at all times
- Transaction logic is encapsulated to ensure that data operations are performed within transaction boundaries
- Transaction handlers abstract away transaction management details from the service layer
- Transaction handlers handle exceptions that may occur during database operations. If an exception occurs, the transaction is rolled back to ensure that no partial changes are committed to the db

### Usage Example
```
with TransactionHandler() as cursor:
    cursor.execute("INSERT INTO victims (x_coordinate, y_coordinate) VALUES (45.444, 13.352);")
    cursor.execute("INSERT INTO neighbours (module_id, neighbour_module_id) VALUES (3, 1);")
```
The `with` statement is used to create a context handled by the `TransactionHandler`. Within this context, database operations are performed using the curser object obtained from the `TransactionHandler`.

# Migrations
Create migrations by running the `createMigrationFile` script.
```
python3 createMigrationFile.py
```

Migration file names follow this format: `<timestamp>_migraiton.sql`. This format helps ensure that database migration files don't get overwritten so we can keep track of all migrations.

> 📣 Be sure to leave a comment in the migration file explaining your changes!