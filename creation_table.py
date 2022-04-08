
def creation_table_entreprise(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entreprise
    (id_client_entreprise INTEGER PRIMARY KEY,
    nom_entreprise STRING,
    num_SIRET INTEGER ,
    FOREIGN KEY(id_client_entreprise) REFERENCES client(id_client)
    )
    """)

    connexion.commit()

def creation_table_client(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS client
    (id_client INTEGER PRIMARY KEY,
    nom  STRING,
    prenom STRING,
    courriel STRING,
    courrier STRING,
    tel STRING,
    commentaire STRING,
    nom_entreprise STRING,
    num_SIRET INTEGER
    )
    """)

    connexion.commit()

def creation_table_utilisateur(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilisateur
    ( num_tilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    logo BLOB
    nom_entreprise STRING,
    courriel STRING,
    courrier STRING,
    tel STRING,
    num_SIREN STRING
    )
    """)
    connexion.commit()



def creation_table_acompte(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accompte
    (id_acompte INTEGER PRIMARY KEY,
    date INTEGER
    montant STRING,
    id_fac INTEGER,
    FOREIGN KEY(id_fac) REFERENCES fac(id_fac)
    )
    """)
    connexion.commit()

def creation_table_article(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS article
    ( id_article INTEGER PRIMARY KEY AUTOINCREMENT,
    nom STRING,
    description STRING,
    prix float
    )
    """)

    connexion.commit()

def creation_table_facture_devis(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facture_devis
    ( id_facdev INTEGER PRIMARY KEY,
    montant FLOAT,
    date INTEGER,
    description STRING,
    notes STRING
    commentaire STRING
    id_client INTEGER,
    id_util INTEGER,

    FOREIGN KEY(id_util) REFERENCES utilisateur(id_util)
    )
    """)

    connexion.commit()

def creation_table_art_dev(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS art_dev
    (
    id_article INTEGER,
    id_facdev STRING,
    FOREIGN KEY(id_facdev) REFERENCES facture_devis(id_facdev),
    FOREIGN KEY(id_article) REFERENCES article(id_article)
    )
    """)

    connexion.commit()

def creation_table_facture(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facture
    (
    id_facture INTEGER,
    solde INTEGER
    )
    """)

    connexion.commit()
