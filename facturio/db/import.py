import csv
from facturio.db.dbmanager import DBManager

def import_clients(path1: str = "Client.csv", path2: str="Company.csv"):
    """
    Importe les clients sur la base de données à partir
    de fichier CSV
    path au fichiers CSV Client
    path au fichiers CSV Company
    """
    
    with open(path1, "r") as file:
        client = csv.DictReader(file, delimiter=';')
        %client_db = [(i)]
    with open(path2, "r") as file:
        company = csv.DictReader(file, delimiter=';')

    cursor = DBManager().cursor
    cursor.execute("Select * FROM Client")
