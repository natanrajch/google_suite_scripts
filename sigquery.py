import mysql.connector
from mysql.connector import errorcode
import mysql.connector

def conexion():
    try:
        cnx = mysql.connector.connect(user='user', password='pass',
                                    host='host ip',
                                    database='database name')
        #print(cnx)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx

def query_a_sig(query_string):
    """Recibe un string de SQL, lo ejecuta contra la base local del SIG con perfil de user. Devuelve una list of lists"""
    cnx = conexion()

    mycursor = cnx.cursor()

    mycursor.execute(query_string)


    myresult = mycursor.fetchall() #Devuelve una lista de Tuples
    myresult = [[str(it) for it in list(row)] for row in myresult] #Convierte a una list of lists, que es lo que pide Sheets API
    #print(myresult)
    # for x in myresult:
    #   print(x)

    cnx.close()
    return myresult
# query_a_sig()

