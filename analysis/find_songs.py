# This is to pull in all the data and

import pandas as pd
import psycopg2
import time
import datetime

try:
    songs_to_find = ['Bathtub Gin','Tweezer']

    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="joe",
        password=""
    )
    #Still todo:
        # points for each song to sum up for all the favorite song
        # 2025-03-22 (discovered) Some songs appear in the same show more than once


    cursor = connection.cursor()
    cursor.execute("SELECT * FROM setlists")
    myresult = cursor.fetchall()
    max_count = [0] * len(songs_to_find)
    counter = [0] * len(songs_to_find)
    best_week_start = [""] * len(songs_to_find)
    best_week_end = [""] * len(songs_to_find)
    for x in myresult:
        date_1 = datetime.datetime.strptime(str(x[7]), "%Y-%m-%d")
        show_date = str(x[7])
        end_date = date_1 + datetime.timedelta(days=7)

        # count songs per date window
        str_sql="SELECT song_name FROM setlists WHERE show_date BETWEEN '"
        str_sql += show_date + "' AND '" + str(end_date) + "'"
        cursor.execute(str_sql)
        myresult1 = cursor.fetchall()

        start_week = show_date
        end_week = end_date
        for i in range(0,len(songs_to_find)):
            counter[i] = 0
        for y in myresult1:
            if (y[0] in songs_to_find):
                for i in range(0,len(songs_to_find)):
                    if (y[0] == songs_to_find[i]):
                        counter[i] += 1
                        if counter[i] > max_count[i]:
                            max_count[i] = counter[i]
                            best_week_start[i] = start_week
                            best_week_end[i] = end_week
                            print("new max_counter="+str(max_count[i]))
                            print("new song_name="+str(y[0]))
                            print("new week_start="+str(best_week_start[i]))
                            print("new week_end="+str(best_week_end[i]))

except psycopg2.Error as e:
    print(f"Error interacting with PostgreSQL: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

