# -*- coding: utf-8 -*-
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

'''def ToRify():
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
    socket.socket = socks.socksocket
    currentip = requests.get("http://icanhazip.com").text
    print "=================="
    print "ToRify Using IP Address: " + currentip
    print "=================="'''

class PropertiSpider(scrapy.Spider):
    name = "properti"
    start_urls = ['https://www.urbanindo.com/cari/Indonesia/']
    currentpage = 1
    def parse(self,response):
        x = 0
        '''ToRify()'''
        for properti in response.css('li.__item'):
            yield {
            'tipe_properti': properti.css('h4.property-type-title::text').extract_first(),
            'judul': properti.css('h4.long-title::text').extract_first(),
            'lokasi': properti.css('ul li.address::text').extract_first(),
            'alamat': properti.css('ul li.additionalRegion::text').extract_first(),
            'kabkot': properti.css('ul li.locality::text').extract_first(),
            'provinsi': properti.css('ul li.province::text').extract_first(),
            'jumlah kamar': properti.css('div.items__info div.row div.col-xs-8 ul.property-attribute-list-view span::text').extract(),
            'jumlah lavatory': properti.css('div.items__info div.row div.col-xs-8 ul.property-attribute-list-view span::text').extract(),
            'luas lahan': properti.css('div.items__info div.row div.col-xs-8 ul.property-attribute-list-view span::text').extract(),
            'luas bangunan' : properti.css('div.items__info div.row div.col-xs-8 ul.property-attribute-list-view span::text').extract(),
            'harga': properti.css('span.price::text').extract_first(),
            'agen': properti.xpath("//*[@class='contact-agent btn btn-primary btn-sm']/@data-agent-name").extract()[x],
            'username': properti.xpath("//*[@class='contact-agent btn btn-primary btn-sm']/@data-agent-username").extract()[x],
            'kontak': properti.xpath("//*[@class='contact-agent btn btn-primary btn-sm']/@data-agent-telephone").extract()[x],
            'company': properti.css('div.__items__info__more div.info a.agent-info__company-name::text').extract_first(),
            }
            if x == 9:
            	break
            x=x+1
     
        time.sleep(randint(3,15))

        page = self.currentpage + 1
        next_page= "/cari/Indonesia/listingType_sale/radius_-1/page_%s" % page
        if response.css('div.property-list-pagination li.next') is not None:
            next_page = response.urljoin(next_page)
            self.currentpage = page
            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)
        else:
            print "Finished."
