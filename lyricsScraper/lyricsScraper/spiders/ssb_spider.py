from scrapy import Spider, Request
from scrapy.selector import Selector
from lyricsScraper.items import LyricsscraperItem
from w3lib.html import remove_tags
import string

## Global Variable Decleration ##
removepunc = string.punctuation.replace(".","").replace(",", "").replace("/", "")

class LyricsSpider(Spider):
    name = "sinhalasongbook"
    allowed_domains = ["sinhalasongbook.com"]
    start_urls = [
        "https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=1"
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


        songLyricswithExtra = remove_tags(responseSelector.xpath('//*[@id="genesis-content"]/article/*[@class="entry-content"]//pre')[0].extract())
        songLyrics = "".join([char for char in songLyricswithExtra if ( ( char not in string.digits ) and (char not in string.ascii_letters) and (char not in removepunc )) ]).strip()
        item["songLyrics"] = songLyrics

        titlestring = remove_tags(responseSelector.xpath('//*[@id="genesis-content"]/article/*[@class="entry-content"]/h2')[0].extract())
        if("-" in titlestring):
            titles = titlestring.split("-")
            titles = [i.strip() for i in titles]
            item["title"] = titles
        elif("|" in titlestring):
            titles = titlestring.split("|")
            titles = [i.strip() for i in titles]
            item["title"] = titles
        else:
            item["title"] = titlestring.strip()

        songInfo = responseSelector.xpath('//*[@id="genesis-content"]/article/*[@class="entry-content"]/*[@class="su-row"]//ul/li')
        for i in range(0,len(songInfo)):
            headstring = remove_tags(songInfo[i].extract())
            if( "Artist:" in headstring ) :
                artiststring = headstring.replace("Artist:", "").strip()
                artists = artiststring.split(",")
                artists = [i.strip() for i in artists]
                item['artist'] = artists
            elif(( "Genre:" in headstring ) ) :
                genrestring = headstring.replace("Genre:", "").strip()
                genre = genrestring.split(",")
                genre = [i.strip() for i in genre]
                item['genre'] = genre
            elif (("Lyrics:" in headstring)):
                writerstring = headstring.replace("Lyrics:", "").strip()
                writers = writerstring.split(",")
                writers = [i.strip() for i in writers]
                item['writer'] = writers
            elif (("Music:" in headstring)):
                composerstring = headstring.replace("Music:", "").strip()
                composers = composerstring.split(",")
                composers = [i.strip() for i in composers]
                item['composer'] = composers
            elif (("Movie:" in headstring)):
                item['movie'] = headstring.replace("Movie:", "").strip()
        return item
