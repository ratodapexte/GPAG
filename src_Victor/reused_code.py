#SERVIDOR
import psycopg2
from config import config

def commit_querry(sql, *args):
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
        
   # execute a statement
        print('Running querry:')
        cur.execute(sql, args)
        status = cur.statusmessage
        conn.commit()
        # display the last Querry status    
        print("Querry status: ", cur.statusmessage)
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return status.encode()
        return None

def querry_one(sql, *args):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        print('Params: ',params)
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('Running querry:')
        cur.execute(sql, args)
        row = cur.fetchone()

        # display the last Querry status    
        print("Querry status: ", cur.statusmessage)
        
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return row

def querry_many(sql, size, *args):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('Running querry:')
        cur.execute(sql, args)
        rows = cur.fetchmany(size)

        # display the last Querry status    
        print("Querry status: ", cur.statusmessage)
        
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            if rows is None:
                return None
            else:
                return rows
        return None

def querry_all(sql, *args):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('Running querry:')
        cur.execute(sql, args)
        rows = cur.fetchall()
        

        # display the last Querry status    
        print("Querry status: ", cur.statusmessage)
        
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return rows
        return None
        

def authenticate_user(tcp, login, auth_key):
    tcp.send(json.dumps({'command': 'authenticate_user', 'login': login, 'auth_key': auth_key}).encode())
    result = tcp.recv(1024).decode()
    if result = 'true':
        return True
    else:
        return False
























