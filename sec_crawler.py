from copy import deepcopy
from pyexpat import features
from bs4 import BeautifulSoup
import urllib.request
#from urllib.request import Request

seed_url = "https://www.sec.gov/news/pressreleases"
url='https://www.sec.gov/news/press-release/'
urls = [seed_url]    #queue of urls to crawl
seen = [seed_url]    #stack of urls seen so far
opened = []          #we keep track of seen urls so that we don't revisit them
ans=[] # store the covid

maxNumUrl = 20; #set the maximum number of urls to visit
print("Starting with url="+str(urls))
while len(urls) > 0 and len(ans) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue    #skip code below
    soup = BeautifulSoup(webpage,features='lxml')  #creates object soup
    # Put child URLs into the stack
    text=soup.get_text().lower()
    text=text.replace('-',' ')
    text=text.replace(',',' ')
    text=text.replace('.',' ')
    text=text.replace('\n',' ')
    text=text.split(' ')
    text=[i for i in text if i!="" ]
    if "charges" in text:
        t=" ".join(text)
        ans.append((curr_url,t))
    
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href'] #extract just the link
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        if url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)
        
print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print("num. of URLs that is about charges",len(ans))
print("List of charges URLs:")
for (url,text) in ans:
    print(url)
    print(text)