import sqlite3

def database1():
    conn=sqlite3.connect('ashwin.sqlite3')
    cur=conn.cursor()
    return conn,cur

def row_exists(value):
    """
    Checks to see if a row exists in a table

    Parameters
    ----------
    conn: sqlite3.Connection object
        connection object to the database
    table_name: str
        the name of the table in which to search for the row
    col_name: str
        the name of the column to search for the value in
    value: str
        the value to use as a key to check if a row exists
    """
    sql_cmd = 'SELECT count(*) FROM {0} WHERE {1} = "{2}"'.format('users','name', value)
    conn,cur=database1()
    cursor = conn.execute(sql_cmd)
    data = cursor.fetchone()[0]
    if data == 0:
        return(False)
    else:
        return(True)
    
def save(name,pas):
    con,cur=database1()
    cur.execute('insert into users(NAME,PASSWORD) values(?,?)',(name,pas))
    con.commit()
    con.close()
        
def login_details(username, password):

    connection,cursor =database1() 
    cursor.execute('SELECT * FROM users WHERE NAME=? AND PASSWORD=?', (username, password))
    user = cursor.fetchone()
    if user is None:
        return False
    else:
        return True
        
    
