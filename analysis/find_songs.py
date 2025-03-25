# This is to pull in all the data and

import pandas as pd
import psycopg2
import time
import datetime

start_time = time.time()
# python framework for postgres used from internet (next 9 lines)
try:
    songs_to_find = ['Wading in the Velvet Sea','Gumbo','Possum']

    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="joe",
        password=""
    )
    #Still todo:
        # points for each song to sum up for all the favorite song
        # 2025-03-22 (discovered) Some songs appear in the same show more than once
        # 2025-03-24 performance must be looked at.
        # - 2 songs to find ~ 100 sec on M2 Macbook Pro

#logic my own
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM setlists")
    myresult = cursor.fetchall()
    max_count = [0] * len(songs_to_find)
    counter = [0] * len(songs_to_find)
    max_total_count = 0
    best_week_start = [""] * len(songs_to_find)
    best_week_end = [""] * len(songs_to_find)
    for x in myresult:
        date_1 = datetime.datetime.strptime(str(x[7]), "%Y-%m-%d")
        show_date = str(x[7])
        end_date = date_1 + datetime.timedelta(days=7)

        # count songs per date window
        str_sql = "SELECT song_name, show_date FROM setlists WHERE show_date "
        str_sql += "BETWEEN '" + show_date + "' AND '" + str(end_date) + "'"
        str_sql += "group by song_name ,show_date"
        # the group by is necessary as the same song can show up more than once
        # in the same show
        cursor.execute(str_sql)
        myresult1 = cursor.fetchall()

        start_week = show_date
        end_week = end_date
        for i in range(0,len(songs_to_find)):
            counter[i] = 0
        for y in myresult1:
            if y[0] in songs_to_find:
                for i in range(0,len(songs_to_find)):
                    if y[0] == songs_to_find[i]:
                        counter[i] += 1
                        if sum(counter) > max_total_count:
                            max_total_count = sum(counter)
                            best_week_start[i] = start_week
                            best_week_end[i] = end_week
                            print("new max_total_count="+str(max_total_count))
                            print("new week_start="+str(best_week_start[i]))
                            print("new week_end="+str(best_week_end[i]))

# framework for postgres taken from internet (next 7 lines)
except psycopg2.Error as e:
    print(f"Error interacting with PostgreSQL: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

end_time = time.time()
print("execution time "+str(end_time - start_time))