import functools
import re
from itertools import chain
from functools import reduce

WORD_MIN_LENGTH = 2
inverted = {}

def split(text):
    """
        Split the text into words
    """
    tokens =[]
    tokens = re.split(';|,|\*|\n| |\t|:|\(|\)|_|\+|=',text)
    #print(tokens)
    return tokens

def generate_ngrams(word):
    pass 

def normalize(words):
    """
    Do a normalization precess on words. In this case is just a tolower(),
    but you can add accents stripping, convert to singular and so on...
    """
    normalized_words = []
    lower_words = (word.lower() for word in words)
    reversed_words = (word[::-1].lower() for word in words)
    for word in chain(lower_words, reversed_words):
        normalized_words.append(word)
    return normalized_words

def cleanup(words):
    """
    Remove words with length less then a minimum and stopwords.
    """
    cleaned_words = set(
            filter(lambda x: len(x) > WORD_MIN_LENGTH, words)
        )
    return cleaned_words

def tokenize(text):
    """
    Just a helper method to process a text.
    It calls word split, normalize and cleanup.
    """
    words = split(text)
    words = normalize(words)
    words = cleanup(words)
    return words


def index(text, line, filepath):
    """
    Create an Inverted-Index of the specified text document.
        {word:[locations]}
    """    
    for word in tokenize(text):
        locations = inverted.setdefault(word, [])
        locations.append(str(line)+":"+ str(filepath)+":"+text)

    return inverted

def index_file(filepath):
    print('visited index_file')
    with open(filepath) as file:
        for line_number, line in enumerate(file,1):
            #print(line_number, line)
            index(line.rstrip(),line_number,filepath)

def search(query):
    """
    Returns a set of documents id that contains all the words in your query.
    """
    print('visited in search')
    #words = [word for _, word in index(query) if word in inverted]
    results = inverted[query]
    return results
'''
if __name__ == '__main__':
    doc1 = """
Niners head coach Mike Singletary will let Alex Smith remain his starting 
quarterback, but his vote of confidence is anything but a long-term mandate.

Smith now will work on a week-to-week basis, because Singletary has voided 
his year-long lease on the job.

"I think from this point on, you have to do what's best for the football team,"
Singletary said Monday, one day after threatening to bench Smith during a 
27-24 loss to the visiting Eagles.
"""

    doc2 = """
The fifth edition of West Coast Green, a conference focusing on "green" home 
innovations and products, rolled into San Francisco's Fort Mason last week 
intent, per usual, on making our living spaces more environmentally friendly 
- one used-tire house at a time.

To that end, there were presentations on topics such as water efficiency and 
the burgeoning future of Net Zero-rated buildings that consume no energy and 
produce no carbon emissions.
"""

    # Build Inverted-Index for documents
    inverted = {}
    documents = {'doc1':doc1, 'doc2':doc2}
    for doc_id, text in documents.iteritems():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

    # Print Inverted-Index
    for word, doc_locations in inverted.iteritems():
        print word, doc_locations

    # Search something and print results
    queries = ['Week', 'Niners week', 'West-coast Week']
    for query in queries:
        result_docs = search(inverted, query)
        print "Search for '%s': %r" % (query, result_docs)
        for _, word in word_index(query):
            def extract_text(doc, index): 
                return documents[doc][index:index+20].replace('\n', ' ')

            for doc in result_docs:
                for index in inverted[word][doc]:
                    print '   - %s...' % extract_text(doc, index)
        print
'''

if __name__ == '__main__':
    index_file('/Users/raksingh/personal/my-scripts/scripts/search.py')
    for match in search('index'):
        print(match)