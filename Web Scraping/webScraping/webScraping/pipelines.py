# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from itemadapter import ItemAdapter
import re

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest



class WebscrapingPipeline(object):
    def process_item(self, item, spider):
        newsArray = ItemAdapter(item).asdict()
        contentList = newsArray['content']
        # contentString = ' '.join(map(str, contentList))
        contentString = ''.join(contentList)
        # contentStringJoin = ''.join(contentString)
        summarizedContent = self.text_summarizer(contentString)
        # newsTitleString = "'" + newsArray['title'] + "'"
        # newsTitle = newsArray['title'].replace('(', '')
        # newsTitle = newsTitleString.replace('(', '')
        newsTitle = newsArray['title']
        newsTitleString = ''.join(newsTitle)
        newsAuthor = newsArray['author']
        newsAuthorString = ''.join(newsAuthor)
        newsImage = newsArray['image']
        newsImageString = ''.join(newsImage)


        # print(summarizedContent)
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

        print("News INFO PRINTINGGGGG now new")
        print(newsInfo)
        # newsTitleString = ''.join(newsTitle)
        # print("news title strings")
        # print(newsTitleString)
        # authorString = ''.join(newsAuthor)
        # print("News author")
        # print(authorString)
        # print(contentString)
        # print(contentStringJoin)
        # print(contentString)

        # print(newsTitle)
        # json_object = json.dumps(newsInfo, indent = 4)
  
        # # # Writing to sample.json
        # with open("freshNews.json", "w") as outfile:
        #     outfile.write(json_object)
       

    # def print_content(self, con):
    #     print("This is the function contenttt", con)

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
        