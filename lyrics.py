import requests
import json
import re
import string
import random
from time import sleep
import pyperclip as pclip

songlist_url = "https://www.azlyrics.com/{}/{}.html"
lyrics_url = "https://www.azlyrics.com/lyrics/{}/{}.html"


def cls():  # clear da screen
    input('Press any key to continue...')
    if name == 'nt':  # for windows
        _ = system('cls')
    else:  # for mac and linux(here, os.name is 'posix')
        _ = system('clear')


def print_list_in_sections(list, length=10):
    for x in range(len(list)):
        if x%length != 0 or x == 0:
            print(f"{x} - {list[x]}")
        elif x%length == 0 and x != 0:
            print(f"{x} - {list[x]}")
            cont = input("\nEnter \'q\' to stop...\n\'Enter\' key to continue...\nInput song index to get lyrics\nInput: ")
            if cont.lower() == 'q':
                break
            elif cont.isdigit() and int(cont) <= len(list):
                return cont
            else:
                continue
        else:
            print(f"Error with following index: {x}")


def check_band_page(page, band_name_input):  # check that requests actually finds a page with lyrics results
    re_pattern = "(<title>.*?</title>)"
    re_pattern2 = "(<title>|</title>)"
    title = re.findall(re_pattern, page)

    for x in range(len(title)):
        title[x] = re.sub(re_pattern2,'',title[x])

    for x in title:  # it shouldn't ever find more than one title, but if it does...
        if "AZLyrics - Song Lyrics from A to Z" in title:
            return False
            break
        else:
            return True
            break
    return False


def get_lyrics(page):
    # print(page.text)
    re_pattern = "<!-- U([\w\W]*?)<\/div>"
    re_pattern2 = r"<!--.*?-->"
    re_pattern3 = r"<br>|</div>|.*?-->"

    lyrics = re.findall(re_pattern, page.text)
    # lyrics = re.sub(re_pattern2,'',lyrics[0])
    lyrics = re.sub(re_pattern3,'',lyrics[0])
    lyrics = re.sub("&quot;","\"",lyrics)

    print(lyrics)

    copy = input("\'C\' to copy lyrics to clipboard\n\'Enter\' to continue\nInput: ")
    if copy.lower() != 'c':
        print('Resetting...\n\n')
    else:
        pclip.copy(lyrics)
        print("Lyrics copied to clipboard!\n\nResetting...")


if __name__ == "__main__":
    u_session = requests.session()
    function = 'S'

    while function.lower() != 'q':
        cls()
        sleep(2)  # to avoid the silly bot ban
        function = input("\'S\' to search\n\'Q\' to quit\nInput:")
        if function.lower() == 'q':
            break
        else:
            band_name_input = input("Enter Band Name: ")
            band_name = band_name_input.lower().strip().replace(" ","")
            band_page = u_session.get(songlist_url.format(band_name[0],band_name))

            if check_band_page(band_page.text, band_name_input) == True:
                # print("That's a real page!")
                re_pattern = '(s:\".*?\")'
                lyrics_list = re.findall(re_pattern, band_page.text)
                lyrics_list_formatted = [x.split(":")[1].replace("\"","") for x in lyrics_list]
                lyrics_list_nonhuman = [re.sub(r'[^\w_]', '', x).lower() for x in lyrics_list_formatted]

                song_index = print_list_in_sections(lyrics_list_formatted)
                # print(lyrics_url.format(band_name,lyrics_list_nonhuman[int(song_index)]))

                lyrics_page = u_session.get(lyrics_url.format(band_name,lyrics_list_nonhuman[int(song_index)]))
                # u_session.close()
                # print(lyrics_page.text)
                # with open("lyrics_dump.txt","w") as out_file:
                #     out_file.write(lyrics_page.text)
                get_lyrics(lyrics_page)
                #do some stuff
            else:
                print("Goodbye!")
