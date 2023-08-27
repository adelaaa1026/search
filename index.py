import argparse
import copy
import math
import sys
import xml.etree.ElementTree as et
import re
from nltk.corpus import stopwords
STOP_WORDS = set(stopwords.words('english'))
from nltk.stem import PorterStemmer
nltk_test = PorterStemmer()
# read and write
import file_io

class Indexer:
    def __init__(self, xml : str, titles : str, docs : str, words : str):
        # Parse the xml file and get a list of pages:
        self.all_pages = et.parse(xml).getroot().findall("page")

        # For TITLES file:
        self.id_to_title_dictionary = self.id_to_title()

        # To process all the texts and links: 
        self.all_links = {}
        self.ni_for_all_words = {}
        self.pages_to_their_words = {}
        self.process_all_pages()

        # To get pagerank weights:
        self.page_pairs_to_weights = {}
        self.epsilon = 0.15
        self.number_of_pages = len(self.all_pages)
        self.ids_to_pageranks = self.calc_page_ranks()

        # To get relevances:
        self.words_to_doc_relevance = {}
        self.pages_to_relevance_dict()

        # To write into titles/docs/words files:
        self.write(titles, docs, words)

        
    def id_to_title (self) -> dict:
        id_to_title_dictionary = {}
        for page in self.all_pages:
            title = page.find('title').text.strip()
            id = int(page.find('id').text)
            id_to_title_dictionary[id] = title
        return id_to_title_dictionary

    def process_all_pages(self):
        '''
        A method that calls helper method: processing_text to process every 
        page in the page list: self.all_pages

        It will update information for the fields in the current Indexer class.

        Parameters: None
        Returns: None

        '''
        for page in self.all_pages:
            self.pages_to_their_words[page] = \
                self.processing_text(page)

    def processing_text (self, page : et) -> list :
        '''
        A method to process a single page.
        Steps:
        Parse -> Tokenizing -> Removing stopwords -> Stemming
        (Parsing is mostly done in the constructor already)

        Parameters:
        page -- an ElementTree, representing a page in wiki file.

        Return:
        words --a list, representing all the words 
        in the text of input page. 

        Updates: 
        self.all_links[id], update the links exist in this page. 
        self.ni_for_all_words, update the count for ni. 

        
        '''
        # Parse and get rid of extra white spaces:
        text = page.find('text').text.strip()
        id = int(page.find('id').text.strip())
        title = str(page.find('title').text.strip())

        # Tokenizing - get all the links:
        link_regex = '''\[\[[^\[]+?\]\]'''
        links = re.findall(link_regex, text)
        # Tokenizing - get all the words:
        n_regex = '''\[\[[^\[]+?\]\]|[a-zA-Z0-9]+'[a-zA-Z0-9]+|[a-zA-Z0-9]+'''
        words_with_links = re.findall(n_regex, text)
        words = [word for word in words_with_links if word not in links]

        # Process the links and store the in a dictionary: self.all_links
        self.all_links[id] = []
        links_texts = []
        for link in links:
            the_link = link.replace("[[", "").replace("]]", "")
            if "|" in the_link:
                the_word = the_link.split("|")[1]
                the_link = the_link.split("|")[0]
                the_word_processed = re.findall(n_regex, the_word)
                links_texts.extend(the_word_processed)
            else:
                the_word_processed = re.findall(n_regex, the_link)
                links_texts.extend(the_word_processed)
                
            #If the_link links to a valid page, and this link is not counted 
            #before, then add it into all_links for this page.
            titles_list = self.id_to_title_dictionary.values()
            if the_link in titles_list and the_link not in self.all_links[id]:
                if the_link != title:
                    self.all_links[id].append(the_link)
        # Add the word in link into word list
        words.extend(links_texts)
        
        # Check whether this page has no links 
        if len(self.all_links[id]) == 0:
            for p in self.all_pages:
                if p != page:
                    self.all_links[id].append(p.find("title").text.strip())

        # Removing stop words:
        words = \
            [word.lower() for word in words if not word.lower() in STOP_WORDS]
        
        # Stemming:
        words = [nltk_test.stem(word) for word in words]

        # Keep track of n_i: the number of docs that contains it:
        no_duplicate_words = []
        for word in words:
            # if the word is already counted, we do not count it again. 
            if word not in no_duplicate_words:  
                if word in self.ni_for_all_words:
                    self.ni_for_all_words[word] += 1
                else:  
                    self.ni_for_all_words[word] = 1
                no_duplicate_words.append(word)   
    
        return words
        

    def pages_to_relevance_dict(self):
        '''
        This method calls the helper method relevance_of_words()
        to calculate the relevance of all pages.
       
        Parameters:
        None.

        Return:
        None.

        '''
        for page in self.all_pages:
            self.relavence_of_words(page)

    def relavence_of_words(self, page: et):
        '''
        A method that calculates relevance of words in a given page.

        Parameters:
        page -- an ElementTree, representing a page in wiki file.

        Return:
        words --a list, representing all the words 
        in the text of input page. 

        Updates: 
        self.words_to_doc_relevance dictionary
        
        '''
        words_to_count_dict = {} # a dict that mapps words to their counts
        aj = 1  # the maximum count in this page
        words_in_this_page = self.pages_to_their_words[page] 

        #populating the words_to_count dict, and updating aj, the maximum count
        for word in  words_in_this_page:
            if word in words_to_count_dict:
                words_to_count_dict[word] += 1
                if words_to_count_dict[word] > aj:
                    aj = words_to_count_dict[word]
            else:
                words_to_count_dict[word] = 1     
      
        #calculating tf, idf, and relavance of words in this page, 
        # and saving the relavance in a dictionary
        for word in  words_in_this_page:
            tf =  words_to_count_dict[word]/ aj  
            idf = math.log(self.number_of_pages/self.ni_for_all_words[word])
            if not word in self.words_to_doc_relevance:
                self.words_to_doc_relevance[word] = {}
            # save relavances in the words_to_doc_relevance dictionary
            self.words_to_doc_relevance[word][int(page.find("id").text.strip())]\
                 = tf * idf

    

    def calc_page_ranks(self) -> dict:
        '''
        A method to calculate pageranks.

        Parameter:
        None

        Return:
        a dict --representing the dictionary from page id to its pagerank.
        '''
        page_rank_1 = {} # a dictionary from page id to rank. (r) 
        page_rank_2 = {} # (r')
        for page in self.all_pages:
            page_rank_1[page.find("id").text.strip()] = 0
            page_rank_2[page.find("id").text.strip()] = 1/self.number_of_pages
        self.calc_weights()
        while self.calc_distance(page_rank_1, page_rank_2) > 0.001:
            page_rank_1 = page_rank_2.copy()
            for page1 in self.all_pages:
                page_rank_2[page1.find("id").text.strip()] = 0
                for page2 in self.all_pages:
                    page_rank_2[page1.find("id").text.strip()] \
                        = page_rank_2[page1.find("id").text.strip()] \
                            + self.page_pairs_to_weights[(page2, page1)]* \
                                page_rank_1[page2.find("id").text.strip()]
        return page_rank_2
            

    def calc_distance(self, page_rank_1, page_rank_2) -> int:
        '''
        A method to calculate distance between two dictionary of pageranks.

        Parameters:
        page_rank_1 -- a dictionary from page id to its pagerank. (r)
        page_rank_2 -- another dictionary from page id to its pagerank. (r')

        Return:
        an int -- representing the distance between the two ranks.
        '''
        squares_sum = 0
        for page in self.all_pages:
            squares_sum = \
                squares_sum + \
                    (page_rank_1[page.find("id").text.strip()] - \
                        page_rank_2[page.find("id").text.strip()]) ** 2
        distance = squares_sum ** (1/2)
        return distance     


    def calc_weights(self):
        '''
        A method that calculates the weights between pages and store them to 
        self.page_pairs_to_weights
        It is called inside of calc_page_ranks method.

        Parameter:
        None

        Return:
        None

        Updates:
        self.page_pairs_to_weights
        '''
        for k in self.all_pages:
            k_id = int(k.find("id").text.strip())
            for j in self.all_pages:
                if str(j.find('title').text.strip()) in self.all_links[k_id]: 
                    #if page 2 is linked to page 1
                    self.page_pairs_to_weights[(k, j)] = \
                        self.epsilon/self.number_of_pages \
                        + (1-self.epsilon)/len(self.all_links[k_id])
                else:
                    self.page_pairs_to_weights[(k, j)] = \
                        self.epsilon/self.number_of_pages
    
    def write(self, titles: str, docs : str, words : str):
        '''
        A method that write self.id_to_title_dictionary, self.ids_to_pageranks,
        self.words_to_doc_relevance into the empty input files. 

        Parameters:
        titles --a string, representing the filepath to store titles & id info.
        docs --a string, representing the filepath to store pagerank info.
        words --a string, representing thr filepath to store relevance info.

        Return:
        None

        Updates:
        titles, docs, words. 
        '''
        file_io.write_title_file(titles, self.id_to_title_dictionary)
        file_io.write_docs_file(docs, self.ids_to_pageranks)
        file_io.write_words_file(words, self.words_to_doc_relevance)


# main:
# it is used in the terminal. 

if __name__ == "__main__":
    #print(sys.argv)
    if len(sys.argv) == 5:
        xml = sys.argv[1]
        titles = sys.argv[2]
        docs = sys.argv[3]
        words = sys.argv[4]
        i = Indexer(xml, titles, docs, words)



    












    
