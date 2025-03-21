# This is to pull in all the data and

import pandas as pd
import psycopg2
import time
import datetime

try:
    # fill in your stuff here to update to postgres.
    # If you don't like postgres, this script can be
    # easily modified.
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="joe",
        password=""
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM setlists")

    myresult = cursor.fetchall()


    for x in myresult:
        date_1 = datetime.datetime.strptime(str(x[7]), "%Y-%m-%d")
        show_date = str(x[7])
        end_date = date_1 + datetime.timedelta(days=10)
        # count songs per date window
        for i in range(1, 105):
            str_sql="SELECT song_name FROM setlists WHERE show_date BETWEEN '"
            str_sql += show_date + "' AND '" + str(end_date) + "'"
            cursor.execute(str_sql)
            myresult = cursor.fetchall()
        print(str(date_1) +"-"+ str(end_date))

except psycopg2.Error as e:
    print(f"Error interacting with PostgreSQL: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

