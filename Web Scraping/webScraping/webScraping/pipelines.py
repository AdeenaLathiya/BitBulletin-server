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
        cred = credentials.Certificate("./credentials.json")
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
            db.collection(u"Category")
            .document(u"uLzkXth3HoYSWg9qF8VR")
            .collection(u"Business")
        )
        tech_ref.add(techNews)

    def sportsNews_save(self, sportsNews):
        db = firestore.client()
        tech_ref = (
            db.collection(u"Category")
            .document(u"uLzkXth3HoYSWg9qF8VR")
            .collection(u"Sports")
        )
        tech_ref.add(sportsNews)

    def techNews_save(self, techNews):
        db = firestore.client()
        tech_ref = (
            db.collection(u"Category")
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