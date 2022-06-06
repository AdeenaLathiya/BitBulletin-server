# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import json
from itemadapter import ItemAdapter
# import re

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import json
# import os
class WebscrapingPipeline(object):
    def __init__(self):
        cred = credentials.Certificate('./credentials.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https:/bitbulletin-73e03.firebaseio.com'
        })

    def process_item(self, item, spider):
        newsArray = ItemAdapter(item).asdict()

        newsTitle = newsArray['title']
        newsTitleString = ''.join(newsTitle)

        newsAuthor = newsArray['author']
        newsAuthorString = ''.join(newsAuthor)

        contentList = newsArray['content']
        contentString = ''.join(contentList)

        newsImage = newsArray['image']
        newsImageString = ''.join(newsImage)
       
        summarizedContent = self.text_summarizer(contentString)

        newsInfo = {
            "title": newsTitleString,
            "author": newsAuthorString,
            "content": contentString,
            "image": newsImageString,
            "time": newsArray['time'],
            "date": newsArray['date'],
            "category": newsArray['category'],
            "source": newsArray['source'],
            "summary": summarizedContent
        }
        
        db = firestore.client()
        def firebase_save():
            tech_ref = db.collection(u'Old12').document(u'Business').collection(u'News')
            tech_ref.add(newsInfo)

        firebase_save()    
       
        print("News INFO PRINTINGGGGG now new")
        print(newsInfo)

    def text_summarizer(self, raw_docx):
        nlp = spacy.load('en_core_web_sm')

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
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        # Sentence Tokens
        sentence_list = [ sentence for sentence in docx.sents ]

        # Calculate Sentence Score and Ranking
        sentence_scores = {}  
        for sent in sentence_list:  
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if len(sent.text.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word.text.lower()]
                        else:
                            sentence_scores[sent] += word_frequencies[word.text.lower()]

        # Find N Largest
        summary_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
        final_sentences = [ w.text for w in summary_sentences ]
        summary = ' '.join(final_sentences)
        # print('\n\nSummarized Document\n')
        return summary


    
            # return item
    #newsArray se object banwakr save krwaskte hain
        