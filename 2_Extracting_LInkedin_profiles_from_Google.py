#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Defining function to fetch linkedin urls

def get_urls(country_name,profile_name):
    Country_name = country_name
    Job_Profile = profile_name
    
    search_query = "site:linkedin.com/in AND" + Job_Profile + " AND " + Country_name
    # Use a try-except block to handle the ImportError
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    
    profile_link = []
    for i, link in enumerate(search(search_query, num=5, stop=5, pause=2)):
        # Check if the link is not already in the list
        if link not in profile_link:
            profile_link.append(link)
            #print(f"{i+1}. {link}")


    # Use pandas to write the list to a CSV file
    column_names = ['LinkedIn_Profile_Links']
    df = pd.DataFrame(profile_link,columns=column_names)
    df['Candidate ID'] = df.index + 100
    df['LinkedIn_Profile_Links'] = df['LinkedIn_Profile_Links'].replace({'in.l': 'www.l'}, regex=True)
    df.to_csv(r'C:\Users\Deepak Gupta\OneDrive - Indian School of Business\Term 2\Foundational Project 1\Group Project\Outputs\linkedin_profile_links.csv',index = False)

    

