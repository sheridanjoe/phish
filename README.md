# phish
joe's phish project for datamining at the osu

This purpose of this project is to find relationships, et. al. on phish setlist data.
The data was obtained from setlist.fm.

Files:
- /data/* <- these are the actual data in a nice csv for easy consumption
- /dataload/* <- if you want to pull the data or load it yourself, here are the files I used to do that
- /analysis/
  - find_songs.py <- Given a set of songs, find the week where the songs were played the most
    - for example: if you wanted to know the week that they played the most "Tweezer" and "Gumbo", you add that to the songs to look for and it will tell you which week in history has the most count of those songs.  It's not intelligent in that if it finds 10 "Tweezer" and no "Gumbo" it will report the value as 10 and probably win. (10 instances of a single song in a week are very unlikely, but you get the point.)
    -  Some shows have more than one instance of the same song in the same show.  For example it could go "Tweezer" -> "Gumbo" -> "Tweezer", it will only record the first Tweezer for that show.
