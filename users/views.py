from django.shortcuts import render

# Create your views here.

def UserHomePage(request):
    return render(request, 'users/userhome.html')

#-----------------------------------------------------------------------------------------------------

def Task1(request):
    return render(request, 'users/task1.html')

#-----------------------------------------------------------------------------------------------------

def ConfusionMatrice(request):
    return render(request, 'users/confusion_matrix.html')

#------------------------------------------------------------------------------------------------------

 
#-------------------------------------------------------------------------------------------------------
# views.py
from django.shortcuts import render
from django.http import HttpResponse
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from .forms import HateSpeechForm
from django.conf import settings
import os

svm_path = os.path.join(settings.MEDIA_ROOT,'finalized_model_SVM.sav')
nb_path = os.path.join(settings.MEDIA_ROOT,'finalized_model_NB.sav')
# Load the models and vectorizer
loaded_model_svm = pickle.load(open(svm_path, 'rb'))
loaded_model_nb = pickle.load(open(nb_path, 'rb'))


data_path = os.path.join(settings.MEDIA_ROOT,'processed_data_vol2.csv')
# Load the processed data to fit the vectorizer
dp = pd.read_csv(data_path, encoding='cp1252')

# Fit the Tfidf Vectorizer
Tfidf_vect = TfidfVectorizer()
Tfidf_vect.fit(dp['text_final'])

def hate_speech_predictor(request):
    if request.method == 'POST':
        form = HateSpeechForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['sentence']
            new_input = [user_input]
            new_input_Tfidf = Tfidf_vect.transform(new_input)

            # SVM prediction
            new_output_svm = loaded_model_svm.predict(new_input_Tfidf)
            # Naive Bayes prediction
            new_output_nb = loaded_model_nb.predict(new_input_Tfidf)

            predictions = {
                'user_input': user_input,
                'svm_prediction': 'Hateful' if new_output_svm == 0 else 'Not Hateful',
                'nb_prediction': 'Hateful' if new_output_nb == 0 else 'Not Hateful',
            }

            return render(request, 'users/hate_speech_result.html', {'predictions': predictions})
    else:
        form = HateSpeechForm()

    return render(request, 'users/hate_speech_form.html', {'form': form})
