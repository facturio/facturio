def delete_table(cursor,connexion,name,id):
    cursor.execute(""" DELETE FROM"""+name+""" WHERE id_"""+name+"""="""+str(id))
    connexion.commit()
