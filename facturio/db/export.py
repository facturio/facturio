import csv
from facturio.db.clientdao import ClientDAO
from facturio.db.companydao import CompanyDAO


def export_clients(container_folder: str = ".", file_name1: str = "Client",
    file_name2: str = "Company"):
    """
    Exporte les clients en fichiers CSV
    file name 1 -> Client
    file name 2 -> Company
    """
    cursor = ClientDAO().bdd.cursor
    dump = cursor.execute("PRAGMA table_info(Client)").fetchall()
    # On recupère seulement le nom des colones
    headers = []
    for i in range(len(dump)):
        headers.append(dump[i][1])
    cursor.execute("Select * FROM Client")
    rows = cursor.fetchall()
    with open(f"{container_folder}/{file_name1}.csv", "w") as file:
        csvWriter = csv.writer(file, delimiter=";")
        csvWriter.writerow(headers)
        for row in rows:
            csvWriter.writerow(row)
    cursor = CompanyDAO().bdd.cursor
    dump = cursor.execute("PRAGMA table_info(Company)").fetchall()
    headers = []
    for i in range(len(dump)):
        headers.append(dump[i][1])
    cursor.execute("Select * FROM Company")
    rows = cursor.fetchall()
    with open(f"{container_folder}/{file_name2}.csv", "w") as file:
        csvWriter = csv.writer(file, delimiter=";")
        csvWriter.writerow(headers)
        for row in rows:
            csvWriter.writerow(row)

if __name__ == "__main__":
    export_clients(container_folder="../data")
