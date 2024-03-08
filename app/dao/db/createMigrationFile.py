import os
import time

# File name format: <timestamp>_migration.sql
def main():
    # make the file name
    timestamp = str(int(time.time()))
    fileName = timestamp + "_migration.sql"
    
    # get the target path
    cwd = os.getcwd()
    migrationDir = "dao/db/migrations/"
    targetPath = os.path.join(cwd, migrationDir)

    # check if file already exists before creating
    migrationFile = os.path.join(targetPath, fileName)

    if not os.path.exists(migrationFile):
        try:
            open(migrationFile, 'w+').close()
            print(f"Success! Created migration file: {fileName}")
        except OSError:
             print(f"ERROR: {OSError}")
        except:
            print("ERROR: Could not create migration file.")
    else:
        print("ERROR: Could not create migration file, file already exists.")


if __name__ == "__main__":
    main()
