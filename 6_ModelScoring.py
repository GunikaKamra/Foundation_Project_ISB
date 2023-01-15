#!/usr/bin/env python
# coding: utf-8

# In[ ]:



#created a pickel to call the model
def prediction(X):
    with open(r'C:\Users\Deepak Gupta\OneDrive - Indian School of Business\Term 2\Foundational Project 1\Group Project\model1.pkl', 'rb') as f:
        clf2 = pickle.load(f)

    clf2.predict(X[0:1])
    if (clf2.predict(X[0:1])[0]) == 1:
        print("Candidate will accept the offer")
    else:
        print("Candidate will most probably reject the offer")

