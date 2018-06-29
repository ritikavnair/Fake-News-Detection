import pandas as pd 
import os
from sklearn.utils import shuffle
import crawler
LEN=2

''' fetch the raw real news data from csv '''

def fetchDataFrameRealNewsCSV():
    print('Fetching real news dataset....')
    fake_news_data = pd.read_csv('../DataSets/uci-news-aggregator.csv')
    dfReal = pd.DataFrame(data=fake_news_data)
    return dfReal

''' fetch the raw fake news data from csv '''

def fetchDataFrameFakeNewsCSV():
    print('Fetching fake news dataset....')
    fake_news_data = pd.read_csv('../DataSets/fake.csv')
    dfFake = pd.DataFrame(data=fake_news_data)
    return dfFake

''' process fake news data '''

def processFakeNewsDataFrame(dfFake):
    pd.options.mode.chained_assignment = None
    dfFake=dfFake.astype('str')
    dfFake['country']=pd.Series('united states',index=dfFake.index)
    dfFake['Site Country']=dfFake['site_url'].apply(lambda x: str(x).split('.')[0])
    dfFake=dfFake[['site_url','title','text','author','language','country','Site Country','published']]
    dfFake['Fake ( fake =1 and Real =0)']=pd.Series('1',index=dfFake.index)
    dfFake.columns=[ 'URL', 'Title', 'Text', 'Author', 'Language', 'Site Country', 'Site Name', 'ThreadPublication Date', 'Fake ( fake =1 and Real =0)']
    print (len(dfFake['URL'][1].split('.')[1])==3)
    dfFake=dfFake.loc[(dfFake['Language']=='english') & (dfFake['Site Country']=='united states')]
    print dfFake['URL'].size
    dfFake.reindex(fill_value='')
    print "No. of fake records : ",dfFake['URL'].size
    return dfFake

''' process real news data '''

def processRealNewsDataFrame(dfReal):
    pd.options.mode.chained_assignment = None
    dfReal=dfReal.loc[(dfReal['CATEGORY']=='b') & (dfReal['URL']!='') & (dfReal['URL']!=None)] #& dfReal.URL.str.contains('^http') ]
    dfReal['Text']=pd.Series('',index=dfReal.index)
    dfReal['Fake ( fake =1 and Real =0)']=pd.Series('0',index=dfReal.index)
    dfReal['Language']=pd.Series('english',index=dfReal.index)
    dfReal['Site Country']=pd.Series('united states',index=dfReal.index)
    dfReal=dfReal.drop_duplicates('URL')
    dfReal=dfReal[['URL','TITLE','Text','PUBLISHER','Language','Site Country','HOSTNAME','TIMESTAMP','Fake ( fake =1 and Real =0)']]
    dfReal.columns=[ 'URL', 'Title', 'Text', 'Author', 'Language', 'Site Country', 'Site Name', 'ThreadPublication Date', 'Fake ( fake =1 and Real =0)']
    dfReal=dfReal.astype('str')
    dfReal.reindex()
    print 'No. of Real news records: ',dfReal['URL'].size
    return dfReal

''' extract top real news urls for crawling '''

def extractTopRealResultsForCrawling(dfReal):
    print "Retrieve top 20000 Real news data"
    num=dfReal.size
    loop=num/10000
    listOfIndex=[]
    df=[]
    for i in range(0,loop):
        listOfIndex.append(dfReal[i*10000:(i+1)*10000])
        df+=[dfReal[i*10000:(i+1)*10000]]
    
    #print "length of dataframe array retrieved:",len(df[0])
    return df[:LEN]

''' filter text records that is not relevant or null '''

def filterNullTextContentRecords(df):
    keyList =['Page Not Found','The item that you have requested was not found','The address was entered incorrectly',\
              'The item no longer exists','There has been an error on the site','We apologize for any inconvenience','font-size,font-family',\
              'text-align','404 - File or directory not found','The resource you are looking for might have been removed', \
              'had its name changed', 'or is temporarily unavailable.','Return to the previous page',\
              'If you feel the address you entered is correct you can contact us',\
               'mentioning the error message received and the item you were trying to reach','It looks like nothing was found at this location.',\
               'Well, this is unfortunate','Your story was not found','The story you requested could not be found',\
               '404 - File or directory not found','PAGE NOT FOUND','We\'re sorry that the page you\'re looking for cannot be found','Page Not Found - 404',\
               'Sorry, but the page you were looking for is not here','This is usually the result of a bad or outdated link','ERROR404',\
               'The case of this missing page is still unsolved','Return to the previous page','The item that you have requested was not found',\
               'The case of this missing page is still unsolved','The page may no longer exist or may have moved to another web address',\
               'The page you were looking for cannot be found','The page you requested cannot be found',\
               'Either it doesn\'t exist or it was removed from the site','It looks like nothing was found at this location',\
               'This Page Could Not Be Found','404 Sorry, the page you have searched for doesnt exist','Nothing was found at this location',\
               'ERROR404The case of this missing page is still unsolved','Error 404 Nothing found','404 - File or directory not found',\
               'Oh no!No content to show for this page','404 The resource or page you are looking for could have been removed, had its name changed, or is temporarily unavailable',\
               'Sorry, the page you are looking for cannot be found','Oops! Page Not Found','Oops! Page Not Found',\
               '404We\'re sorry, but the page you were looking for doesn\'t exist','Page not found','Pardon Our Interruption',\
               '500 - Internal server error','Not found, error 404','The page you are looking for no longer exists','Oops, This Page Could Not Be Found',\
               'The page you\'ve requested can not be displayed','It appears you\'ve missed your intended destination, either through a bad or outdated link',\
               'This might be because:You have typed the web address incorrectly, or the page you were looking for may have been moved, updated or deleted',\
               'we couldn\'t find the page you were looking for','500 - Internal server error.There is a problem with the resource you are looking for, and it cannot be displayed',\
               'We haven\'t been able to serve the page you asked for','We\'re sorry, but we seem to have lost this page','PAGE NOT FOUND',\
               'We\'re sorry,the page you requested could not be found']   # print keyList
    print 'No. of records: ',df['URL'].size
    pd.options.mode.chained_assignment = None
    for index,row in df.iterrows():
        if checkText(str(row['Text']),keyList) or len(str(row['Text']))<300:
            df.drop(index, inplace=True)
    df.reindex()
     
''' test whether the key words exist in the given text '''

def checkText(text,keyWords):
    
    for key in keyWords:
        if key in text:
            return True
    return False

''' combine and shuffle the data '''  
   
def combineAndShuffle(dfCombine):
    combinedDf = pd.concat(dfCombine)
    combinedDf = shuffle(combinedDf)
    return  combinedDf   

''' extract real and fake news data '''
    
def dataSetExtraction():
    dfReal=fetchDataFrameRealNewsCSV()
    dfFake=fetchDataFrameFakeNewsCSV()
    dfFake=processFakeNewsDataFrame(dfFake) 
    dfReal=processRealNewsDataFrame(dfReal)
    dfCombine=[]
    for d in extractTopRealResultsForCrawling(dfReal):
        print 'len of datadrame :',d['URL'].size
        #d=d[:100]
        d=crawler.crawlUrlsFromDF(d)
        d=filterNullTextContentRecords(d)
        dfCombine+=[d]
    dfCombine+=[dfFake]
    df=combineAndShuffle(dfCombine)
    if os.path.exists('../DataSets/FinalDataSet.csv'):
        os.remove('../DataSets/FinalDataSet.csv')    
    df.to_csv('../DataSets/FinalDataSet.csv', index=False)
    print 'No. of records in final data set: ',df['URL'].size
    print "Saving New CSV file"

if __name__=='__main__':dataSetExtraction()