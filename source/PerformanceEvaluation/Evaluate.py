import numpy as np
  
def accuracy(pred,y_test):
    
    '''  compute accuracy  '''
    
    prediction=np.array(pred).astype(int)
    y_test=np.array(y_test).astype(int)
    count=0
    for i in range (0,len(y_test)):
        if prediction[i]==y_test[i]:
            count+=1
    accuracy=(count/float(len(y_test)))
    print "Accuracy on prediction :",accuracy
    
    return accuracy
    
    
def precision_recall_evaluation(prediction, y_test):
    
    ''' calculate precision, recall '''
    
    true_positive = 0;
    false_positive = 0;
    false_negative = 0;
    true_negative = 0;
    
    for index in range(len(prediction)):
        if y_test[index] == 1 and prediction[index] == 1:
            true_positive += 1
        elif y_test[index] == 0 and prediction[index] == 1:
            false_positive += 1
        elif y_test[index] == 1 and prediction[index] == 0:
            false_negative += 1
        else:
            true_negative+=1
            
    ''' confusion matrix data  '''
            
    print('True Positive', true_positive)
    print('False Positive', false_positive)
    print('False Negative', false_negative)
    print('True Negative', true_negative)
 
    precision = true_positive / (float) (true_positive + false_positive)
    recall = true_positive / (float) (true_positive + false_negative)
    
    print 'Precision: {0:0.2f}'.format(precision)
    print 'Recall: {0:0.2f}'.format(recall)
    
    reportResults={'True Positive':true_positive,
                   'True Negative':true_negative,
                   'False Positive':false_positive,
                   'False Negative':false_negative,
                   'Precision':'{0:0.2f}'.format(precision),
                   'Recall': '{0:0.2f}'.format(recall)}
    return reportResults