import csv
from facturio.db.dbmanager import DBManager
 

def export_clients(container_folder: str = ".", file_name1: str = "Client", 
    file_name2: str = "Company"):
    """
    Exporte les clients en fichiers CSV
    file name 1 -> Client
    file name 2 -> Company
    """
    cursor = DBManager().cursor
    cursor.execute("Select * FROM Client")
    rows = cursor.fetchall()
    with open(f"{container_folder}/{file_name1}.csv", "w") as file:
        csvWriter = csv.writer(file, delimiter=";")
        for row in rows:
            csvWriter.writerow(row)
    
    cursor.execute("Select * FROM Company")
    rows = cursor.fetchall()
    with open(f"{container_folder}/{file_name2}.csv", "w") as file:
        csvWriter = csv.writer(file, delimiter=";")
        for row in rows:
            csvWriter.writerow(row)
    
if __name__ == "__main__":
    export_clients(container_folder="../data")
