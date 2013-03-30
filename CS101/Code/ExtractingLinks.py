## Udacity CS101 Web Crawler
import urllib2
    
##
#   Utilities
##    
def union(a,b):
    return list(set(a+b))

def split_string(source,splitlist):    
    default_sep = splitlist[0]
    for sep in splitlist[1:]:
        source = source.replace(sep, default_sep)
    return [i.strip() for i in source.split(default_sep) if i != '']

def hash_string(keyword,buckets):
    sum = 0
    for c in keyword:
        sum += ord(c)
    return sum % buckets  
    
##
#   Index Stuff
##    
def lookup(index,keyword):
    for entry in index:
        if (entry[0] == keyword):
            return entry[1]
    return []
    
def record_user_click(index,keyword,url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] += 1

def add_to_index(index, keyword, url):
    # loop through existing keywords
    for entry in index:
        # check if current keyword matches our parameter value
        if entry[0] == keyword:
            # loop through existing url-count lists
            for url_and_count in entry[1]:
                if url_and_count[0] == url:
                    return
            # if we leave loop, url does not yet exist, so append it
            entry[1].append([url, 0])
            return
    # not found, add new keyword to index
    index.append([keyword, [[url, 0]]])  

def add_page_to_index(index,url,content):
    contentList = content.split()
    
    for keyword in contentList:
        add_to_index(index, keyword, url)

##
#   Crawl Stuff
##
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote+1:end_quote]
    return url, end_quote
        
def get_all_links(page):
    links = []
    while get_next_target(page)[0] != None:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""
    
def crawl(seed):
    tocrawl = [seed]
    crawled = []
    index = []
    
    while tocrawl:
        next_crawl = tocrawl.pop()
        if next_crawl not in crawled:
            page = get_page(next_crawl)
            add_page_to_index(index,next_crawl,page)
            page_links = get_all_links(page)
            union(tocrawl, page_links)
        crawled.append(next_crawl)
    return index


##
# TESTING
##

# execution timer
import time

def time_execution(code):
    start = time.clock()
    result = eval(code)
    run_time = time.clock() - start
    print result, run_time
    
def spin_loop(n):
    i = 0
    while i < n:
        i = i + 1
    return i

# make big indexes
def make_string(p):
    s = ""
    for e in p:
        s = s + e
    return s

def make_big_index(size):
    index = []
    letters = ['a', 'a', 'a', 'a', 'a', 'a', 'a', 'a']
    while len(index) < size:
        word = make_string(letters)
        add_to_index(index, word, 'fake')
        for i in range(len(letters) - 1, 0, -1):
            if letters[i] < 'z':
                letters[i] = chr(ord(letters[i]) +1)
                break
            else:
                letters[i] = 'a'
    return index

seed = 'http://www.udacity.com/cs101x/index.html'

# print crawl(seed)

index10000 = make_big_index(10000)
time_execution('lookup(index10000, "udacity")')
