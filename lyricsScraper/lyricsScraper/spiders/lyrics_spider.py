from scrapy import Spider
from scrapy.selector import Selector
from lyricsScraper.items import LyricsscraperItem
from w3lib.html import remove_tags

class LyricsSpider(Spider):
    name = "lyricslk"
    allowed_domains = ["lyricslk.com"]
    start_urls = [
        "http://lyricslk.com/lyrics/sunil-edirisinghe/1187-ran-malak-lesa.html"
    ]

    def parse(self, response):
        responseSelector = Selector(response)
        item = LyricsscraperItem()
        item['songLyrics'] = remove_tags(responseSelector.xpath("//*[contains(@id, 'lyricsBody')]")[0].extract())
        songInfo = responseSelector.xpath('//*[@id="lyricsViewer"]/*[@class="lyricsInfo"]/span')
        for i in range(0,len(songInfo),2):
            headstring = remove_tags(songInfo[i].extract())
            if( "Song title" in headstring ) :
                item['artist'] = remove_tags(songInfo[i+1].extract())
            elif(( "The author" in headstring ) ) :
                item['writer'] = remove_tags(songInfo[i+1].extract())
            elif(( "The singer" in headstring ) ) :
                item['artist'] = remove_tags(songInfo[i+1].extract())
        yield item
