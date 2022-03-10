import requests
import json
import re
import string
import random
from time import sleep
from bs4 import BeautifulSoup

songlist_url = "https://www.azlyrics.com/{}/{}.html"
lyrics_url = "https://www.azlyrics.com/lyrics/{}/{}.html"
agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0'
headers = {'User-Agent': agent}
proxy_list = ["http://130.185.119.20:3128","http://99.71.86.199:8118"]


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
    re_pattern = r"<!-- U([\w\W]*?)<\/div>"
    re_pattern2 = r"<!--.*?-->"
    re_pattern3 = r"<br>|</div>|.*?-->"

    lyrics = re.findall(re_pattern, page.text)
    # lyrics = re.sub(re_pattern2,'',lyrics[0])
    lyrics = re.sub(re_pattern3,'',lyrics[0])
    lyrics = re.sub("&quot;","\"",lyrics[0])

    print(lyrics)


if __name__ == "__main__":
    u_session = requests.session()
    # proxy_choice = random.randint(1,len(proxy_list)-1)
    # proxies = {"http":proxy_list[proxy_choice],"https":proxy_list[proxy_choice]}
    y=0
    while y <= 10:
        proxy_choice = random.randint(1,len(proxy_list)-1)
        proxies = {"http":proxy_list[proxy_choice],"https":proxy_list[proxy_choice]}
        print(proxies)
        sleep(2)
        # band_name_input = input("Enter Band Name: ")
        band_name_input = "modest mouse"
        band_name = "modestmouse"
        # band_name = band_name_input.lower().strip().replace(" ","")
        band_page = u_session.get(songlist_url.format(band_name[0],band_name), headers=headers,proxies=proxies)
        print(band_page.text)

        if check_band_page(band_page.text, band_name_input) == True:
            # print("That's a real page!")
            re_pattern = '(s:\".*?\")'
            lyrics_list = re.findall(re_pattern, band_page.text)
            lyrics_list_formatted = [x.split(":")[1].replace("\"","") for x in lyrics_list]
            lyrics_list_nonhuman = [re.sub(r'[^\w_]', '', x).lower() for x in lyrics_list_formatted]

            # song_index = print_list_in_sections(lyrics_list_formatted)
            song_index = 12 # random.randint(1,100)

            lyrics_page = u_session.get(lyrics_url.format(band_name,lyrics_list_nonhuman[int(song_index)]), headers=headers,proxies=proxies)
            u_session.close()
            # print(lyrics_page.text)
            with open("lyrics_dump.txt","w") as out_file:
                out_file.write(lyrics_page.text)
            get_lyrics(lyrics_page)
            #do some stuff
        else:
            print("Goodbye!")
        y+=1


# print(band_page)
#
# soup = BeautifulSoup(band_page.text, 'html.parser')
#
# print(soup)
#
# # re_pattern = f'lyrics/{band_name}/.*?.html\"'
# re_pattern = '(s:\".*?\")'
#
# #soup.find('div',text=f"lyrics/{band_name}/.*?.html\"")
#
# lyrics_list = re.findall(re_pattern, band_page.text)
#
# # lyrics_list_formatted = [x.split("/")[2].replace(".html\"","") for x in lyrics_list]
# lyrics_list_formatted = [x.split(":")[1].replace("\"","") for x in lyrics_list]
# lyrics_list_nonhuman = [re.sub(r'[^\w_]', '', x).lower() for x in lyrics_list_formatted]
#
# # for x in lyrics_list:
# #     print(x)
#
# song_index = print_list_in_sections(lyrics_list_formatted)
#
# print(song_index)
# print(lyrics_list_nonhuman[int(song_index)])
#
# lyrics_page = requests.get(lyrics_url.format(band_name,lyrics_list_nonhuman[int(song_index)]))
# print(lyrics_page.text)

# for x in lyrics_list_nonhuman:
#     print(x)
