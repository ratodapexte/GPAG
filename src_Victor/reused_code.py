#SERVIDOR
import psycopg2
import json
from config import config
from datetime import datetime

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
        return 'Erro!'
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.\n\n\n')
    return status

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
            print('Database connection closed.\n\n\n')
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
            conn.close()
            print('Database connection closed.\n\n\n')
    return rows

def querry_all(sql, *args):
    conn = None
    rows = None
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
            print('Database connection closed.\n\n\n')
    return rows

        
def authenticate_user(username, auth_key):
    print("##### AUTENTICANDO USUARIO #####")
    print("Dados recebidos: ", username, auth_key)
    querry = querry_one("""SELECT auth_key_init_datetime FROM users WHERE username = %s AND auth_key = %s""",
            username, auth_key)

    time_dif = datetime.now() - querry[0]
    print(time_dif.seconds)

    if time_dif.seconds < 300:
        auth_key_init_datetime = datetime.now()
        commit_querry("""UPDATE users SET auth_key_init_datetime = %s 
                        WHERE username = %s AND auth_key = %s""",
        auth_key_init_datetime, username, auth_key)
        return True
    else:
        commit_querry("""UPDATE users SET auth_key = null, auth_key_init_datetime = null 
                        WHERE username = %s""", username)
        return False


