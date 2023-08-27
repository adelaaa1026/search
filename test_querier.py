import math
from index import Indexer
from query import Querier
from cmath import log

#### TEST FUNCTIONS IN QUERIER #####

def test_find_top_ten():
    # Test find TOP 10 helper function:
    querier = Querier("title", "doc", "word")
    # if there are more than 10 pages:
    dict1 = {
        0: 1, 1: 1, 2: 200, 3: 3, 4: 400, 5: 5, 6: 600, 7: 7, \
            8: 800, 9: 9, 10: 1000, 11: 11, 12: 1200, 13: 13
    }
    # if there are less than 10 pages:
    dict2 = {
        0: 1, 1: 1, 2: 200, 3: 3, 4: 400
    }
    # if there are 10 pages:
    dict3 = {
        0: 1, 1: 1, 2: 200, 3: 3, 4: 400, 5: 5, 6: 600, 7: 7, 8: 800, 9: 9
    }
    top_10 = querier.find_top_ten(dict1)
    top_10_2 = querier.find_top_ten(dict2)
    top_10_3 = querier.find_top_ten(dict3)
    assert top_10[0] == (1200, 12)
    assert top_10_2[0] == (400, 4)
    assert top_10_3[0] == (800, 8)

def test_process_query():
    # Test different kinds of query inputs:
    querier = Querier("title", "doc", "word")
    q_list1 = querier.process_query("I see the fire.")
    q_list2 = querier.process_query("")
    q_list3 = querier.process_query("I")
    q_list4 = querier.process_query("Star")
    q_list5 = querier.process_query("STAR")
    q_list6 = querier.process_query("xisjeksidsfajdk")
    q_list7 = querier.process_query("??!&&OOO2***4542")
    assert len(q_list1) == 2
    assert len(q_list2) == 0
    assert len(q_list3) == 0
    assert len(q_list4) == 1
    assert q_list4[0] == "star"
    assert q_list5[0] == "star"
    assert q_list6[0] == "xisjeksidsfajdk"
    assert q_list7[0] == "ooo2"
 


def system_texting_query():
    indexer = Indexer("MedWiki.xml", "title", "doc", "word")
    querier = Querier("title", "doc", "word")
    ## Test "cats" without pagerank
    # check whether the printed output is the same as the ones TA provided:
    querier.have_pagerank = False
    print(querier.calc_final_score("cats"))
    ## Test "cats" with pagerank:
    querier.have_pagerank = True
    print(querier.calc_final_score("cats"))
    ## Test "computer science" without pagerank:
    querier.have_pagerank = False
    print(querier.calc_final_score("computer science"))
    ## Test "computer science" with pagerank:
    querier.have_pagerank = True
    print(querier.calc_final_score("computer science"))
    ## Test weird inputs without pagerank:
    querier.have_pagerank = False
    print(querier.calc_final_score(""))
    print(querier.calc_final_score("xndjfishaklsls"))
    print(querier.calc_final_score("see you"))
    print(querier.calc_final_score("a"))
    ## Test weird inputs with pagerank:
    querier.have_pagerank = True
    print(querier.calc_final_score("ajsosllskajaiaojsn"))
    print(querier.calc_final_score("see you"))
    print(querier.calc_final_score("a"))
    

def call_all_tests():
    system_texting_query()
    test_process_query()
    test_find_top_ten()


#Use our own wiki to test the method cal_final_score() and its helper find_top_ten().
#This wiki doesn't contain any links, so the querier should return the same result
#  regardless of its pagerank.
def test_querier_miniwiki():
    indexer = Indexer("MiniWiki2.xml", "title", "doc", "word")
    querier = Querier("title", "doc", "word")
    querier.have_pagerank = False #testing querier without pagerank
    assert querier.calc_final_score("best beef") == ['ratty', 'tasty', 'andrews']
    querier.have_pagerank = True #testing querier with pagerank
    assert querier.calc_final_score("best beef") == ['ratty', 'tasty', 'andrews']


#test the method cal_final_score() and its helper find_top_ten()
def test_querier_medwiki():
    indexer = Indexer("MedWiki.xml", "title", "doc", "word")
    querier = Querier("title", "doc", "word")
    
    querier.have_pagerank = False #testing without pageRank
    print("1 baseball is: ", querier.calc_final_score("baseball"))
    assert querier.calc_final_score("baseball") == ['Oakland Athletics', \
        'Minor league baseball', 'Miami Marlins', 'Fantasy sport', \
        'Kenesaw Mountain Landis', 'Out', 'October 30', 'January 7', \
        'Hub', 'February 2']
    assert querier.calc_final_score("fire") == ['Firewall (construction)',\
        'Pale Fire','Ride the Lightning', 'G?tterd?mmerung', 'FSB', 'Keiretsu',
        'Hephaestus', 'KAB-500KR', 'Izabella Scorupco', 'Justin Martyr' ]
  
    querier.have_pagerank = True #testing with pageRank
    assert querier.calc_final_score("fire") == ['Falklands War', \
        'Justin Martyr', 'Firewall (construction)', 'Empress Suiko', \
        'New Amsterdam', 'Pale Fire', 'Montoneros', 'Hermann G?ring', \
        'Nazi Germany', 'Navy']
    
    #manually compare the output with the answers given by TAs
    print("baseball is: ", querier.calc_final_score("baseball"))
    print("fire is: ", querier.calc_final_score("fire"))
    print("united states is: ", querier.calc_final_score("united states"))
    print("computer science is: ", querier.calc_final_score("computer science"))
    print("battle is: ", querier.calc_final_score("battle"))
   



   

