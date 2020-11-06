# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json, urllib.request
import ssl
import pandas as pd

class IeeexploreSpider(scrapy.Spider):
    name = 'ieeexplore'
    allowed_domains = ['ieee.org']
    #doi_shneiderman = '10.1109/TTS.2020.2992669'

    def __init__(self, doi='', **kwargs):
        super().__init__(**kwargs)
        self.get_ieee_paper(doi)

    def get_ieee_paper_dict(self, doi):
        api_key = '3r88q7n22u429vtenyjjrhks'
        url = f'https://ieeexploreapi.ieee.org/api/v1/search/articles?parameter&apikey={api_key}&doi={doi}'
        context_ssl = ssl._create_unverified_context()

        try:
            with urllib.request.urlopen(url, context = context_ssl) as url:
                data = json.loads(url.read().decode())
                return data
        except Exception as e:
            print(e)

        return {}

    def get_ieee_paper(self, doi):
        data = self.get_ieee_paper_dict(doi)

        article_data = data['articles']
        title = article_data[0]["title"]

        authors_data = article_data[0]['authors']['authors']
        authors_full_name = ''
        for i in authors_data:
            authors_full_name += i['full_name'] +', '

        abstract = article_data[0]['abstract']

        final_data = [{
            'DOI': doi,
            'Title': title,
            'Author(s)': authors_full_name,
            'Abstract': abstract,
        }]

        df = pd.DataFrame(final_data, columns = ['DOI', 'Title', 'Author(s)', 'Abstract'])

        df.to_csv('ieee.csv')

