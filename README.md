# Hate Speech Recognition Using Machine Learning

## 📌 Project Overview

Hate Speech Recognition Using Machine Learning is a Django-based web application that identifies whether a given text is **Hateful** or **Not Hateful**.

The system uses **TF-IDF (Term Frequency-Inverse Document Frequency)** for text feature extraction and applies two machine learning classification algorithms:

- Support Vector Machine (SVM)
- Multinomial Naive Bayes

The application provides a web interface where users can enter a sentence and receive predictions from both trained models.

---

## 🚀 Features

- User registration and login
- Admin login and user management
- User activation and deactivation
- Hate speech prediction from text
- SVM-based classification
- Multinomial Naive Bayes classification
- TF-IDF text vectorization
- Model training through the Django application
- Model accuracy display
- Confusion matrix visualization
- Prediction results from both ML models
- Django-based web interface

---

## 🧠 Machine Learning Approach

The project follows these main steps:

```text
Input Text
    ↓
Text Preprocessing
    ↓
TF-IDF Vectorization
    ↓
Machine Learning Models
    ↓
SVM / Naive Bayes
    ↓
Hateful / Not Hateful
