# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest

from itemadapter import ItemAdapter
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class WebscrapingPipeline(object):
    def __init__(self):
        cred = credentials.Certificate({
            "type": "service_account",
            "project_id": "bitbulletin-6052e",
            "private_key_id": "fc4b68dd25c7e6c205eccbeb4010f2ecc1f45c91",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDoGtwEEN34evpj\nORNDQRfukGFmHAoxufcbtG8OpwweMUzEV3ymsgbOVwXt4ujM/tPz1EE5DXv3bU07\n8JOwm8yzzkzL8+BcCZB5iyVfap5pmmqrUEaJ29c8aSWz1f9KfUv+YI7SpfABIHmc\nl3lgmy6Md4Qnqh4uAIlfKy314WPZuoeZm7Zh8OQu9CyE0ctgss1NIJsEl68rqlqK\njO1pQVGQS0NfdRhlRUXha1feWd0+iKBEK/fhcklni8fsQ/LmSmhcyXGb4/Lk6N/j\nFkssjOgd4EiPjfVW41RWyEVA8k9Mwkp6aAfIMwFCMSHdI51irV7zMe9+deFdTc5k\nwjfsvuKXAgMBAAECggEAA6COfqZwKZbBEfWNi61ZPTpWuKdIhiq/UK4FrEdyWjMa\nstjL0w5mKn7+pznhZHljq474w/ZQ0SGNUESmsjRabcGUE/3dgY1eth+Kt86Ckj4+\nW4Cs0YZfezYIx6IuU/uC9AM4nX8dXI8lh2EbSFC0g1pyH206UoK3TYbvDXAhGivB\n8jxqMGldTI+JBmHySTRC+uiOrW48Av1M4vzaIouIV4/dNxG/D4R7IENnOnAhWGm2\nWu6gMAWmQ/n2NFgU6D88rjkc6OTRs3+guJyMeJ02MgFw9l1G+2inTlQwg2rAOIqU\nBgOxPBXGJvxL8AsuKGn3RACdl906alpHLlWjbGpWrQKBgQD8FImzRFeU/GwDdWBM\n5fpQxi2ThdkQ/qOtF9HjE/mqW/A1j4D7fi6LCjhQDKAbQjCYL6aITAzxPYnoCsLi\n3xCz01y2nMZIqOtGWVILj8z3qMZebk0RKJrjjLBLM9AirqL3wEAxL2haKrG233dx\n8xLcrizCy9u0vD+SoXwW2BtP1QKBgQDrts4qvGSZPueU8DSg5Put71bzKwe+0qvO\nfutAeZtq8NCsgu8fdhjG5xB/IZTRY5q0JBtXAks8LciBXImflt/SQBJWQuGGqSP/\nNjZ1kBTDyQ2ssEDuAfbxGzTi8fJlyQpkyM6/sqkD+FlRfkntTClmKDikbuhszoqf\nF+4pkNhKuwKBgDosMyrflqaXKgYSTEryt7V0RohI1zMI0JTdbl5M+czKssBpgYaI\nNA16Kkyu3TPtLnGwbWn+wu3ZGb4m3Zqlh6E4IakyvL9/2+u8KSbp5I8yr7STF83h\n5PymNvjj2CBo1Mr/3tB69EX6nFBreZEeWzf6KfI6QVWQK8uW4KAU9xiRAoGBAJSK\nuxnLZ0n7jk0ZotDR/Jj7/zt2nobulD6pVO9oszyNTbOpP6//6FVQP+Ed9H6P2moz\nZtdKJsdhwr1i54eeuKXyopuhwiXuaTTnoSItDijjhq6Q1BopOslub8Gk3zCtpNMm\niMPdfw11cDQe9c+I833hUvCsw+PttQXVOs0O7n8JAoGAelL8yn5mjHk6Hh9YKdmq\nblNohKhRrD6SsT7wC65ab9qddcmFmORu2ZcWDgKGwaPJhRFCEBIDWJJWbD6AIW4U\nSAtGnrksfPKM7PcOhUgDgbSRW5gMGE6u5y9O+G3QxEJtazBhKjn6sNjfc9tzZGB8\nd3VHI6enPuH7IK4XwuzJDsg=\n-----END PRIVATE KEY-----\n",
            "client_email": "firebase-adminsdk-khuhj@bitbulletin-6052e.iam.gserviceaccount.com",
            "client_id": "105186619009911355205",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-khuhj%40bitbulletin-6052e.iam.gserviceaccount.com"
}
)
        firebase_admin.initialize_app(
            cred, {"databaseURL": "https:/bitbulletin-6052e.firebaseio.com"}
        )

    def process_item(self, item, spider):
        news = ItemAdapter(item).asdict()

        content = news['content']

        extraString = 'Compunode.com Pvt. Ltd. ( ).Designed for  . Copyright © 2022, Dawn Scribe Publishing Platform' 
        extraString2 = ".Updated"

        if extraString in content:
            content = content.replace(extraString, '')
        if extraString2 in content:
            content = content.split(extraString2, 1)
            content = content[0]

        summary = self.text_summarizer(content)

        time = news['time']
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        news = {
            "title": news['title'],
            "author": news['author'],
            "content": content,
            "image": news['image'],
            "time": time,
            # "date": news['date'],
            "category": news['category'],
            "source": news['source'],
            "summary": summary,
            "link": news['link'],
        }

        if news["category"] == "business":
            print("true1")
            self.businessNews_save(news)
        if news["category"] == "sports":
            print("true2")
            self.sportsNews_save(news)
        if news["category"] == "tech":
            print("true3")
            self.techNews_save(news)

    def businessNews_save(self, techNews):
        db = firestore.client()
        tech_ref = (
            db.collection(u"newCategory")
            .document(u"uLzkXth3HoYSWg9qF8VR")
            .collection(u"Business")
        )
        tech_ref.add(techNews)

    def sportsNews_save(self, sportsNews):
        db = firestore.client()
        tech_ref = (
            db.collection(u"newCategory")
            .document(u"uLzkXth3HoYSWg9qF8VR")
            .collection(u"Sports")
        )
        tech_ref.add(sportsNews)

    def techNews_save(self, techNews):
        db = firestore.client()
        tech_ref = (
            db.collection(u"newCategory")
            .document(u"uLzkXth3HoYSWg9qF8VR")
            .collection(u"Tech")
        )
        tech_ref.add(techNews)

    def text_summarizer(self, raw_docx):
        nlp = spacy.load("en_core_web_sm")

        raw_text = raw_docx
        docx = nlp(raw_text)
        stopwords = list(STOP_WORDS)
        # Build Word Frequency
        # word.text is tokenization in spacy
        word_frequencies = {}
        for word in docx:
            if word.text not in stopwords:
                if word.text not in word_frequencies.keys():
                 word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / maximum_frequncy
        # Sentence Tokens
        sentence_list = [sentence for sentence in docx.sents]

        # Calculate Sentence Score and Ranking
        sentence_scores = {}
        for sent in sentence_list:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if len(sent.text.split(" ")) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]

        # Find N Largest
        summary_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
        final_sentences = [w.text for w in summary_sentences]
        summary = " ".join(final_sentences)
        # print('\n\nSummarized Document\n')
        return summary