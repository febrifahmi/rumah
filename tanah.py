import scrapy
import time
import socks
import socket
import requests
from random import randint


'''
Untuk mendapatkan data selector seperti di bawah ini, lakukan interogasi data secara manual dengan scrapy shell terlebih dahulu,
$> scrapy shell 'url'

response.css('div.land-size b::text').extract() #luas lahan
response.css('h2.listing-title a::text').extract() #judul iklan
response.xpath("//*[@class='listing-location']/@title").extract()[x] #lokasi lahan, dimana x adalah index dari list lokasi, x dimulai dari 0
response.css('div.price-info::text').extract_first()  #harga
response.xpath("//*[@class='btn btn-default contact-agent-btn']/@data-agent-name").extract_first() #contact agent name
response.xpath("//*[@class='btn btn-default contact-agent-btn']/@data-agent-id").extract_first() # agent id
response.xpath("//*[@class='btn btn-default contact-agent-btn']/@data-ads-url").extract_first() #url iklan
response.css('div.posted-date::text').extract_first() #tayang sejak
response.xpath("//*[@class='ajax']/@href").extract_first()[x] #hal selanjutnya
'''

def ToRify():
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
    socket.socket = socks.socksocket
    currentip = requests.get("http://icanhazip.com").text
    print "=================="
    print "ToRify Using IP Address: " + currentip
    print "=================="

class TanahSpider(scrapy.Spider):
    name = "tanah"
    start_urls = ['https://www.rumah123.com/tanah-dijual/']
    currentpage = 1
    def parse(self,response):
        x = 0
        ToRify()
        for tanah in response.css('div.listing.gts-listing'):
            yield {
            'tanah': tanah.css('h2.listing-title a::text').extract_first(),
            'lokasi': tanah.xpath("//*[@class='listing-location']/@title").extract()[x],
            'luasan': tanah.css('div.land-size b::text').extract_first(),
            'harga': tanah.css('div.price-info::text').extract_first(),
            'penjual': tanah.xpath("//*[@class='btn btn-default contact-agent-btn']/@data-agent-name").extract()[x],
            'penjual_id': tanah.xpath("//*[@class='btn btn-default contact-agent-btn']/@data-agent-id").extract()[x],
            'tanggal_tayang': tanah.css('div.posted-date::text').extract_first(),
            'url': tanah.xpath("//*[@class='btn btn-default contact-agent-btn']/@data-ads-url").extract()[x],
            }
            x=x+1

        time.sleep(randint(3,15))
        
        page = self.currentpage + 1
        next_page= "/tanah-dijual/page-%s" % page
        if response.css('div.listing.gte-listing') is not None:
            next_page = response.urljoin(next_page)
            self.currentpage = page
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        else:
            print "Finished."
