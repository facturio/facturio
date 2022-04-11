#faire les liste

def selection_table(cursor,conenxion,nom):
    cursor.execute("""select * from """+nom)
    print(cursor.fetchall())
