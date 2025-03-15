import json
import psycopg2

def load_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

try:
    # fill in your stuff here to update to postgres.
    # If you don't like postgres, this script can be
    # easily modified.
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="XXXXX",
        password="YYYYY"
    )
    cursor = connection.cursor()

    for i in range(1, 105):
        json_obj = load_json('output/phish_setlists_'+str(i)+'.txt')
        for setlist in json_obj["setlist"]:
            venue_name = setlist["venue"]["name"]
            venue_city = setlist["venue"]["city"]["name"]
            venue_state = setlist["venue"]["city"]["stateCode"]
            setlist_date = setlist["eventDate"]
            tour_name = "unk"
            # some tours have names, some don't
            if "tour" in setlist:
                tour_name = setlist["tour"]["name"]
            else:
                tour_name = "unk"
            for set_item in setlist["sets"]["set"]:
                for song_item in set_item["song"]:
                    song_name = song_item["name"]
                    # some songs are covers, so we capture that here
                    song_cover = ""
                    if "cover" in song_item:
                        if "name" in song_item["cover"]:
                            song_cover = song_item["cover"]["name"]
                        else:
                            song_cover = ""
                    # this is a little primitive, but it gets the job done.
                    str_sql="INSERT INTO public.setlists "
                    str_sql += "( venue_name, venue_city, venue_state_code, "
                    str_sql += "song_name, song_cover, tour_name, show_date) "
                    str_sql += "VALUES( %s, %s, %s, %s, %s, %s, to_date('"
                    str_sql += setlist_date + "','DD-MM-YYYY'));"
                    data = (venue_name, venue_city, venue_state, song_name, song_cover, tour_name)

                    cursor.execute(str_sql, data)
                    connection.commit()

except psycopg2.Error as e:
    print(f"Error interacting with PostgreSQL: {e}")
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


#phish = e01646f2-2a04-450d-8bf2-0d993082e058
