############################################################################################################
####################################        FINAL PROJECT        ###########################################
############################################################################################################

 GOAL: Detection of Fake News using various Machine Learning Classifier algorithms and evaluation of their 
	   performance

 SUBMISSION SUMMARY:

 Task 1: Generation of DataSet

		> A. The News Aggregator Dataset from the UCI Machine Learning Repository was used to extract real 
		     news. This dataset consists of links to the originally published news articles in their websites.
			 We extracted these URLS and crawled them to download the news content using Beauti-fulSoup.
		> B. For fake news we used Kaggle’s ‘Getting Real about Fake News’ dataset.
			 The CSV file with data was available off the shelf for use, and we had to perform minimal text
			 pro-cessing on this data.
		  
 Task 2: Implementation of Classifier Algorithms:

		> A. Implemented Logistic Regression Algorithm from scratch and test it against the dataset.
		> B. Implemented Naive Bayes Classifier Algorithm from scratch and test it against the dataset.
		> C. Implemented Random Forest Classifier Algorithm using 'scikit-learn' library and integrate it with 
		     our data set.
		> D. Implemented Support Vector Machine Classifier Algorithm using 'scikit-learn' library and integrate 
		     it with our data set.

 Task 3: Implementation of Evaluation Measure:
 	  
 	  	> A. Implemented methods to calculate accuracy of the prediction algorithms.
		> B. Implemented methods to calculate precision of the prediction algorithms.
		> C. Implemented methods to calculate recall of the prediction algorithms.

Task 4: Implementation of Data Visualization code via graph plots:
	
		> A. Implemented methods to plot iteration vs loss graph for Logistic Regression.
		> B. Implemented methods to generate scatter plot of predictions and actual results against data set.
 	  

		
############################################################################################################	

 INSTALLATION GUIDE:

		> Download Python 2.7 from : "https://www.python.org/download/releases/2.7/"
		> Set Environment variables for Python [for detailed steps refer : 
		  "https://docs.python.org/2/using/windows.html" ]
		> Install BeautifulSoup  by the following the below steps:
		       1. Open command prompt (cmd) in Windows.
		       2. Run Command : 'pip install BeautifulSoup4'
			   3. Run Command : 'pip install sklearn'
			   4. Run Command : 'pip install pandas'
			   5. Run Command : 'pip install numpy'
			   6. Run Command : 'pip install matplotlib'
			   7. Run Command : 'pip install nltk'
		       
#############################################################################################################


 STEPS TO RUN PROGRAM:

		> Open Command Prompt in Windows
		> Go to the directory {localpath}/FakeNews/ModelRun
		> Run the command:
			python Driver.py
		> Follow the instructions as shown in the command prompt
		     