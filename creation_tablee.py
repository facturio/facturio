
def creation_table_entreprise(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entreprise
    (id_client_entreprise INTEGER PRIMARY KEY,
    nom_entreprise STRING,
    num_SIRET INTEGER ,
    FOREIGN KEY(id_client_entreprise) REFERENCES client(id_client) ON DELETE CASCADE
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
    commentaire STRING
    )
    """)

    connexion.commit()

def creation_table_utilisateur(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS utilisateur
    ( num_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    logo BLOB,
    nom_entreprise STRING,
    courriel STRING,
    courrier STRING,
    tel STRING,
    num_SIREN STRING
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
    ( id_facdev INTEGER PRIMARY KEY AUTOINCREMENT,
    montant FLOAT,
    date INTEGER,
    description STRING,
    notes STRING,
    commentaire STRING,
    id_client INTEGER,
    id_util INTEGER,
    FOREIGN KEY(id_util) REFERENCES utilisateur(num_utilisateur),
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
    FOREIGN KEY(id_facdev) REFERENCES facture_devis(id_facdev) ON DELETE CASCADE,
    FOREIGN KEY(id_article) REFERENCES article(id_article)
    )
    """)

    connexion.commit()

def creation_table_facture(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facture
    (
    id_facture INTEGER PRIMARY KEY AUTOINCREMENT,
    solde INTEGER
    )
    """)

    connexion.commit()
def creation_table_acompte(cursor,connexion):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accompte
    (id_acompte INTEGER PRIMARY KEY AUTOINCREMENT,
    date INTEGER
    montant STRING,
    id_fac INTEGER,
    FOREIGN KEY(id_fac) REFERENCES facture(id_facture) ON DELETE CASCADE
    )
    """)
    connexion.commit()
