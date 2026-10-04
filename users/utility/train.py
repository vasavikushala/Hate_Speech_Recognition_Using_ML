# views.py

from django.shortcuts import render
from django.conf import settings
import os
import pandas as pd
from sklearn import model_selection, svm, naive_bayes, metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

def task1_view(request):
    # Read processed data and labels
    path1 = os.path.join(settings.MEDIA_ROOT, 'processed_data_vol2.csv')
    path2 = os.path.join(settings.MEDIA_ROOT, 'class.csv')
    dp = pd.read_csv(path1, encoding='cp1252')
    dc = pd.read_csv(path2, encoding='cp1252')
    
    # Split data into training and testing sets
    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(dp['text_final'], dc['class'], test_size=0.3)
    
    # Encode labels
    Encoder = LabelEncoder()
    Train_Y = Encoder.fit_transform(Train_Y)
    Test_Y = Encoder.fit_transform(Test_Y)
    
    # Vectorize text data
    Tfidf_vect = TfidfVectorizer()
    Tfidf_vect.fit(dp['text_final'])
    Train_X_Tfidf = Tfidf_vect.transform(Train_X)
    Test_X_Tfidf = Tfidf_vect.transform(Test_X)
    
    # Train SVM model
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    SVM.fit(Train_X_Tfidf, Train_Y)
    
    # Train Naive Bayes model
    Naive = naive_bayes.MultinomialNB()
    Naive.fit(Train_X_Tfidf, Train_Y)
    
    # Save models to disk
    svm_filename = 'finalized_model_SVM.sav'
    nb_filename = 'finalized_model_NB.sav'
    pickle.dump(SVM, open(os.path.join(settings.MEDIA_ROOT, svm_filename), 'wb'))
    pickle.dump(Naive, open(os.path.join(settings.MEDIA_ROOT, nb_filename), 'wb'))
    
    # Predict using SVM and Naive Bayes
    predictions_SVM = SVM.predict(Test_X_Tfidf)
    predictions_NB = Naive.predict(Test_X_Tfidf)
    
    # Calculate accuracies
    svm_accuracy = accuracy_score(predictions_SVM, Test_Y) * 100
    nb_accuracy = accuracy_score(predictions_NB, Test_Y) * 100
    
    # Generate confusion matrices
    def generate_conf_matrix(model, predictions):
        mat = confusion_matrix(predictions, Test_Y)
        axis_labels=['Hateful', 'Not Hateful']
        plt.figure(figsize=(6, 4))
        sns.heatmap(mat, square=True, annot=True, fmt='d', cbar=False,
                    xticklabels=axis_labels, yticklabels=axis_labels)
        plt.title(f"{model} Confusion Matrix")
        plt.xlabel('Predicted Categories')
        plt.ylabel('True Categories')
        plt.tight_layout()
        plt.savefig(os.path.join(settings.MEDIA_ROOT, f"{model}_confusion_matrix.png"))
    
    generate_conf_matrix("SVM", predictions_SVM)
    generate_conf_matrix("Naive_Bayes", predictions_NB)
    
    # Prepare context for rendering
    context = {
        'svm_accuracy': svm_accuracy,
        'nb_accuracy': nb_accuracy,
        'svm_conf_matrix': 'finalized_model_SVM_confusion_matrix.png',
        'nb_conf_matrix': 'finalized_model_NB_confusion_matrix.png',
    }
    
    return render(request, 'users/task1.html', context)
