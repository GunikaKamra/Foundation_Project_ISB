#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Creating widgets for the deployement

#Dropdown widget
location = widgets.Dropdown(
    options=['India','United States'],
    value='India',
    description='Location:',
)

job_profile = widgets.Dropdown(
    options=['Data scientist','Software engineer'],
    value='Data scientist',
    description='Job Profile:',
)

#Text Widget
profiles_required = widgets.Text(placeholder='Enter no of profiles',description='# of Profiles:')


LOB = widgets.Dropdown(
    options=['LOB_BFSI','LOB_CSMP','LOB_EAS','LOB_ERS','LOB_ETS','LOB_Healthcare','LOB_INFRA','LOB_MMS'],
    value='LOB_BFSI',
    description='LOB:',
)


Offered_band = widgets.Dropdown(
    options=['Offered_band_E1','Offered_band_E2','Offered_band_E3'],
    value='Offered_band_E1',
    description='CTC Band:',
)

Candidate_ID = widgets.Text(placeholder='Candidate_ID',description='Candidate_ID')

Profile_Link = widgets.Text(placeholder='Profile Link',description='Profile Link')

Duration_to_accept_offer = widgets.Text(placeholder='Duration_to_accept_offer',description='Duration_to_accept_offer')

Notice_period = widgets.Text(placeholder='Notice_period',description='Notice_period')

Percent_difference_CTC = widgets.Text(placeholder='Percent_difference_CTC',description='Percent_difference_CTC')

Rex_in_Yrs = widgets.Text(placeholder='Rex_in_Yrs',description='Rex_in_Yrs')

Companies_Count = widgets.Text(placeholder='Companies_Count',description='Companies_Count')

Proximity_to_Job_Location = widgets.Text(placeholder='Proximity_to_Job_Location',description='Proximity_to_Job_Location')

Age = widgets.Text(placeholder='Age',description='Age')

Match_Score = widgets.Text(placeholder='Match_Score',description='Match_Score')

DOJ_Extended_Yes = widgets.Text(placeholder='DOJ_Extended_Yes',description='DOJ_Extended_Yes')

Joining_Bonus_Yes = widgets.Text(placeholder='Joining_Bonus_Yes',description='Joining_Bonus_Yes')

Candidate_relocate_actual_Yes = widgets.Text(placeholder='Candidate_relocate_actual_Yes',description='Candidate_relocate_actual_Yes')

Gender_Male = widgets.Text(placeholder='Gender_Male',description='Gender_Male')

