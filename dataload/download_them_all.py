import requests, time

# change this to be your batch size for calls.  75 is way too high for Phish!
for i in range(1, 75):
    # This sleep is very important!  If you don't space out your calls, they will
    # get blocked for too many requests.
    time.sleep(30)
    # phish = e01646f2-2a04-450d-8bf2-0d993082e058
    url = "https://api.setlist.fm/rest/1.0/artist/e01646f2-2a04-450d-8bf2-0d993082e058/setlists?p=" + str(i)

    headers = {
        "Accept": "application/json",
        # get your api key from setlist.fm
        "x-api-key": "XXXXXXXXXX"
    }

    response = requests.request("GET", url, headers=headers)

    # This is for debugging
    #print(response.content)

    # You can output these anywhere you want.  Read in the jSON you capture here with
    # read_events.py
    f = open("./output/phish_setlists_"+str(i)+".txt", "w")
    f.write(response.content.decode('utf-8'))
    f.close()
