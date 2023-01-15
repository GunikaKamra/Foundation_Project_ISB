#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def text_maching(profile_name):
    Script = pd.read_csv(r'C:\Users\Deepak Gupta\OneDrive - Indian School of Business\Term 2\Foundational Project 1\Group Project\Outputs\linkedin_profile_dataframe.csv')
    #Converting text to lower case
    
    Script['skills_list']=Script['skills_list'].str.lower()
    # # removing punctuation
    Script['skills_list']=Script['skills_list'].astype(str).apply(lambda text: re.sub(r'[^\w\d\s]','',text))
    
    import nltk
    nltk.download('stopwords')
    # Import stopwords with nltk.
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    
    Script['skills_list'] = Script['skills_list'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

    Script['skills_list']=Script['skills_list'].replace("Skills","")
    
    
    
    if profile_name == profile_name:
        Script['DATA_SCIENCE_REQUIRED_JD']="'Artificial Intelligence (AI)', 'Analytics', 'SAS', 'R', 'Microsoft Excel',  'Business Intelligence', 'Machine Learning', 'Strategy analytics', 'Analytical Skills', 'Campaign Management', 'Modeling',  'Building Automation', 'Python',  'Flask',  'Deep Learning', 'Django', 'API', 'Deployment', 'Artificial Intelligence', 'Machine Learning', 'Data Mining', 'Pattern Recognition', 'Algorithms', 'Analytics', 'Text Mining', 'MapReduce', 'Information Retrieval', 'Statistical Modeling', 'Big Data', 'Predictive Analytics', 'Optimization', 'Distributed Systems', 'Natural Language Processing', 'Image Processing', 'Computer Vision', 'Recommender Systems', 'Statistics', 'Time Series Analysis','NLP','AWS Glue', 'AWS Lambda', 'Amazon S3', 'Python (Programming Language)'"
    else:
        Script['DATA_SCIENCE_REQUIRED_JD']="'Software', 'Engineer','Java','C++','C'"
        
        
    #Converting text to lower case
    Script['DATA_SCIENCE_REQUIRED_JD']=Script['DATA_SCIENCE_REQUIRED_JD'].str.lower()
    # # removing punctuation
    Script['DATA_SCIENCE_REQUIRED_JD']=Script['DATA_SCIENCE_REQUIRED_JD'].astype(str).apply(lambda text: re.sub(r'[^\w\d\s]','',text))
    Script['DATA_SCIENCE_REQUIRED_JD']= Script['DATA_SCIENCE_REQUIRED_JD'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
    
    
    # Match_Test=[Script['skills_list'],Script['skills_list_wo_stp']]
    Script["Match_key_word"] = Script.apply(lambda x: " ".join(i for i in x["DATA_SCIENCE_REQUIRED_JD"].split() if i in x["skills_list"]),axis=1) 

    Script["Matched_wrds"] = Script["Match_key_word"].apply(lambda n: len(n.split()))
    
    Script["Total_wrds"] = Script["DATA_SCIENCE_REQUIRED_JD"].apply(lambda n: len(n.split()))
    
    Script["Percent_match"] = Script["Matched_wrds"]/Script["Total_wrds"]
    
    #Filter where match perecent is greater than 20%
    Script = Script[Script['Percent_match'] >= 0.05] 
    
    Script.to_csv(r'C:\Users\Deepak Gupta\OneDrive - Indian School of Business\Term 2\Foundational Project 1\Group Project\Outputs\Shortlisted_profiles.csv', header=True, index=False)
    
    Script_output = Script[['Candidate_ID','ProfileLink','Name','Percent_match']]
    print(tabulate(Script_output,headers = 'keys',tablefmt = 'psql'))
    #print(Script_output)

