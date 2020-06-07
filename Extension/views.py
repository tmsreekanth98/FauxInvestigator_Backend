from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Analysis
from .serializers import AnalysisSerializer
import os
from django.conf import settings

#ML related imports
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
import mord
from scipy.sparse import coo_matrix, hstack,csr_matrix

from random import uniform

# Create your views here.


class AnalysisMethods(APIView):

	def get(self,request):
		#Get request handler
		pass



	def post(self,request):
		#post request handler
		
		#Parse the request body
		text = request.data['text']
		author = request.data['author']
		heading = request.data['heading']
		source = request.data['source']


		#Pre process the input request. Currently using TFIDF approach
		temp_list = [text,heading,author,"","",""]
		temp_list[0] = re.sub('[^a-zA-z]',' ',temp_list[0]).lower()
		temp_list[1] = re.sub('[^a-zA-z]',' ',temp_list[1]).lower()
		temp_list[2] = re.sub('[^a-zA-z]',' ',temp_list[2]).lower()

		print("--------------------")
		print(author)
		print(text)
		print(source)
		
		

		#Error handling
		if text == "":
			db_entry = Analysis()
			db_entry.text = text
			db_entry.heading = heading
			db_entry.author = author
			db_entry.source = source
			db_entry.label = -1

			db_entry.save()

			#Serialize & return response
			curr_serializer = AnalysisSerializer(db_entry)

			return Response(curr_serializer.data)


		ps = PorterStemmer() #Optionally use stemming for performance enhancement

		#Preprocessing phase
		fin_row = ""
		for item in temp_list:
			row = item.split()
			row = [word for word in row if not word in set(stopwords.words('english'))]
			#row = [ps.stem(word) for word in row if not word in set(stopwords.words('english'))]
			row = ' '.join(row)
			fin_row = fin_row.rstrip() + ' ' + row.lstrip()





		#Load the dumped models to build ensemble
		
		file_paths = ['ord_at_model.p','lr_model.p','svm_model.p']
		class_probability = []
		all_predictions = []

		#Take into account results of all the above models
		for model_path in file_paths:
			path = os.path.join(settings.BASE_DIR,model_path)

			with open(path, 'rb') as pickled:
				data = pickle.load(pickled)

			classifier = data['classifier']
			vectorizer = data['vectorizer']


			#Transformation & Classification phase
			X = vectorizer.transform([fin_row]).toarray()

			#Giving credit history score based on history of source
			if source in ['CNN','TOI']:
				r = uniform(0,0.6)
				CS = np.array([[r]])
			else:
				r = uniform(0.3,1)
				CS = np.array([[r]])	

			
			X = hstack([csr_matrix(X),CS]).toarray()
			print(X.shape)
			
			prediction = classifier.predict(X)

			#Obtain class probabilities
			try:
				probabilities = classifier.predict_proba(X)
				class_probability.append(probabilities[0])
				print(probabilities[0])
			except:
				pass

			#Taking expected value of Logistic regression Model
			# if model_path == 'lr_model.p':
			# 	pred = 0
			# 	for i,x in enumerate(probabilities[0]):
			# 		pred = pred + ((i+1)*x)
			# 	print(int(round(pred)))
			# 	all_predictions.append(int(round(pred)))
			# else:
			
			print(prediction[0])
			all_predictions.append(prediction[0]+1)
				

		class_probability_final = np.mean([class_probability[1],class_probability[0]],axis=0)

		pants_on_fire = round(class_probability_final[0],3)
		false = round(class_probability_final[1],3)
		barely_true = round(class_probability_final[2],3)
		half_true = round(class_probability_final[3],3)
		mostly_true = round(class_probability_final[4],3)
		true = round(class_probability_final[5],3)


		prediction_final = int(round(np.mean(all_predictions)))
		print(all_predictions)
		#prediction_final = np.bincount(np.array(all_predictions)).argmax()


		print("-------------------------")
		print("Output Label: ",prediction_final)
		print("Class probabilities: ",class_probability_final)
		print("-------------------------\n\n\n")


		#Save the entry in DB
		db_entry = Analysis()
		db_entry.text = text
		db_entry.heading = heading
		db_entry.author = author
		db_entry.source = source
		db_entry.label = prediction_final
		db_entry.pants_on_fire = pants_on_fire
		db_entry.false = false
		db_entry.barely_true = barely_true
		db_entry.half_true = half_true
		db_entry.mostly_true = mostly_true
		db_entry.true = true

		db_entry.save()

		#Serialize & return response
		curr_serializer = AnalysisSerializer(db_entry)

		return Response(curr_serializer.data)


