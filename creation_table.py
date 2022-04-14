
def creation_table_company(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company
    (id_client_company INTEGER PRIMARY KEY,
    company_name STRING,
    num_SIRET INTEGER ,
    FOREIGN KEY(id_client_company) REFERENCES client(id_client) ON DELETE CASCADE
    )
    """)

    connexion.commit()

def creation_table_client(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client
    (id_client INTEGER PRIMARY KEY,
    last_name STRING,
    first_name STRING,
    e_mail STRING,
    address STRING,
    phone STRING,
    remark STRING
    )
    """)

    connexion.commit()

def creation_table_user(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user
    ( id_user INTEGER PRIMARY KEY AUTOINCREMENT,
    logo BLOB,
    company_name STRING,
    e_mail STRING,
    address STRING,
    phone STRING,
    num_SIREN STRING
    )
    """)
    connexion.commit()





def creation_table_article(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS article
    ( id_article INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING,
    description STRING,
    price float
    )
    """)

    connexion.commit()

def creation_table_invoice_devis(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice_devis
    ( id_facdev INTEGER PRIMARY KEY AUTOINCREMENT,
    amount FLOAT,
    date INTEGER,
    description STRING,
    note STRING,
    remark STRING,
    id_client INTEGER,
    id_util INTEGER,
    FOREIGN KEY(id_util) REFERENCES user(id_user),
    FOREIGN KEY(id_client) REFERENCES client(id_client) ON DELETE CASCADE
    )
    """)

    connexion.commit()

def creation_table_art_dev(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS art_dev
    (
    id_article INTEGER,
    id_facdev INTEGER,
    FOREIGN KEY(id_facdev) REFERENCES invoice_devis(id_facdev) ON DELETE CASCADE,
    FOREIGN KEY(id_article) REFERENCES article(id_article)
    )
    """)

    connexion.commit()

def creation_table_invoice(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice
    (
    id_invoice INTEGER PRIMARY KEY AUTOINCREMENT,
    solde INTEGER
    )
    """)

    connexion.commit()
def creation_table_deposit(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS deposit
    (id_deposit INTEGER PRIMARY KEY AUTOINCREMENT,
    date INTEGER,
    amount STRING,
    id_fac INTEGER,
    FOREIGN KEY(id_fac) REFERENCES invoice(id_invoice) ON DELETE CASCADE
    )
    """)
    connexion.commit()
