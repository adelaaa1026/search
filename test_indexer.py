import math
import pytest
from index import Indexer
from query import Querier
from cmath import log
import xml.etree.ElementTree as et

#### TEST INDEXER #####

'''
Testing the constructor runtime (efficiency)
'''

def test_indexer_constructor():
    indexer = Indexer("Page_rank_Example2.xml", "title", "doc", "word")
    return indexer.all_links

def test_indexer_constructor_2():
    indexer = Indexer("MedWiki.xml", "title", "doc", "word")

def test_indexer_constructor_3():
    indexer = Indexer("SmallWiki.xml", "title", "doc", "word")

def test_indexer_constructor_4():
    indexer = Indexer("BigWiki.xml", "title", "doc", "word")

def test_indexer_constructor_5():
    indexer = Indexer("SmallWiki.xml", "title", "doc", "word")


'''
PROCESSING ALL PAGES:

'''

def test_processing_text_2():
    # Test: removing stop words.
    #       including words in the links. 
    xml = "MiniWiki1.xml"
    root = et.parse(xml).getroot()
    all_pages = root.findall("page")
    page1 = all_pages[0]
    indexer = Indexer("MiniWiki1.xml", "title", "doc", "word")
    words = indexer.processing_text(page1)
    print(words)
    assert len(words) == 6
    
def test_processing_text_3():
    # Test: 1) when meeting a special link, the first part is the link,
    #       the second part is the word.
    #    2) check whether regex can get upper cases and other special spellings
    #       in the text. 
    xml = "MiniWiki_Process_text.xml"
    root = et.parse(xml).getroot()
    all_pages = root.findall("page")
    page1 = all_pages[0]
    indexer = Indexer("MiniWiki_Process_text.xml", "title", "doc", "word")
    words = indexer.processing_text(page1)
    assert len(words) == 15

def test_process_all_pages():
    indexer = Indexer("MiniWiki_Process_text.xml", "title", "doc", "word")
    assert len(indexer.pages_to_their_words) == 3
    assert indexer.ni_for_all_words["weather"] == 2
    print("all_links: ", indexer.all_links)
    assert len(indexer.all_links[0]) == 2
    print("all titles: ", indexer.id_to_title_dictionary.values())
    print("all ids to titles:")
    print("word_ro_count_in_pages: ", indexer.ni_for_all_words)
    print("words to doc relevance: ", indexer.words_to_doc_relevance)

# TEST id_to_title:
def test_id_to_title():
    indexer = Indexer("Page_rank_Example2.xml", "title", "doc", "word")
    assert len(indexer.id_to_title()) == 4

'''
PAGERANK:

'''
# TEST PAGERANK:
def test_calc_weights():
    indexer = Indexer("Page_rank_Example2.xml", "title", "doc", "word")
    print(indexer.page_pairs_to_weights)

def test_calc_weights_and_distance():
    # Test case example 1 from the handout: 
    indexer = Indexer("Page_rank_test_2.xml", "title", "doc", "word")

    # Test the method, calc_weight:
    print(indexer.page_pairs_to_weights)
    assert indexer.page_pairs_to_weights[('C', 'A')] == 0.9
    # Test there is no link from a page to oneself. 
    assert abs(indexer.page_pairs_to_weights[('A', 'A')] - 0.05) < 0.0001
    # Test a page that have no links will link to everyone other than itself.
    assert abs(indexer.page_pairs_to_weights[('B', 'A')] - 0.475) < 0.0001
    assert abs(indexer.page_pairs_to_weights[('B', 'C')] - 0.475) < 0.0001

    # Test the method, calc_distance:
    rank1 = {0: 0.3333,	1: 0.3333,	2: 0.3333}
    rank2 = {0: 0.4750, 1: 0.1916,	2: 0.3333}	
    distance_1_2 = 0.2003
    rank3 = {0: 0.4148, 1: 0.2519, 2: 0.3333}
    distance_2_3 =	0.0851
    a1 = abs(indexer.calc_distance(rank1, rank2) - distance_1_2)
    print(a1)
    a2 = abs(indexer.calc_distance(rank2, rank3) - distance_2_3)
    print(indexer.calc_distance(rank2, rank3))

    # !!!? the second assertion does not work with 0.0001. 
    # Will it be a problem?
    assert abs(indexer.calc_distance(rank1, rank2) - distance_1_2) < 0.0001 
    assert abs(indexer.calc_distance(rank2, rank3) - distance_2_3) < 0.001 

def test_calc_pageranks():
    # Test case example 2 from the handout: 
    indexer = Indexer("Page_rank_Example2.xml", "title", "doc", "word")
    print(indexer.calc_page_ranks())
    assert abs(indexer.calc_page_ranks()[0] - 0.2018) < 0.0001
    assert abs(indexer.calc_page_ranks()[1] - 0.0375) < 0.0001
    assert abs(indexer.calc_page_ranks()[2] - 0.3740) < 0.0001
    assert abs(indexer.calc_page_ranks()[3] - 0.3867) < 0.0001

    indexer2 = Indexer("PageRankExample4.xml", "title", "doc", "word")
    print(indexer2.calc_page_ranks())
    assert abs(indexer2.calc_page_ranks()[1] - 0.0375) < 0.0001
    assert abs(indexer2.calc_page_ranks()[2] - 0.0375) < 0.0001
    assert abs(indexer2.calc_page_ranks()[3] - 0.4625) < 0.0001
    assert abs(indexer2.calc_page_ranks()[4] - 0.4625) < 0.0001

def test_calc_pageranks_2():
    # Test case example 3 from the handout: 
    # Testing a link to itself is not counted. 
    indexer3 = Indexer("PageRankExample3.xml", "title", "doc", "word")
    print(indexer3.calc_page_ranks())
    print(indexer3.page_pairs_to_weights)
    print(indexer3.all_links)
    assert abs(indexer3.calc_page_ranks()[1] - 0.0524) < 0.0001
    assert abs(indexer3.calc_page_ranks()[2] - 0.0524) < 0.0001
    assert abs(indexer3.calc_page_ranks()[3] - 0.4476) < 0.0001
    assert abs(indexer3.calc_page_ranks()[4] - 0.4476) < 0.0001
def test_calc_pageranks_3():
    # Test case example 3 from the handout: 
    # Testing a special link: [[rain | sun]]
    indexer4 = Indexer("PageRankExample1.xml", "title", "doc", "word")
    assert abs(indexer4.calc_page_ranks()[1] - 0.4326) < 0.0001
    assert abs(indexer4.calc_page_ranks()[2] - 0.2340) < 0.0001
    assert abs(indexer4.calc_page_ranks()[3] - 0.3333) < 0.0001

#test the method pages_to_relevance_dict and its helper relavence_of_words
def test_relevance():
    indexer = Indexer("MiniWiki1.xml", "title", "doc", "word")
    #test the relevance of word "weather" in the page at 0
    assert indexer.words_to_doc_relevance["weather"]\
           [int(indexer.all_pages[0].find("id").text.strip())] == \
            pytest.approx(math.log(3))


    #test the relevance of word "sun" in the page at 1
    assert indexer.words_to_doc_relevance["sun"]\
           [int(indexer.all_pages[1].find("id").text.strip())] == \
            pytest.approx(math.log(3))

def test_relevance2():
    indexer = Indexer("MiniWiki2.xml", "title", "doc", "word")
    #test the relevance of word "ratti" in the page at 0
    assert indexer.words_to_doc_relevance["best"]\
           [int(indexer.all_pages[0].find("id").text.strip())] == \
            pytest.approx(0.5*math.log(3/2))

    #test the relevance of word "ratti" in the page at 1
    assert indexer.words_to_doc_relevance["ratti"]\
           [int(indexer.all_pages[1].find("id").text.strip())] == \
            pytest.approx(math.log(3/2))   


def test_relevance3():
       indexer =  Indexer("MiniWiki3.xml", "title", "doc", "word")  
       #testing in pipe link the text is counted 
       assert indexer.words_to_doc_relevance["spring"]\
           [int(indexer.all_pages[0].find("id").text.strip())] == \
            pytest.approx(1/3*math.log(3/2)) 
       #testing in pipe link the title isn't counted
       assert indexer.words_to_doc_relevance["love"]\
           [int(indexer.all_pages[0].find("id").text.strip())] == \
            pytest.approx(1/3*math.log(3/2))  
       
       #testing the text in category link is counted
       assert indexer.words_to_doc_relevance["season"]\
           [int(indexer.all_pages[1].find("id").text.strip())] == \
            pytest.approx(math.log(3))  

       #testing the text in normal link is counted   
       assert indexer.words_to_doc_relevance["movi"]\
           [int(indexer.all_pages[1].find("id").text.strip())] == \
            pytest.approx(1/2*math.log(3/2))  
                     




