#!/usr/bin/env python
# coding: utf-8

# In[ ]:



#defining the function to fetch data from linkedin

def get_scrapped_data():
    
    PAGE_LOAD_TIME_WAIT_SEC = 20
    CALL_WAIT_TIME_SEC = 10

    EXP_PAGE_PATH = "/details/experience"
    SKILLS_PAGE_PATH = "/details/skills"

    INPUT_PROFILES_FILE_PATH = r'C:\Users\Deepak Gupta\OneDrive - Indian School of Business\Term 2\Foundational Project 1\Group Project\Outputs\linkedin_profile_links.csv'
    PROFILE_DF_FILE = r'C:\Users\Deepak Gupta\OneDrive - Indian School of Business\Term 2\Foundational Project 1\Group Project\Outputs\linkedin_profile_dataframe.csv'
    PROFILE_JSON_FILE = r'C:\Users\Deepak Gupta\OneDrive - Indian School of Business\Term 2\Foundational Project 1\Group Project\Outputs\linkedin_profile_json.csv'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # driver.get method() will navigate to a page given by the URL address
    driver.get('https://www.linkedin.com/')

    # locate email form by_class_name
    #username = driver.find_element(By.CLASS_NAME,'input__input')
    username = driver.find_element("name",'session_key')

    # send_keys() to simulate key strokes
    username.send_keys('gunika.kamra.ampba@gmail.com')

    password = driver.find_element("name",'session_password')
    password.send_keys('isb@12345')

    log_in_button = driver.find_element(By.CLASS_NAME,'sign-in-form__submit-button')
    log_in_button.click()
    
    
    
    profile_df = pd.read_csv(INPUT_PROFILES_FILE_PATH)

    #Fetching name from the linkedin profile
    def get_name_from_profile(soup):

        if (soup.find('section', {'class':"artdeco-card ember-view pv-top-card"}) is None):
            return ""

        try:
            name = soup.find('section', {'class':"artdeco-card ember-view pv-top-card"})                .find('div',{'class':'mt2 relative'})               .find('h1',{'class':'text-heading-xlarge inline t-24 v-align-middle break-words'}).string.strip()
            #print(name)
            return name
        except:
            return ""
        
        
#fetching location from the linkedin profile
    def get_location_from_profile(soup):
        location = ""

        if ((soup.find('section', {'class':"artdeco-card ember-view pv-top-card"})) is None):
            return location
        try:
            location = soup.find('section', {'class':"artdeco-card ember-view pv-top-card"})                .find('div',{'class':'mt2 relative'})               .find('div',{'class':'pv-text-details__left-panel mt2'})               .find('span',{'class':'text-body-small inline t-black--light break-words'}).string.strip()
            #print(location)
        except:
            pass

        return location
    

#fetching descritions and about sections
    def get_about_from_profile(soup,text_bagofwords):
        about_text = ""

        try:
            cards =soup.find_all('section', {'class':"artdeco-card ember-view relative break-words pb3 mt2"})
        except:
            return about_text,text_bagofwords

        for card in cards:
            if (card.find('div',attrs={'id':'about'})):
                try:
                    about_div = card.find('div',attrs={'class':'inline-show-more-text inline-show-more-text--is-collapsed full-width'})
                    about_text = re.sub(r'<.*>',"",str(about_div))
                except:
                    pass

        text_bagofwords += about_text
        return about_text, text_bagofwords

    
#fetching education background
    def get_about_education_from_profile(soup,text_bagofwords):

        educ_list = []

        try:
            cards =soup.find_all('section', {'class':"artdeco-card ember-view relative break-words pb3 mt2"})
        except:
            return educ_list

        for card in cards:
            if (card.find('div',attrs={'id':'about'})):
                try:
                    about_div = card.find('div',attrs={'class':'inline-show-more-text inline-show-more-text--is-collapsed full-width'})
                    about_text = re.sub(r'<.*>',"",str(about_div))
                    text_bagofwords += about_text
                except:
                    pass

            if(card.find('div',attrs={'id':'education'})):
                edu_list = card.find_all('li',{'class':'artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column'})

                for edu in edu_list:
                    educ_dict = {}
                    collegename_string = ""
                    degreename_string = ""
                    degreedate_string = ""

                    try:
                        collegename_div = edu.find('div',{'class':'display-flex flex-column full-width align-self-center'})                                        .find('span',{'class':'mr1 hoverable-link-text t-bold'})                                        .find('span',{'class':'visually-hidden'})
                        collegename_string = re.sub('<.*?>',"",str(collegename_div))
                    except:
                        pass

                    try:
                        degreename_div = edu.find('div',{'class':'display-flex flex-column full-width align-self-center'})                                        .find('span',{'class':'t-14 t-normal'})                                        .find('span',{'class':'visually-hidden'})
                        degreename_string = re.sub('<.*?>',"",str(degreename_div))
                    except:
                        pass

                    try:
                        degreedate_div = edu.find('div',{'class':'display-flex flex-column full-width align-self-center'})                                        .find('span',{'class':'t-14 t-normal t-black--light'})                                        .find('span',{'class':'visually-hidden'})
                        degreedate_string = re.sub('<.*?>',"",str(degreedate_div))
                    except:
                        pass

                    educ_dict["Name"]=collegename_string
                    educ_dict["Degree"]=degreename_string
                    educ_dict["Date"]=degreedate_string
                    educ_list.append(educ_dict)

        return about, educ_list, text_bagofwords
    


    #Get Experience List
    def get_experience_from_experience_page(soup,text_bagofwords):
        job_list = []
        total_exp_months = 0
        companies_count = 0

        if(soup.find('section',{'class':'artdeco-card ember-view pb3'})is None):
            return total_exp_months, companies_count, text_bagofwords, job_list

        try:
            exp_list = soup.find('section',{'class':'artdeco-card ember-view pb3'})                    .find('div',{'class':'pvs-list__container'})                    .find_all('li',{'class':'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        except:
            return total_exp_months, companies_count, text_bagofwords, job_list

        companies_count = len(exp_list)
        for job in exp_list:

            #Different layouts depending on whether multiple roles within same company or 1 role in the company
            if (job.find('div',{'class':'display-flex flex-column full-width'})):
                job_dict ={}
                designation = ""
                company = ""
                tenure = ""
                location = ""
                description_string = start_date = end_date = ""

                #Designation field crawled
                try:
                    designation_div = job.find('div',{'class':'display-flex flex-column full-width'})                            .find('span',{'class':'mr1 t-bold'})                            .find('span',{'class':'visually-hidden'})
                    designation = re.sub('<.*?>',"",str(designation_div))
                except:
                    pass
                job_dict["Designation"] = designation

                #Company field crawled
                try:
                    company_div = job.find('div',{'class':'display-flex flex-column full-width'})                                .find('span',{'class':'t-14 t-normal'})                                .find('span',{'class':'visually-hidden'})
                    company = re.sub('<.*?>',"",str(company_div))
                except:
                    pass
                job_dict["Company"] = company

                #Tenure field crawled
                duration_in_months = 0
                try:
                    tenure_div = job.find('div',{'class':'display-flex flex-column full-width'})                                .find('span',{'class':'t-14 t-normal t-black--light'})                                .find('span',{'class':'visually-hidden'})
                    tenure = re.sub('<.*?>',"",str(tenure_div))
                    job_dict["Tenure"] = tenure
                    match = re.search(r'(.*) - (.*) ·(.*)', tenure)
                    if match:
                        start_date = match.group(1)
                        end_date = match.group(2)
                        period = match.group(3)

                        year_match = re.search(r'(\d*) yr.*',period)
                        months_match = re.search(r'(\d*) mo.*',period)

                        if year_match:
                            years = int(year_match.group(1))
                        else:
                            years = 0
                        if months_match:
                            months = int(months_match.group(1))
                        else:
                            months = 0
                        duration_in_months = years * 12 + months
                except:
                    pass

                total_exp_months += duration_in_months
                job_dict["Start Date"]=start_date
                job_dict["End Date"]=end_date
                job_dict["Tenure Months"]=duration_in_months


                #location field crawled
                try:
                    location_div = job.find('div',{'class':'display-flex flex-column full-width'})                                .find('span',{'class':'t-14 t-normal t-black--light'})                                .findNext('span',{'class':'t-14 t-normal t-black--light'})                                .find('span',{'class':'visually-hidden'})
                    location = re.sub('<.*?>',"",str(location_div))
                    location_list = location.split(",")
                    job_dict["Location"] = location
                    job_dict["City"]=location_list[0]
                except:
                    pass
                location_list = location.split(",")
                job_dict["Location"] = location
                job_dict["City"]=location_list[0]
                if(len(location_list)>=2):
                    job_dict["State"]=location_list[1]
                else:
                    job_dict["State"]=""
                if(len(location_list)>=3):
                    job_dict["Country"]=location_list[2]
                else:
                    job_dict["Country"]=""

                #Details of job description crawled
                try:
                    description_div = job.find('ul',{'class':'pvs-list'})                                 .find_all('div',{'class':'pvs-list__outer-container'})
                    description_string = start_date = end_date = ""
                    for describe in description_div:
                        try:
                            describe_div = describe.find('div',{'class':'display-flex full-width'})                                       .find('div',{'class':'display-flex align-items-center t-14 t-normal t-black'})                                       .find('span',{'class':'visually-hidden'})
                            description_string +=  re.sub('<.*?>',"",str(describe_div))
                        except:
                            pass       
                except:
                    pass
                job_dict["Description"] = description_string
                job_list.append(job_dict)
                text_bagofwords += designation+" "+description_string

            else:
                #Else loop for match with multiple roles in the same company
                company_div = job.find('div',{'class':'display-flex flex-column full-width align-self-center'})                                .find('span',{'class':'mr1 hoverable-link-text t-bold'})                                .find('span',{'class':'visually-hidden'})
                company = re.sub('<.*?>',"",str(company_div))

                role_list = job.find('div',{'class':'pvs-list__outer-container'})                            .find('ul',{'class':'pvs-list'})                            .find_all('div',{'class','display-flex flex-column full-width align-self-center'})


                for role in role_list:
                    job_dict ={}
                    designation_div = role.find('span',{'class':'mr1 hoverable-link-text t-bold'})                                .find('span',{'class':'visually-hidden'})
                    designation = re.sub('<.*?>',"",str(designation_div))

                    tenure_div = role.find('span',{'class':'t-14 t-normal t-black--light'})                                    .find('span',{'class':'visually-hidden'})
                    tenure = re.sub('<.*?>',"",str(tenure_div))
                    match = re.search(r'(.*) - (.*) ·(.*)', tenure)
                    if match:
                        start_date = match.group(1)
                        end_date = match.group(2)
                        period = match.group(3)

                        year_match = re.search(r'(\d*) yr.*',period)
                        months_match = re.search(r'(\d*) mo.*',period)

                        if year_match:
                            years = int(year_match.group(1))
                        else:
                            years = 0
                        if months_match:
                            months = int(months_match.group(1))
                        else:
                            months = 0

                        duration_in_months = years * 12 + months
                    else:
                        duration_in_months = 0
                        start_date = end_date = ""

                    total_exp_months += duration_in_months

                    try:
                        location_div = role.find('span',{'class':'t-14 t-normal t-black--light'})                                    .findNext('span',{'class':'t-14 t-normal t-black--light'})                                    .find('span',{'class':'visually-hidden'})
                        location = re.sub('<.*?>',"",str(location_div))
                    except:
                        pass

                    try:
                        describe_div = role.find('ul',{'class':'pvs-list'})                                           .find('div',{'class':'pvs-list__outer-container'})                                           .find('div',{'class':'display-flex full-width'})                                           .find('div',{'class':'display-flex align-items-center t-14 t-normal t-black'})                                           .find('span',{'class':'visually-hidden'})
                        description_string =  re.sub('<.*?>',"",str(describe_div))
                    except:
                        description_string = ""
                    job_dict["Company"]=company
                    job_dict["Designation"]=designation
                    job_dict["Start Date"]=start_date
                    job_dict["End Date"]=end_date
                    job_dict["Tenure Months"]=duration_in_months
                    job_dict["Tenure"]=tenure
                    job_dict["Location"]=location

                    location_list = location.split(",")
                    job_dict["Location"] = location
                    job_dict["City"]=location_list[0]
                    if(len(location_list)>=2):
                        job_dict["State"]=location_list[1]
                    else:
                        job_dict["State"] = ""
                    if(len(location_list)>=3):
                        job_dict["Country"]=location_list[2]
                    else:
                        job_dict["Country"]=""
                    job_dict["Description"]=description_string
                    text_bagofwords += designation+" "+description_string
                    job_list.append(job_dict)



        return total_exp_months, companies_count, text_bagofwords, job_list  
    

    #Code to get Skills from skills page
    def get_skills_from_skills_page(soup,text_bag_of_words):
        skill_string_list = []
        skillname_string = ""

        if(soup.find('ul',{'class':'pvs-list'}) is None):
            return skill_string_list,text_bag_of_words

        try:
            skills_list = soup.find('ul',{'class':'pvs-list'})                       .find_all('li',{'class':'pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated'})
        except:
            return skill_string_list,text_bag_of_words

        for skill in skills_list:  
            skillname_div = skill.find('div',{'class':'display-flex flex-column full-width align-self-center'})                            .find('div',{'class':'display-flex align-items-center'})                            .find('span',{'class':'mr1 hoverable-link-text t-bold'})                            .find('span',{'class':'visually-hidden'})
            skillname_string = re.sub('<.*?>',"",str(skillname_div))
            text_bag_of_words += " "+skillname_string
            skill_string_list.append(skillname_string)

        return skill_string_list,text_bag_of_words

#appending and merging all the fetched data into one dataframe
    for i,row in profile_df.iterrows():
        profile_dict = {}
        profile_df_row = []
        text_bagofwords = ""
        about =""
        educ_list = []
        profilecrawl_df = pd.DataFrame([],columns=['Candidate_ID','ProfileLink','Name','City','State','Country','Total_Experience_Months',                                              'Companies_Count','Text_BagofWords','skills_list'])   

        profile_link = row['LinkedIn_Profile_Links']

        profile_dict["Candidate_ID"] = row['Candidate ID']
        profile_dict["Profile_Link"] = profile_link

        #Load the Main Profile Page of the candidate
        time.sleep(CALL_WAIT_TIME_SEC)
        driver.get(profile_link)
        time.sleep(PAGE_LOAD_TIME_WAIT_SEC)
        html = driver.page_source
        soup = BeautifulSoup(html)


        #Load and Crawl the Main Profile Page of the candidate to get Name, Location, About, Education
        profile_dict["Name"] = get_name_from_profile(soup)

        profile_dict["Location"] = get_location_from_profile(soup)
        profile_dict["City"] = profile_dict["Location"].split(',')[0]
        #profile_dict["State"] = profile_dict["Location"].split(',')[1]
        profile_dict["Country"] = profile_dict["Location"].split(',')[-1]


        about, educ_list, text_bagofwords = get_about_education_from_profile(soup, text_bagofwords)
        profile_dict["About"] = about
        profile_dict["Education"] = educ_list


        #Load and Crawl the Experience Page of the candidate
        time.sleep(CALL_WAIT_TIME_SEC)
        experience_page=profile_link+EXP_PAGE_PATH
        driver.get(experience_page)
        time.sleep(PAGE_LOAD_TIME_WAIT_SEC)
        html = driver.page_source
        soup = BeautifulSoup(html)

        total_exp_months, companies_count, text_bagofwords, job_list = get_experience_from_experience_page(soup,text_bagofwords)
        profile_dict["Total_Experience_Months"] = total_exp_months
        profile_dict["Companies_Count"] = companies_count
        profile_dict["Experience"] = job_list

        #Load and Crawl the Skills Page of the candidate
        time.sleep(CALL_WAIT_TIME_SEC)
        skills_page=profile_link+SKILLS_PAGE_PATH
        driver.get(skills_page)
        time.sleep(PAGE_LOAD_TIME_WAIT_SEC)
        html = driver.page_source
        soup = BeautifulSoup(html)

        skills_list, text_bagofwords = get_skills_from_skills_page(soup,text_bagofwords)
        profile_dict["Skills"] = skills_list



        #Append the Profile Dict json in file
        with open(PROFILE_JSON_FILE, 'a', encoding ='utf8') as json_file:
            json.dump(profile_dict, json_file, ensure_ascii = False,separators=(",",":"))

        #Append the Profile df in the file    
        profilecrawl_df.loc[0, 'Candidate_ID'] = profile_dict['Candidate_ID']
        profilecrawl_df.loc[0, 'ProfileLink'] = profile_dict['Profile_Link']
        profilecrawl_df.loc[0, 'Name'] = profile_dict['Name']
        profilecrawl_df.loc[0, 'City'] = profile_dict['City']
        #profilecrawl_df.loc[0, 'State'] = profile_dict['State']
        profilecrawl_df.loc[0, 'Country'] = profile_dict['Country']
        profilecrawl_df.loc[0, 'Total_Experience_Months'] = total_exp_months
        profilecrawl_df.loc[0, 'Companies_Count'] = profile_dict['Companies_Count']
        profilecrawl_df.loc[0, 'Text_BagofWords'] = text_bagofwords
        profilecrawl_df.loc[0, 'skills_list'] = profile_dict["Skills"]


        profilecrawl_df.to_csv(PROFILE_DF_FILE, mode='a', index=False, header=True)

