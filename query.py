import sys
from xml.etree.ElementTree import TreeBuilder
import file_io

import re

from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))

from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()

import argparse

import bisect

class Querier:
    def __init__(self, titles : str, docs : str, words : str):
            self.words_to_doc_relevance = {}
            self.ids_to_pageranks = {}
            self.ids_to_titles ={}
            self.read(titles, docs, words)

            # an component indicating whether Querier need to take pagerank 
            # into account. It is being set in main.py
            self.have_pagerank = False
            

    def read(self, titles: str, docs : str, words : str):
        file_io.read_title_file(titles, self.ids_to_titles)
        file_io.read_docs_file(docs, self.ids_to_pageranks)
        file_io.read_words_file(words, self.words_to_doc_relevance)
    
    def process_query(self, query_sentence : str) -> list:
        '''
        A method that process the user input text.
        process: tokenizing, removing stop words, stemming. 

        Parameter:
        query_sentence -- a string, representing the user input.

        Return:
        a list of strings, representing the processed user input. 
        '''
        # Tokenizing:
        n_regex = '''\[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        query_sentence = query_sentence.strip()
        query_words_list = re.findall(n_regex, query_sentence)
        # Removing stop words:
        query_words_list = \
            [word.lower() for word in query_words_list \
                if not word.lower() in STOP_WORDS]
        # Stemming:
        query_words_list = [nltk_test.stem(word) for word in query_words_list]

        return query_words_list
    
    def calc_final_score(self, query_sentence : str) -> list:
        '''
        a method that calculate the score of each page based on a given query
        and returns the top ten pages  

        Parameters:
        query_sentence -- a string of query from input

        Return:
        a list of ten links that have the highest final scores

        Updates: 
        self.words_to_doc_relevance dictionary
        
        '''    
        id_to_final_score = {} #dict that maps page an id to its score 
        query_words_list = self.process_query(query_sentence)
        
        #calculating the score of each page based on a given query
        # and save the results in the id_to_final_score dictionary
        for id in self.ids_to_titles:
            S_Qj = 0   

            #calculating S_Q,j by summing up relevances of all words in a query
            for word in query_words_list:
                if word in self.words_to_doc_relevance and \
                   id in self.words_to_doc_relevance[word]: #making sure 
                   #the word is in indexer and the page has the word
                    S_Qj = S_Qj + self.words_to_doc_relevance[word][id] 
            
            #save the results with or without page rank in a dictionary
            if self.have_pagerank:
                id_to_final_score[id] = S_Qj * self.ids_to_pageranks[id]
            else:
                id_to_final_score[id] = S_Qj
        
        top_ten_score_id_tuple = self.find_top_ten(id_to_final_score)

        #mapping a list of page id to a list of page titles
        top_ten_link = [self.ids_to_titles[x[1]] for x in top_ten_score_id_tuple]
        return top_ten_link
    
    def find_top_ten(self, page_id_to_final_score : dict) -> list: 
        
        '''
        A helper method that takes in a dictionary from page id to final score,
        and returns a list of ten pages that have the highest final scores   

        Parameters:
        page_id_to_final_score -- a dictionary, mapping page ids to their final scores.

        Return:
        a list of ten (score, page id) tuples that have the highest final scores
        '''    

        top_ten = [] #initializing a list of top ten pages

        #goes through all pages and keeps track of ten pages with highest scores
        for id in page_id_to_final_score:
            score = page_id_to_final_score[id] 
            
            #adding the page to the list if the list has less than 10 pages: 
            if len(top_ten) < 10:
                top_ten.append((score, id))
                top_ten = sorted(top_ten, key = lambda x: x[0], reverse=True)
            #if the list already has 10 pages:
            elif len(top_ten) == 10:
                #if the current score is larger than smallest score in the list:
                if score > top_ten[9][0]: 
                    del top_ten[9] 
                    top_ten.append((score, id))
                    top_ten =  sorted(top_ten, key = lambda x: x[0], reverse=True)
        
        return top_ten




if __name__ == "__main__":
    print(sys.argv)
    titles = ""
    docs = ""
    words = ""
    has_pagerank = False
    if len(sys.argv) == 4:
        titles = sys.argv[1]
        docs = sys.argv[2]
        words = sys.argv[3]
    elif len(sys.argv) == 5:
        titles = sys.argv[2]
        docs = sys.argv[3]
        words = sys.argv[4]
        has_pagerank = True
    q = Querier(titles, docs, words)
    if has_pagerank:
        q.have_pagerank = has_pagerank

    user_input = input("search>")
    while user_input != "quit":
        print("after while")
        print(q.calc_final_score(user_input))
        print("after a while")
        user_input = input("search>")    

