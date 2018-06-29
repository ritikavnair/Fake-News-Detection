import matplotlib.pyplot as plt


TITLE ={"ModelLogisticRegression":"Logistic Regression Model",
        "NaiveBayes":"Naive Bayes Model",
        "GridSearchCV":"Support Vector Machine Model",
        "RandomForestClassifier":"Random Forest Model"}
    

def plotScatterGraphForPrediction(prediction ,y_test,className):
    
    ''' scatter plot '''
    
    #fig=plt.figure()
    plt.ylim(-1, 2)
    ax = plt.subplots(nrows=2, ncols=1, figsize=(7,7))[1]
    plt.title('Fake news vs Real News -> '+TITLE[className])
    ax[0].scatter(xrange(len(prediction)), prediction, color='red')
    ax[0].set_title='Prediction'
    ax[0].plot()
    ax[1].scatter(xrange(len(y_test)), y_test, color='green')
    ax[1].set_title='Actual'
    ax[1].plot()
    #fig.add(ax)
    plt.savefig('../DataVisualization/Plot_Images/'+TITLE[className]+'-scatterPlot.png')
    plt.show()
    
def loss_vs_iteration_plot(loss_array):
    
    '''  plot loss v/s iteration plot '''
            
    plt.title('loss vs iteration')
    plt.plot(xrange(len(loss_array)), loss_array)
    plt.savefig('../DataVisualization/Plot_Images/LossVsIterationPlot.png')
    plt.show()
    