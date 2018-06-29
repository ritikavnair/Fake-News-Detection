import math
import numpy as np

class NaiveBayes():
    
    def __init__(self,pp):
        print ""
    
    def fit(self,X,y):
        ''' initialize the model '''
  
        self.X=X[:,1:]
        self.y=y
        self.docCount,self.vocabularyCount = np.shape(self.X)
        #print self.docCount,self.vocabularyCount
        self.categories,self.categoryCount=self.createFeatureDictionary()
        self.featureCount={}
        for classes in self.categories:
            self.featureCount[classes]=len(self.categories[classes])
        self.train()
        
        
            
    def createFeatureDictionary(self):
        
        ''' create dictionary for each class 
            key : class , value = {feature : frequency } ''' 
        
        categories={}
        categoryCount={}
        for yi in np.unique(self.y):
                categories[yi]={}
                categoryCount[yi]=len(self.y[self.y==yi])
        
        #print categoryCount
                    
        for j in range(self.docCount) :    
            for i in range(self.vocabularyCount):
                if self.X[j][i]!=0:
                    if i not in categories[self.y[j]]:
                        categories[self.y[j]][i]=1
                    else:
                        categories[self.y[j]][i]+=1
                else:
                    categories[self.y[j]][i]=0
        
        return categories,categoryCount
        
        
    def train(self):
        
        ''' train the model '''
        
        ''' calculate the prior probabilities
                and conditional probabilities '''
        
        self.priorProbab={}
        self.conditionalProbab={}
        
        for classes in self.categories:
            self.priorProbab[classes]=math.log(self.featureCount[classes]/float(self.docCount))
            self.conditionalProbab[classes]={}
            for features in self.categories[classes]:
                self.conditionalProbab[classes][features]=\
                math.log((self.categories[classes][features] + 1) / ( float( self.featureCount[classes] + self.vocabularyCount ) ) )
        
    
    def predict(self,X_test):
        
        pred=[]
        for xi in X_test:
            pred.append(self.check(xi))
            
        return pred
    
    def check(self,x):
        ''' test the data '''
        docfeatures=[]
        for i in range(len(x)):
            if x[i]!=0:
                docfeatures.append(i)
        
        val={}
        for classes in self.categories:
            val[classes]=self.priorProbab[classes]
        
            
        unseenProbab={}
        for classes in self.categories:
            unseenProbab[classes]=math.log(1/float(self.featureCount[classes]+self.vocabularyCount))
            
        
        for classes in self.categories:
            for feature in docfeatures:
                if feature in self.categories[classes]:
                    val[classes]+=self.categories[classes][feature]
                else:
                    val[classes]+=unseenProbab[classes]  
                    
        sortedMap=sorted(val.iteritems(),key=lambda(k,v):(v,k),reverse=True)
        
        return sortedMap[0][0]
            
if __name__=='__main__':
    
    ''' testing Naive Bayes accuracy '''
    n=NaiveBayes(1)
    X=np.array([[0,0,0,0,0.33,0.121,0.1121,0,0,0,0,0,0,0,0.33,0.121,0.1121,0,0,0],
                [0.134,0,0.111,0.11,0,0.1231,0,0,0,0,0.134,0,0.111,0.11,0,0.1231,0,0,0,0],
                [0,0.11,0,0,0.123,1.111,1.566,0,0.221,0,0,0.11,0,0,0.123,1.111,1.566,0,0.221,0],
                [0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11,0,0.11,0,0,0.123,1.111,1.566,0,0.221,0],
                [0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11,0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11],
                [0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11,0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11],
                [0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11,0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11],
                [0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11,0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11],
                [0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11,0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11],
                [0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11,0,0,0.12,0,0.01,1.111,1.566,0,0.221,0.11]])
    y=np.array([0,1,0,1,1,1,0,0,1,0])
    n.fit(X[:6], y[:6])
    pred=n.predict(X[7:])
    print pred
    print y[7:]
            