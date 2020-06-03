from scrapy import Spider, Request
from scrapy.selector import Selector
from lyricsScraper.items import LyricsscraperItem
from w3lib.html import remove_tags
from mtranslate import translate
import string
import re


## Global Variable Decleration ##
removepunc = string.punctuation.replace(".","").replace(",", "").replace("/", "")
translation_dict = {}

def translate_word(word):
    translated = translate(word, 'si', 'en')
    return translated

def translate_array(wordlist):
    translated_array = []
    for i in wordlist :
        if i in translation_dict.keys() :
            translated_array.append(translation_dict.get(i))
        else :
            translated_phrase = translate_word(i)
            translation_dict[i] = translated_phrase
            translated_array.append(translated_phrase)
    return translated_array

class LyricsSpider(Spider):
    name = "sinhalasongbook"
    allowed_domains = ["sinhalasongbook.com"]
    start_urls = [
        "https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=" + str(i) for i in range(1,3)
    ]

    def parse(self,response):
        responseSelector = Selector(response)
        urls = responseSelector.xpath('//*[@id="pt-cv-view-9c94ff8o8i"]//a/@href')
        for i in urls :
            songurl = i.extract()
            yield Request(songurl, callback=self.parse_songdata)

    def parse_songdata(self, response):
        responseSelector = Selector(response)
        item = LyricsscraperItem()


        ## Non Translated data
        songLyricswithExtra = remove_tags(responseSelector
                                          .xpath('//*[@id="genesis-content"]/article/*[@class="entry-content"]//pre')[0].extract())
        songLyrics = "".join([char for char in songLyricswithExtra
                              if ( ( char not in string.digits ) and (char not in string.ascii_letters) and (char not in removepunc )) ]).strip()
        songLyrics = songLyrics.replace("∆","")
        item["songLyrics"] = songLyrics

        songLyrics = songLyrics.replace("\n", "")
        songLyrics = songLyrics.replace("\t", "")
        songLyrics = "".join([char for char in songLyrics if (  (char not in string.punctuation )) ]).strip()
        item["songLyricsSearchable"] = songLyrics

        string_viewcount_data = remove_tags(responseSelector.xpath('//*[@class="tptn_counter"]')[0].extract())
        string_viewcount = re.sub('[^0-9,]',"",string_viewcount_data).repace(',','')
        viewcount = int(string_viewcount.replace(",",""))
        item["views"] = viewcount

        string_sharecount_data = remove_tags(responseSelector.xpath('//*[@class="swp_count"]')[0].extract())
        string_sharecount = re.sub('[^0-9,]',"",string_sharecount_data).repace(',','')
        sharecount = int(string_sharecount)
        item["shares"] = sharecount

        titlestring = remove_tags(responseSelector.xpath('//*[@id="genesis-content"]/article/*[@class="entry-content"]/h2')[0].extract())
        if("-" in titlestring):
            titles = titlestring.split("-")
            titles = [i.strip() for i in titles]
            item["title"] = titles[1]
        elif("|" in titlestring):
            titles = titlestring.split("|")
            titles = [i.strip() for i in titles]
            item["title"] = titles[1]
        elif("–" in titlestring):
            titles = titlestring.split("–")
            titles = [i.strip() for i in titles]
            item["title"] = titles[1]
        else:
            item["title"] = titlestring.strip()

        musicInfoString = remove_tags(responseSelector.xpath('//*[@id="genesis-content"]/article/*[@class="entry-content"]/h3')[0].extract())
        if ("-" in musicInfoString):
            musicInfo = musicInfoString.split("-")
            musicInfo = [i.strip() for i in musicInfo]
            item["key"] = musicInfo[0].replace("Key:", "").strip()
            item["beat"] = musicInfo[1].replace("Beat:", "").strip()
        elif ("|" in musicInfoString):
            musicInfo = musicInfoString.split("|")
            musicInfo = [i.strip() for i in musicInfo]
            item["key"] = musicInfo[0].replace("Key:", "").strip()
            item["beat"] = musicInfo[1].replace("Beat:", "").strip()

        item['url'] = response.url

        gotNamesfromElement = False

        artistInfoObject = responseSelector.xpath('//*[@id="genesis-content"]/article//*[@class="artist-name"]')
        if (len(artistInfoObject) > 0) :
            aristInfoString = remove_tags(artistInfoObject[0].extract())
            aristInfoString = aristInfoString.replace("|","/")
            artistNames = aristInfoString.split("/")
            isascii = lambda s: len(s) == len(s.encode())
            sinhalaArtistNamesArray = []
            for i in artistNames :
                if not isascii(i):
                    sinhalaArtistNamesArray.append(i)
            item['artist'] = sinhalaArtistNamesArray
            if ( len(sinhalaArtistNamesArray) > 0 ):
                gotNamesfromElement = True
        ## Translated Data

        songInfo = responseSelector.xpath('//*[@id="genesis-content"]/article/*[@class="entry-content"]/*[@class="su-row"]//ul/li')
        for i in range(0,len(songInfo)):
            headstring = remove_tags(songInfo[i].extract())
            if( "Artist:" in headstring and not gotNamesfromElement) :
                artiststring = headstring.replace("Artist:", "").strip()
                artists = artiststring.split(",")
                artists = [i.strip() for i in artists]
                translated_artists = translate_array(artists)
                item['artist'] = translated_artists
            elif(( "Genre:" in headstring ) ) :
                genrestring = headstring.replace("Genre:", "").strip()
                genre = genrestring.split(",")
                genre = [i.strip() for i in genre]
                translated_genre = translate_array(genre)
                item['genre'] = translated_genre
            elif (("Lyrics:" in headstring)):
                writerstring = headstring.replace("Lyrics:", "").strip()
                writers = writerstring.split(",")
                writers = [i.strip() for i in writers]
                translated_writers = translate_array(writers)
                item['writer'] = translated_writers
            elif (("Music:" in headstring)):
                composerstring = headstring.replace("Music:", "").strip()
                composers = composerstring.split(",")
                composers = [i.strip() for i in composers]
                translated_composers = translate_array(composers)
                item['composer'] = translated_composers
            elif (("Movie:" in headstring)):
                item['movie'] = translate_word(headstring.replace("Movie:", "").strip())
        return item
