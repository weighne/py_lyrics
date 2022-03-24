# py_lyrics

Python script for scraping AZ lyrics using requests and some regex.

## How does this thing work??

1. Download/clone the repo (you only need the py_lyrics.py script)

2. Open up your terminal / command prompt and navigate to whatever directory you dumped the script into

3. 'S' will enter the Search function, where you can enter a band name to get a list of songs

4. After entering a band name (if the script successfully finds a corresponding AZLyrics page) it will start spitting out song names in alphabetical order

5. Entering the corresponding index number of a song will return the lyrics in plaintext and give you the opportunity to copy them to your clipboard

6. Finally, the script loops and you're back at step 3

## Some notes

All the lyrics are being pulled from [AZLyrics](azlyrics.com). While testing the script, I ran into an issue with getting temporarily IP banned from the website for making way too many requests, way too fast, so I advise to use this carefully. I apologize to AZLyrics if this violates some terms that I am not aware of, I'm just trying to have some fun with python :)

Thanks <3
