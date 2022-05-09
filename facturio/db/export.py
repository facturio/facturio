import csv
from facturio.db.clientdao import ClientDAO
from facturio.db.companydao import CompanyDAO
from facturio.classes.client import Client, Company


def export_clients(container_folder: str = ".", file_name1: str = "Client",
    file_name2: str = "Company"):
    """
    Exporte les clients en fichiers CSV
    file name 1 -> Client
    file name 2 -> Company
    """
    headers = ["id_client", "first_name", "last_name", "e_mail", "address",
    "phone", "remark" ]
    cursor = ClientDAO().bdd.cursor
    cursor.execute("Select * FROM Client")
    rows = cursor.fetchall()
    print(rows)
    with open(f"{container_folder}/{file_name1}.csv", "w") as file:
        csvWriter = csv.writer(file, delimiter=";")
        csvWriter.writerow(headers)
        for row in rows:
            csvWriter.writerow(row)
    headers = ["id_company", "company_name","business_num"]
    cursor = CompanyDAO().bdd.cursor
    cursor.execute("Select * FROM Company")
    rows = cursor.fetchall()
    print(rows)
    with open(f"{container_folder}/{file_name2}.csv", "w") as file:
        csvWriter = csv.writer(file, delimiter=";")
        csvWriter.writerow(headers)
        for row in rows:
            csvWriter.writerow(row)

if __name__ == "__main__":


    client_physique = Client(
        "Quentin", "Lombardo",
        None, "HLM Sainte-Muse Toulon", "0678905324",
        note="Personne peu sympathique"
        )
    print(client_physique.dump_to_list())

    client_moral = Company(
            "LeRoy", "Ben", "Karim", "287489404", "LeRoy83@sfr.fr",
            "12 ZAC de La Crau", "0345678910", note="Investisseur important",

        )
    ClientDAO().insert(client_physique)
    CompanyDAO().insert(client_moral)
    export_clients(container_folder="../data")
