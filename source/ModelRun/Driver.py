import os.path
import pickle
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.ranking import roc_auc_score
from sklearn.metrics.scorer import make_scorer
from sklearn.model_selection import GridSearchCV
from DataVisualization import Visualize
from Models.LogisticRegressionImplementation import ModelLogisticRegression
from Models.NaiveBayes import NaiveBayes
from PerformanceEvaluation import Evaluate
import numpy as np
import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


MODEL={1:"Logistic Regression Model",2:"Naive Bayes Model"}
PARAMS={1:(0.0004,0.0003,1000),2:2}
TITLE ={"ModelLogisticRegression":"Logistic Regression Model",
        "NaiveBayes":"Naive Bayes Model",
        "GridSearchCV":"Support Vector Machine Model",
        "RandomForestClassifier":"Random Forest Model"}

def fetchData(fileName,modelObj):
    data=pd.read_csv(fileName)
    print "Enter the size of data to train and test (max data - 20000): "
    dataSize=input()
    print "Enter the ratio of data of Train to Test data (for example: 0.8 for 80% Train to 20% test: "
    data=data[:dataSize]
    trainDataSize=int(abs(dataSize*0.8))
    testStartIndex=trainDataSize
    testEndIndex=dataSize
    
    ''' fetching data text feature from data set for training '''
    X_train=data.iloc[:trainDataSize,2].values
    
    ''' fetching real or fake  feature from data set for training '''
    y_train=data.iloc[:trainDataSize,-1].values
    
    ''' fetching data text feature from data set for testing  '''
    X_test=data.iloc[testStartIndex:testEndIndex,2].values
    
    ''' fetching data text feature from data set for testing '''
    y_test=data.iloc[testStartIndex:testEndIndex,-1].values
    
    print "The data split is as follows:"
    print "X-train :",len(X_train)
    print "Y-train :",len(y_train)
    print "X-test :",len(X_test)
    print "Y-test :",len(y_test)
    
    ''' fetch stop words list from nltk '''
    stopwords_=[word.encode('utf-8')for word in list(stopwords.words('english'))]
    #print stopwords_
   
    ''' Optimization of feature generation based on Model '''
    
    if modelObj.__class__.__name__!='GridSearchCV':
        maxFeatures=50000
    else:
        maxFeatures=10000
    
    ''' intiallize tfidf object  '''
    ''' feature generation -> tfidf { parameters max_features set to a fixed number to produce results fast,
                                     stop_words are removed by initializing the param stop_words using a 
                                     stop words list fetched using NLTK lib }'''    
    tfidf = TfidfVectorizer(min_df=1,max_features=maxFeatures,stop_words=stopwords_)
    
    ''' Generate TF-IDF Feature for train and test data'''
    tfidfTrain = tfidf.fit_transform(X_train).toarray()
    tfidfTest= tfidf.transform(X_test).toarray()
    
    ''' dimensions of new features generated '''
    print 'Shape of the tfidf vector :', np.shape(tfidfTrain)
    
    ''' padding constants to the generated tfidfTrain and tfidfTest '''
    constant = np.ones((len(tfidfTrain), 1))
    tfidfTrain = np.hstack((constant,tfidfTrain))
    constant2 = np.ones((len(tfidfTest), 1))
    tfidfTest = np.hstack((constant2,tfidfTest))
    
    ''' return the data split  '''
    return (tfidfTrain,y_train,tfidfTest,y_test)    
    
def runModel(modelObj):
    print "Enter the file path of the data set to be used: (currently hard coded)"
    #fileName=input()
    
    ''' fetch the data split '''
    X_train,y_train,X_test,y_test=fetchData('../DataSets/FinalDataSet.csv',modelObj)
    
    #Visualize.plotInitalData(X_train,y_train)
    
    ''' fit the Train data '''
    modelObj.fit(X_train,y_train)
    
    ''' predict using test data '''
    pred=modelObj.predict(X_test)
    writeValsToPickleFile(pred,'Prediction-'+modelObj.__class__.__name__)
    writeValsToPickleFile(y_test, 'Actual_data-'+modelObj.__class__.__name__)
    
    print "\nEvaluation on test data:\n"
    ''' Evaluation of testing data and prediction : based on accuracy, precision , recall of the data  '''
    mapResults=Evaluate.precision_recall_evaluation(pred, y_test)
    mapResults['Accuracy']=Evaluate.accuracy(pred,y_test)
    
    print '\n Writing the result to a text file for reference'
    writeResultsToTextFile(mapResults,TITLE[modelObj.__class__.__name__])
    
    print "\nVisualization\n"
    ''' Visualize the output '''
    Visualize.plotScatterGraphForPrediction(pred, y_test,modelObj.__class__.__name__)
    if modelObj.__class__.__name__=='ModelLogisticRegression':
        loss_array = modelObj.loss_array
        writeValsToPickleFile(loss_array, 'loss_data-'+modelObj.__class__.__name__)
        Visualize.loss_vs_iteration_plot(loss_array)    
    
def writeResultsToTextFile(mapResults,model):
    fname="../PerformanceEvaluation/EvaluationReports/"+model+'_Evaluation_Report'+'.txt'
    if os.path.exists(fname):
        os.remove(fname)    
    fileModel=open(fname,'w')
    topic=" Evaluation Report of "+model+" "
    hashLen=90-len(topic)
    hashLen=hashLen/2
    filler="#"*hashLen+topic+"#"*hashLen
    if len(filler)<90:
        filler+="#"
    fileModel.write("#"*90+"\n"+filler+"\n"+"#"*90+"\n\n")
    for results in mapResults:
        fileModel.write(results+": "+str(mapResults[results])+"\n")
    fileModel.close()
    

    
def selectTasks():
    while True:
        print "\nSelect the Model for classification:"
        print "Enter 1 : Logistic Regression"
        print "Enter 2 : Naive Bayes"
        print "Enter 3 : Support Vector Machne Model using SKlearn library"
        print "Enter 4 : Random Forest Model using SKlearn library"
        print "Enter 5 : To exit!!!!"
        options={1:ModelLogisticRegression,
                 2:NaiveBayes,
                 3:svm.SVC,
                 4:RandomForestClassifier}
        print "Enter Your Choice >>> "
        x=input()
        if x==5:
            break
        elif x==4:
            print "Classification on Random Forest Model using SKLearn Library"
            runModel(options[x](n_jobs=2,random_state=0))
        elif x==3:
            print "Classification on Support Vector Machine Model using SKLearn Library"
            parameters={'C' :[0.00001,0.0001,0.001,0.01,0.1,1,10],'kernel':['linear'], 'random_state': [1]}
            svc=svm.SVC(kernel = 'linear', probability = True, random_state = 0)
            roc_auc_scorer = make_scorer(roc_auc_score)
            modelObj = GridSearchCV(svc, parameters, scoring=roc_auc_scorer)
            runModel(modelObj)
        else:
            print "Classification on "+MODEL[x]
            runModel(options[x](PARAMS[x]))
            
def writeValsToPickleFile(data,name):
    
    fName='../DataVisualization/PickleFilesForActualAndPredicted/'+name+'.pickle'
    if os.path.exists(fName):
        os.remove(fName)
    fileIndex=open(fName,'wb')
    pickle.dump(data,fileIndex)
    fileIndex.close()
    
if __name__=='__main__':
    print "Welcome to fake news classifier"
    selectTasks()    