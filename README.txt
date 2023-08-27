Readme

Group members: Adela (Bingbin) Zhou, Meichen Liu

Known bug: none


------------Instructions for use--------------
Before users interact with the program, we first need to set the indexer up 
by inputting the following to the terminal: python index.py <file-path of xml> 
<file-path of titles> <file-path of docs> <file-path of words>
(python could be python3, depending on different python setups.) 

Next, we set up the querier for the users by inputting the following into the 
terminal: python query.py <file-path of titles> <filepath of docs> 
<file-path of words>. After running this line, we will see the terminal is 
prompting for a user input: “search> ” 

When we see “search> ”, it is time for the users to input their query!  They 
can input everything they want, such as “!!!”, “????”, “IIIII”, “apple!”, 
“basketball”. When users hit “enter” on the keyboard, querier will print out 
a list of ten page titles with their rank based on the calculated page score 
related to the user input. After printing out the page list, the program will
print another “search> ”, prompting for another user input.

If users input “quit”, the program will stop running. If users input anything 
other than “quit”, the program will repeat a, b, c until the input is “quit”.


-------How the pieces of our program fit together------
We have three python files:  index.py, query.py, and file_io.py. 

Index.py file has an indexer class that is responsible for parsing a given 
XML document into a list of words, determining the relevance between terms 
and documents, as well as the authority of each document. 

Then Index.py uses methods in file_io.py to write the aforementioned information
into titles file, words file, and docs file. When a user has a query,  query.py 
will read these doc files and determine which pages are most relevant to the 
query and will return the top ten pages.


----------------------Testing Index--------------------------------
In Indexer, we have 10 functions (including the constructor ): 
“__init__”
id_to_title
process_all_pages
processing_text
pages_to_relevance_dict 
relevance_of_words
calc_page_ranks
calc_distance
calc_weights
write

Indexer mainly has five parts:
1. Parse the xml file.
2. Finish populating id_to_title_dictionary.
3. Finish populating ids_to_pageranks dictionary.
4. Finish populating words_to_doc_relevance dictionary.
5. Write the three dictionaries into the inputted empty files.

Our tests are separated into 5 parts corresponding to the five parts above. 


>>>>>>>>>>>>>Indexer-Test-part1:
Unit Testing: __init__, process_all_pages, processing_text. 
We will whether the words and links could be parsed properly.

Besides the normal cases, here are some edge cases for processing_text:
1. Pages that have no links, will link to everywhere except to itself.
2. Pages that have no words.
3. Pages that have special links such as [[Parent|father]], or [[Category:
 detectives]]. 
4. Pages that have special words (upper case, quotes, [], too many white spaces,
 etc.) such as “WATER, ‘water’, WAtEr, Waters,      water… xhsilts, 
 [water] ::water!!water.”
5. The words in links are also being parsed and included into words, while 
the first part in a link with | is not included in words. For example: 
[[rain]], the word rain is included in words. For link, [[ sun | rain ]],  
sun is not included in words, but rain is. Moreover, if “sun” does not link to 
any page in this xml file, “sun” will not be included in all_links[this page],
but rain will always be included in words. 
6. If a page has multiple links at different places in the text that link to 
the same page, the multiple links will be counted as one link. For example, if 
a page have links: [[sun]], [[sun | rain]], [[sun]]. we will say this page has
1 link in total. 


>>>>>>>>>>>>>Indexer-Test-part2:
Unit Testing: id_to_title. Test the length of it is the same as all_pages.


>>>>>>>>>>>>>Indexer-Test-part3:
Unit Testing: calc_page_ranks,  calc_distance,  calc_weights. 
We want to test whether weights calculation and distance calculation are accurate. 
We also want to test whether the pageranks are accurate. 


>>>>>>>>>>>>>Indexer-Test-part4:
Unit Testing: pages_to_relevance_dict,  and its helper relavence_of_words. 
We want to test whether relevance (tf*idf) of a given word in a given page is 
calculated correctly. 

In the tests test_relevance() and test_relevance2(), we used MiniWiki1 and 
MiniWiki2 we wrote to test some base cases, including words that are the 
most frequent words in  a page(tf = 1), words that appear in multiple pages 
(ni > 1), etc.

In the test test_relevance3()  we used MiniWiki3 we wrote to test whether the 
texts in links are counted appropriately. For example,  in pipe links only the 
words after “|” are counted. In category links and normal links, all words are 
counted.


>>>>>>>>>>>>>Indexer-Test-part5:
[System testing: We test whether the method write works properly by testing 
Querier.]   
 
----------------------Testing Query-------------------------------- 
In Indexer, we have 5 functions (including the constructor): 
“__init__”
read
calc_final_score
find_top_ten
process_query

Querier mainly has three parts:
1. Read the input files.
2. Process user input into a list of words.
3. Calculate final score and get the top ten pages.

Our tests are separated into 3 parts corresponding to the 3 parts above. 


>>>>>>>>>>>>>Querier-Test-part1:
[System testing: We test whether the method read works properly by testing 
the other method outputs.]


>>>>>>>>>>>>>Querier-Test-part2:
Unit Testing:__init__, process_query. Test whether the words and links could
 be parsed properly. The same as Indexer-Test-part1, without link-related testing.


>>>>>>>>>>>>>Querier-Test-part3:
Unit Testing: calc_final_score, and its helper find_top_ten. Test whether the 
method calc_final_score calculates the score of each page correctly and returns 
the top ten pages.

We first used the MiniWiki2 we wrote to test some base cases, which should 
return pages in the correct order based on their scores. Since MiniWiki2 doesn't 
contain any links, the querier should return the same result with or without 
pageRanks. 

We then wrote six tests using the MedWiki provided, including three tests with 
pageRank and three tests without pageRank.
 
