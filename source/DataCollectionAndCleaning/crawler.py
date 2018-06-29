import requests
from bs4 import BeautifulSoup
import pandas as pd
import Queue
import threading
import sys
import re

TEXT_PASSAGE={}
queue=Queue.Queue()

''' threaded crawler for crawling data '''
class ThreadedCrawler(threading.Thread):
    def __init__(self,queue):
        
        threading.Thread.__init__(self)
        self.queue=queue
        
       
    def run(self):
        while True:
            try:
                index,url=self.queue.get()
                print "thread no: "+str(threading.current_thread()) +", working on :"+str(index)
                sys.stdout.flush()
                page = requests.get(url)
                text = page.text
                soupObj = BeautifulSoup(text, 'html.parser')
                res = ""
                # remove any remaining image tags
                for img in soupObj.findAll('img'):
                    img.decompose()   
            
                # remove all formulas 
                for mathItems in soupObj.findAll('math'):
                    mathItems.decompose()    
    
                # remove all tables and their content
                for table in soupObj.findAll('table'):
                    table.decompose()
        
                # remove content navigation
                for conNav in soupObj.findAll('div', {'id':'toc'}):
                    conNav.decompose()
    
                # remove script
                for scripts in soupObj.findAll('script'):
                    scripts.decompose()


                for div in soupObj.find_all("div", {"class": re.compile("content")}):                    
                    res += div.get_text().encode('UTF-8')

                # Remove newlines and extra spaces
                res=res.strip()
                res=res.replace("\n", "")
                res=res.replace("\t","")
                res = " ".join(res.split())

                TEXT_PASSAGE[index]=res
            except Exception:
                TEXT_PASSAGE[index]=""
            self.queue.task_done()
       
def main(dataFrame=pd.DataFrame() ,URL=None,listOfUrls=None):  
    threadCount=1
    if not dataFrame.empty:
        #print "Enter the column name from which urls need to be extracted:"
        urlCol='URL'#raw_input()
        #print "Enter the target column name where the crawled text need to be inserted:"
        targetCol='Text'#raw_input()
        if dataFrame.size>10:
            threadCount=abs(dataFrame.size/100)
        startThreads(threadCount)
        for index, row in dataFrame.iterrows():
            queue.put((index,row[urlCol]))
        queue.join()
        count =1
        print 'start copying'
        for index in TEXT_PASSAGE:
            text = TEXT_PASSAGE[index]
            if text == '':                
                dataFrame.drop(index, inplace=True)
                continue
            dataFrame.at[index, targetCol] = text
            print "Completed : " + str(count)
            count+=1
        return dataFrame
    elif listOfUrls!=None:
        if len(listOfUrls)>10:
            threadCount=abs(len(listOfUrls)/10)
        startThreads(threadCount)
        for urls in listOfUrls:
            queue.put((urls,urls))
        queue.join()
        text=[]
        return TEXT_PASSAGE
    elif URL!=None:
        startThreads(threadCount)
        queue.put((URL,URL))
        queue.join()
        if URL in TEXT_PASSAGE:
            return TEXT_PASSAGE[URL]
        else: return ""
          
def startThreads(threadCount):
    
    try:
        for i in range(threadCount):
            print "Thread count :",i
            t=ThreadedCrawler(queue)
            t.setDaemon(True)
            t.start()
    except Exception as e:
        print "error"
        sys.stdout.flush()
        print e.__doc__
        print e.message
        sys.stdout.flush()
    

def crawlSingleUrl():
    
    ''' returns text crawled from url '''
    
    print "Enter url to crawl"
    url=raw_input()
    #text=main(dataFrame=None,URL=url,listOfUrls=None)
    text=main(URL=url)
    return text
    
def crawlListOfUrl():
    
    ''' returns a map {url: text} '''
    
    print "Enter multiple URLs comma separated (eg. http://www.wikipwdia.com, www.yahoo.com) "
    line=raw_input()
    urlList=line.split(',')
    #text=main(dataFrame=None, URL=None,listOfUrls=urlList)
    text=main(listOfUrls=urlList)
    return text
    
def crawlUrlsFromCSV():
    print "Enter the full path of the csv file: "
    f=raw_input()
    df = pd.read_csv(f)
    df=df.astype(str)
    df=main(dataFrame=df)
    df.to_csv(f, index=False) 

def crawlUrlsFromDF(df):
    df=df.astype(str)
    df=main(dataFrame=df)
    return df
       
def selectTask():
    print "\nSelect the Task to perform using multithreaded crawler :"
    print "Enter 1 : To crawl a single URL and return context text or null if the url does not exists."
    print "Enter 2 : To crawl a list of URLs. and return list of textual content"
    print "Enter 3 : To crawl URLs from a csv file and update the same csv on the target column"
    print "Enter 4 : To exit!!!!"
    options={1:crawlSingleUrl,
             2:crawlListOfUrl,
             3:crawlUrlsFromCSV,
             4:crawlUrlsFromDF}
    print "Enter Your Choice >>> "
    x=input()
    if x!=4:
        return options[x]()
     
if __name__ == '__main__':
    print 'Welcome to multithreaded crawler'
    t=selectTask()
    #print t
    #main('DataSets\RealNewsDataSet1.csv')
    