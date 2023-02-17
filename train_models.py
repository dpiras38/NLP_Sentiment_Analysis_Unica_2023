from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn import linear_model
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, accuracy_score
from load_dataset import get_data
import joblib
import pickle
import time
import sys

# If train data equal to 1, the models are trained and saved
# We used this to save some time
train_data = 1

if train_data == 1:

    data,labels = get_data()

    # Split of the dataset into train and test
    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(data,labels,test_size=0.3)

    # Label encoding of the labels
    Encoder = LabelEncoder()
    Train_Y = Encoder.fit_transform(Train_Y)
    Test_Y = Encoder.fit_transform(Test_Y)

    # Vectorization of the tweets
    Tfidf_vect = TfidfVectorizer(max_features=5000)
    Tfidf_vect.fit(data)

    # Save the vectorizer
    current_path = sys.path[0]
    filename = current_path + "/vectorizer.pickle"
    pickle.dump(Tfidf_vect, open(filename, "wb"))

    # Transform the tweets into tf-idf vectors
    Train_X_Tfidf = Tfidf_vect.transform(Train_X)
    Test_X_Tfidf = Tfidf_vect.transform(Test_X)

    # Train model with Naive Bayes
    Naive = naive_bayes.MultinomialNB()
    st = time.time()
    Naive.fit(Train_X_Tfidf,Train_Y)
    et = time.time()
    print("Time to train the Naive Bayes model: ", et-st)
    # Predict the labels of the test set
    predictions_NB = Naive.predict(Test_X_Tfidf)
    # Print the classification report
    print("                    Naive Bayes \n",classification_report(predictions_NB, Test_Y))
    print("Naive Bayes Accuracy Score -> ",accuracy_score(predictions_NB, Test_Y)*100)

    # Save the model
    current_path = sys.path[0]
    filename = current_path + "/naive_bayes.joblib"
    joblib.dump(Naive, filename)

    # Train model with SVM
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
    st = time.time()
    SVM.fit(Train_X_Tfidf,Train_Y)
    et = time.time()
    print("Time to train the SVM model: ", et-st)
    predictions_SVM = SVM.predict(Test_X_Tfidf)
    print("                    SVM \n",classification_report(predictions_SVM, Test_Y))
    print(" Accuracy Score -> ",accuracy_score(predictions_SVM, Test_Y)*100)

    filename = current_path + "/svm.joblib"
    joblib.dump(SVM, filename)

    # Train model with Logistic Regression
    LR = linear_model.LogisticRegression(solver = 'liblinear', C=10, penalty = 'l2')
    st = time.time()
    LR.fit(Train_X_Tfidf,Train_Y)
    et = time.time()
    print("Time to train the Logistic Regression model: ", et-st)
    predictions_LR = LR.predict(Test_X_Tfidf)
    print("                    Logistic Regression \n",classification_report(predictions_LR, Test_Y))
    print(" Accuracy Score -> ",accuracy_score(predictions_LR, Test_Y)*100)

    filename = current_path + "/logistic_regression.joblib"
    joblib.dump(LR, filename)




