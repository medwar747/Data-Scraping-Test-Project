# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 22:33:01 2022

@author: medwar
Michael V. Edwards

The following code
    was written in Spyder,
    utilizes scrapy,
    and was executed with Command Prompt on Windows
        1) activate ScrapyEnvironment
        2) cd [path to 'spiders' folder]
        3) scrapy crawl Scrape -o ResultsSheet.csv -t csv
"""

import scrapy

class LearningItem(scrapy.Item):

    # Defining item fields of interest
    completionTime = scrapy.Field() # Estimated completion time
    specialty = scrapy.Field() # Specialty
    topics = scrapy.Field() # Topics included
    creditAvailableFor = scrapy.Field() # Which professionals benefit from this course
    faculty = scrapy.Field() # faculty


class Scrape(scrapy.Spider):
    name="Scrape"
    # Clinical Consultations™: Expert Opinions on the Management of Ocular Health in Glaucoma – Updating the Armamentarium with Advances in Treatment
    allowed_domains = ['www.learning.freecme.com']
    start_urls = ["https://learning.freecme.com/a/36979Pftpok"]
                
    # Extracting each item value from the website
    # Using its xpath in the browser HTML inspector
    def parse(self, response):
        item = LearningItem()
        
        # Extract completion time data
        item['completionTime'] = response.xpath('/html/body/div/div/div/div[2]/div[1]/div[1]/div[4]/p[@style="text-align: left;"]/text()').extract()
        # clean up each entry
        for i in range(len(item['completionTime'])):
            item['completionTime'][i-1] = item['completionTime'][i-1].strip()
        
        # Extract specialty data
        item['specialty'] = response.xpath('/html/body/div/div/div/div[2]/div[1]/div[2]/div[1]/p[@style="text-align: left;"]/text()').extract()
        # clean up each entry
        for i in range(len(item['specialty'])):
            item['specialty'][i-1] = item['specialty'][i-1].strip()
        
        # Extract topic data
        item['topics'] = response.xpath('/html/body/div/div/div/div[2]/div[1]/div[2]/div[2]/p[@style="text-align: left;"]/text()').extract()
        # clean up each entry
        for i in range(len(item['topics'])):
            item['topics'][i-1] = item['topics'][i-1].strip()
        
        # Extract which professionals benefit from the course
        item['creditAvailableFor'] = response.xpath('/html/body/div/div/div/div[2]/div[1]/ul[1]/li/strong/text()').extract()
        # clean up each entry
        for i in range(len(item['creditAvailableFor'])):
            item['creditAvailableFor'][i-1] = item['creditAvailableFor'][i-1].strip()
            
        # Extract faculty data
        # By testing for faculty data until there are no more entries
        item['faculty'] = []
        i = 4
        while (i>=4):
            try:
                # clean up each entry
                nextAdditionList = response.xpath('/html/body/div/div/div/div[2]/div[1]/div['+str(i)+']/div/h4[@class="media-heading"]/text()').extract()
                item['faculty'].append(nextAdditionList[0].strip())
                i = i + 1
            except:
                break
        
        return item