import os
from random import randint
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    linked = corpus[page]
    baseAdd = (1-damping_factor)/len(corpus)
    linkedCount = len(corpus[page])
    if (linkedCount ==0):#accounting for if no linked
        d = dict()
        for page in corpus:
            d[page] = 1/len(corpus)
        return d
            
    linkedPlus = damping_factor/linkedCount
    returnDict = dict()
    for page in corpus:
        returnDict[page] = baseAdd
        if (page in linked):
            returnDict[page] += linkedPlus
    return returnDict
        
    
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #randint includes last one and first one
    #sys.setrecursionlimit(SAMPLES + 100)
    whichPlace = randint(0,len(corpus)-1)
    startPage = list(corpus.keys())[whichPlace]
    passDict = dict()
    for key in corpus.keys():
        passDict[key] =0
    passDict[startPage] = 1/n
    increaseFactor = 1/n
    #print(startPage)
    return completeSample(corpus, damping_factor, n-1, startPage, passDict,increaseFactor)


    #raise NotImplementedError

def completeSample(corpus, damping_factor, n, startpage, passDict, increaseFactor):
    while True:
        if (n==0):#break case
            return passDict
            break

        fromThere = transition_model(corpus, startpage, damping_factor)
        whichOne = randint(0,10*SAMPLES)/(10*SAMPLES)
        nextPage = None
        #gives a value between 0 and 1 
        for page in fromThere.keys():
            whichOne = whichOne - fromThere[page]
            if (whichOne <=0):
                nextPage = page#corpus[page]
                passDict[page] += increaseFactor
                break
        if (nextPage == None):
            print("error")
            print(whichOne)
        #print(nextPage)
  
        n = n-1
        startpage = nextPage
            
        #return completeSample(corpus, damping_factor, n-1, nextPage, passDict, increaseFactor)
                           




    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    val = dict()
    increaseFactor = 1/len(corpus)
    for i in corpus.keys():
        val[i] = increaseFactor
    #PR(p) = (1-d)/len(corpus) + d * for i in links(p) (PR(i))/len(links(p))
    change = 1
    times = 1
    corpusLength = len(corpus)
    #while (change>= 0.001):
    sampleRank = sample_pagerank(corpus, damping_factor, SAMPLES)
    while (change>= 0.001):
        change = 0 #minimize this
        for page in val.keys():
            previousVal = val[page]

            if (len(corpus[page]) ==0):
                count = 0
                for i in val.keys():
                    count += val[i]
                count = count/len(val)
                val[page] = count + (1-damping_factor)/corpusLength
            else:
                length = len(corpus[page])#the number of pages being linked to
                count= 0
                for i in corpus[page]:
                    count = count + val[i]
                count = count / length
                val[page] = count + (1-damping_factor)/corpusLength
            if (val[page]-previousVal>change or previousVal-val[page]>change):
                change = val[page] - previousVal
                if (change<0):
                    change = change * -1
    return val
            
                
    #raise NotImplementedError


if __name__ == "__main__":
    main()
