# Migrations
Create migrations by running the `createMigrationFile` script.
```
python3 createMigrationFile.py
```

Migration file names follow this format: `<timestamp>_migraiton.sql`. This format helps ensure that database migration files don't get overwritten so we can keep track of all migrations.

> 📣 Be sure to leave a comment in the migration file explaining your changes!