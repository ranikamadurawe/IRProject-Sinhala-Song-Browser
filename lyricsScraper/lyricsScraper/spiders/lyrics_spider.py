from scrapy import Spider, Request
from scrapy.selector import Selector
from lyricsScraper.items import LyricsscraperItem
from w3lib.html import remove_tags
import string

# http://lyricslk.com/search.php?q="+char+"&by=sortByLetter&page=1" for char in string.ascii_lowercase
class LyricsSpider(Spider):
    name = "lyricslk"
    allowed_domains = ["lyricslk.com"]
    start_urls = [
        "http://lyricslk.com/search.php?q=e&by=sortByLetter&page=1"
    ]

    def parse(self, response):
        responseSelector = Selector(response)
        urls = responseSelector.xpath('//*[@id="SearchResults"]/*[@class="ResBound"]/*[@class="ResTitle"]/a/@href')
        for i in urls:
            songurl = i.extract()
            yield Request(songurl, callback=self.parse_songdata)
        currentURL = responseSelector.xpath('//*[@id="searchNavigation"]//*[@class="current"]/a/@href')[0].extract()
        urlPages = responseSelector.xpath('//*[@id="searchNavigation"]/ul/li/a/@href')
        nextURL = "reachedEnd"
        for i in range(0,len(urlPages)):
            if (currentURL == urlPages[i].extract() ):
                if(i < len(urlPages)-1 ):
                    nextURL = urlPages[i+1].extract()
                else:
                    nextURL = "reachedEnd"
                break
        if(nextURL != "reachedEnd") :
            yield Request(nextURL, callback=self.parse)

    def parse_songdata(self, response):
        responseSelector = Selector(response)
        item = LyricsscraperItem()

        item['title'] = []
        item['writer'] = []
        item['artist'] = []

        item['songLyrics'] = remove_tags(responseSelector.xpath("//*[contains(@id, 'lyricsBody')]")[0].extract())

        sinhalaData = remove_tags(responseSelector.xpath("//*[contains(@id, 'lyricsTitle')]/h2")[0].extract())
        if (sinhalaData != None):
            sinhalaDataArray = sinhalaData.split("-")
            sinhalaAristName = sinhalaDataArray[1].strip()
            sinhalaTitleName = sinhalaDataArray[0].strip()
            item['artist'].append(sinhalaAristName)
            item['title'].append(sinhalaTitleName)

        songInfo = responseSelector.xpath('//*[@id="lyricsViewer"]/*[@class="lyricsInfo"]/span')
        for i in range(0,len(songInfo),2):
            headstring = remove_tags(songInfo[i].extract())
            if( "Song title" in headstring ) :
                item['title'].append(remove_tags(songInfo[i+1].extract()).replace(":","").strip())
            elif(( "The author" in headstring ) ) :
                item['writer'].append(remove_tags(songInfo[i+1].extract()).replace(":","").strip())
            elif(( "The singer" in headstring ) ) :
                item['artist'].append(remove_tags(songInfo[i+1].extract()).replace(":","").strip())

        if(len(item['artist']) == 0):
            item['artist'].append('unknown')
        elif(len(item['writer']) == 0):
            item['writer'].append('unknown')
        item['url'] = response.url
        yield item
