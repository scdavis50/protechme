#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Python3
import re
import random
import pypdftk as pdf
from fdfgen import forge_fdf
import os


# In[2]:


reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}


# In[3]:


questions = {
    #po application
    "What is your full name?",
    "You told me that your name is {0}, is that correct?",
    "What is your phone number?",
    "What is your email address?",
    "What is your home address?",
    "Who do you want protection from (the respondent)?",
    "Does that person live with you?(Yes/No)",
    "What is the respondent's address?",
    "Are you and the respondent members of the same family?(Yes/No)",
    "Are you and the respondent married or used to be married?(Yes/No)",
    "Are you and the respondent dating?(Yes/No)",
    "Do you and the repondent have a child or children together(Yes/No)?",
    "Are you an adult asking for protection for children?(Yes/No)",
    "How many children do you want to protect?(up to ten children)",
    "What is the name of the first child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the second child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the third child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the fourth child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the fifth child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the sixth child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the seventh child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the eighth child you want to protect?", 
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the ninth child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "What is the name of the tenth child you want to protect?",
    "Is the respondent their biological parent(Yes/No)?",
    "What is their address?",
    "Are the children members of your family or household?(Yes/No)",
    "Is there a court order affecting access to the children?",
    "Are there other adults needing protection?",
    "How many adults do you want to protect?(up to two adults)",
    #start here
    "Are there other cases including you, the respondent, the children, or the other adults?(Yes/No)",
    "If so what kind of case is it and is it completed or active?",
    "Do you have a copy of the final order?(Yes/No)",
    "Will a copy of the final order be filed before the hearing?(Yes/No)",
    "Has the respondent commited family violence or is the respondent likely to commit family violence in the future?(Yes/No)",
    "Has the respondent violated a protective order that has expired or will expire in thirty days or less?(Yes/No)",
    "If so do you have a copy of the previous order with you?(Yes/No)",
    "Will a copy of the final order be filed before the hearing?(Yes/No)",
    "Do you want the respondent to not commit any family violence to any of the people previously named?(Yes/No)",
    "Do you want the respondent to not communicate in a threatening or harrassing manner with any of the people previously named?(Yes/No)", 
    "Do you want the respondent not to communicate a threat through any person to any person named previously?(Yes/No)",
    "Do you want the respondent not to communicate in any manner with you?(Yes/No)", 
    "Do you want the respondent not to communicate in any manner with the children?(Yes/No)",
    "Do you want the respondent not to communicate in any manner with the other adults previously named?(Yes/No)",
    "Is it okay if the respondent talks directly to you?",
    "Who can the respondent communicate with you through?",
    #200 yds
    "Would you like the respondent to stay at least two hundred yards away from you?(Yes/No)",
    "Would you like the respondent to stay at least two hundred yards away from the children?(Yes/No)",
    "Would you like the respondent to stay at least two hundred yards away from the other adults?(Yes/No)",
    "Would you like the respondent to stay at least two hundred yards away from the residence, workplace, or school of you?(Yes/No)",
    "Would you like the respondent to stay at least two hundred yards away from the residence, workplace, or school of the other adults previously named?(Yes/No)",
    "Would you like the respondent to stay at least two hundred yards away from the children's residence, childcare facility or school except as specifically authorized in a possession schedule authorized by the Court?(Yes/No)",
    "Would you like the respondent not to stalk, follow or engage in conduct directed specifically to anyone named previously that is reasonably likely to harrass, annoy, alarm, abuse, torment, or emmbarrass them?(Yes/No)",
    "Would you like the court to suspend any license to carry a concealed handgun issued to the respondent under state law?(Yes/No)",
    "Would you like the court to require the respondent to complete a battering interention and prevention program?(Yes/No)",
    "If a program is not avalible, would you like the respondent to complete counseling with a social worker, family service agency, phisician, cycoligist, licensed therapist, or professional counselor?(Yes/No)",
    "Would you like the respondent to pay for all of the therapy or counseling?(Yes/No)",
    "Would you like the court to require the respondent to follow these provisions to prevent or reduce the likelyhood of family violence?(Yes/No)",
    "Do you own or lease your house together?(Yes/No)",
    "Do you own or lease you house alone?(Yes/No)",
    "Is your house owned or leased by the respondent?(Yes/No)",
    "Is the respondent obligated to support you and your children(if you have any)?(Yes/No)",
    "Would you like the respondent to move out?(Yes/No)",
    "Would you like a law inforcement officer to accompany you to your house?(Yes/No)",
    "Would you like a law inforcement officer to tell the respondent that the Court has ordered them to move out?(Yes/No)",
    "Would you like a law inforcement officer to provide protection while the respondent moves out?(Yes/No)",
    "If the respondent refuses to move out, would it be okay if the law inforcement office to remove the respondent and arrest him for violating the Court's order?(Yes/No)",
    "Would you like to have exclusive use of the property that you and the respondent own or lease together?(Yes/No)",
    "Should the respondent be prevented from using the property that you and the respondent own together?(Yes/No)",
    "Would you like the respondent to support you financially?(Yes/No)",
    "Should the respondent not take the children from their child-care facility except when authorized by the Court?(Yes/No)",
    "Should the respondent not take the children to a place where the Court can't order the respondent to bring them back?(Yes/No)",
    "Would you like make a schedule for the Respondent to tak ecare of the children with conditions to keep you and the children safe?(Yes/No)",
    "Would you like to require the Respondent to pay for child support in an amount set by the court?(Yes/No)",
    "Would you like an Ex Parte order where the respondent has to move out immediatly?(Yes/No)",
    "Would youu like the Court to keep your contact information confidiential?",
    "Would you like the respondent to pay all of the costs for service, process and resonable attorneys' fees?(Yes/No)",
    "Do you have a fax number? If you do, please tell me it.",
    "What is your birthdate?(MM/DD/YYYY)",
    "What happened the last time that the respondent hurt you or threatened to hurt you?",
    "What was the date the last time the respondent hurt you or threatened to hurt you?",
    "Did they use a weapon?(Yes/No)",
    "What kind of weapon?",
    "Were there any children involed?(Yes/No)",
    "Which children were involved?",
    "Did you call the police?(Yes/No)",
    "What happened after you called the police?",
    "Did you get medical care?(Yes/No)",
    "Will you describe your injuries?",
    "Has the respondent hurt or threaten to hurt you before?(Yes/No)",
    "Describe what happened and include dates.(MM/DD/YYYY)",
    "Were weapons involved?(Yes/No)",
    "What kind of weapon?",
    "Were there any children there?(Yes/No)",
    "Which children were involved?",
    "Have ever called the police before?(Yes/No)",
    "Did you ever recieve medical care?(Yes/No)",
    "Will you describe you injuries?",
    "Has the respondent ever found guilty of family violence?(Yes/No)",
    "List when and where it took place.",
    #temp ex parte
    #protection order
    #already have information/court fills out
    #respondent information
    "Does the respondent have a nickname?",
    "What is your relationship with the respondent?",
    "Is the respondent a girl or boy?",
    "How tall is the respondent?",
    "How heavy is the respondent?",
    "When was the respondent born?",
    "Where was the repondent born?",
    "What is the respondent's social security number?",
    "What is the respondent's drivers license number?",
    "What is the respondent's other ID number?",
    "What state is the respondent's ID from?",
    "When does the respondent's ID expire?",
    "What is the respondent's race?",
    "What is the respondent's eye color?",
    "What is the respondent's hair color?",
    "What color is the respondent's skin?",
    "Does the respondent have a beard?(Yes/No)",
    "Does the respondent wear glasses?(Yes/No)",
    "Does the respondent have a mustache?(Yes/No)",
    "Is the respondent bald?(Yes/No)",
    "Does the respondent have any missing front teeth?(Yes/No)",
    "Does the respondent have any tattos? If so, please describe them.",
    "Does the respondent have any unusual scars? If so, please describe them.",
    "Does the respondent have any unusual markings? If so, please describe them.",
    "Does the respondent have any unusual piercings? If so, please decribe them.",
    "Does the respondent have any mental problems? If so, please describe them.",
    "Does the respondent have any drug or alcohol problems? If so, please decribe them.",
    "Does the respondent own any weapons? If so, which kinds?",
    "Where does the respondent work?",
    "What is the respondent's vehicle ID number?",
    "What color is the respondent's car?",
    "What kind of car does the respondent have?",
    "What year is the respondent's car model from?",
    "Who is the respondent's attorney?",
    "What is the responedent's attorney's phone number?",
    "What is the respondent's license plate number?",
    "What state is the respondent's license plate from?",
    "When does the respondent's license plate expire?",
    "Are there any other contacts that may have information on the respondent?(Yes/No)",
    "How many contacts are there?(1/2)",
    "What is the full name of the first person?",
    "What is the phone number of the first person?",
    "What is the first person's address?",
    "What is the first person's relationship with the respondent?",
    "Is there any other information on the first person?",
    "What is the full name of the second person?",
    "What is the phone number of the second person?",
    "What is the second person's address?",
    "What is the second person's relationship with the respondent?",
    "Is there any other information on the second person?",
}


# In[4]:


answers = {}

#questions code names
a = 0
while a < 1:
    answers = {}
    applicant = input("What is your full name? ")
    phone = input("What is your phone number? ")
    email = input("What is your email address? ")
    applicant_address = input("What is your home address? ")
    respondent = input("Who do you want protection from?(the respondent) ")
    lives_with = input("Does that person live with you?(Yes/No) ")
    if lives_with.lower() == "no":
        respondent_address = input("What is the respondent's address? ")
    else: 
        respondent_address = applicant_address
    same_family = input("Are you and the respondent members of the same family?(Yes/No) ")
    married = input("Are you and the respondent married or used to be married?(Yes/No) ")    
    if married.lower() == "no":
        dating = input("Are you and the respondent dating or were previously dating?(Yes/No) ")
    else:
        dating = "no"
    children = input("Do you and the repondent have a child or children together?(Yes/No) ")
    
    #start of children's section
    #fix undefined/memory
    protecting_children = input("Are you an adult asking for protection for children?(Yes/No) ")
    if protecting_children.lower() == "no":
        number_children = 0
        child1_name = "none"
        child1_parent = "none"
        child1_address = "none"
        child2_name = "none"
        child2_parent = "none"
        child2_address = "none"
        child3_name = "none"
        child3_parent = "none"
        child3_address = "none"
        child4_name = "none"
        child4_parent = "none"
        child4_address = "none"
        child5_name = "none"
        child5_parent = "none"
        child5_address = "none"
        child6_name = "none"
        child6_parent = "none"
        child6_address = "none"
        child7_name = "none"
        child7_parent = "none"
        child7_address = "none"
        child8_name = "none"
        child8_parent = "none"
        child8_address = "none"
        child9_name = "none"
        child9_parent = "none"
        child9_address = "none"
        child10_name = "none"
        child10_parent = "none"
        child10_address = "none"
    else:
        number_children = input("How many children do you want to protect?(up to ten children) ")
        if int(number_children) != 0:
            for c in range(int(number_children)):
                if c == 0:
                    child1_name = input("What is the name of the first child you want to protect? ")
                    child1_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child1_address = input("What is their address? ")
                elif c == 1:
                    child2_name = input("What is the name of the second child you want to protect? ")
                    child2_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child2_address = input("What is their address? ")
                elif c == 2:
                    child3_name = input("What is the name of the third child you want to protect? ")
                    child3_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child3_address = input("What is their address? ")
                elif c == 3:
                    child4_name = input("What is the name of the fourth child you want to protect? ")
                    child4_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child4_address = input("What is their address? ")
                elif c == 4:
                    child5_name = input("What is the name of the fifth child you want to protect? ")
                    child5_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child5_address = input("What is their address? ")
                elif c == 5:
                    child6_name = input("What is the name of the sixth child you want to protect? ")  
                    child6_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child6_address = input("What is their address? ")
                elif c == 6:
                    child7_name = input("What is the name of the seventh child you want to protect? ")
                    child7_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child7_address = input("What is their address? ")
                elif c == 7:
                    child8_name = input("What is the name of the eighth child you want to protect? ")
                    child8_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child8_address = input("What is their address? ")
                elif c == 8:
                    child9_name = input("What is the name of the ninth child you want to protect? ")
                    child9_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child9_address = input("What is their address? ")
                elif c == 9:
                    child10_name = input("What is the name of the tenth child you want to protect? ")
                    child10_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child10_address = input("What is their address? ")
        if int(number_children) != 0:
            for c in range(int(number_children)-1,11,1):
                if c == 0:
                    child1_name = "none"
                    child1_parent = "none"
                    child1_address = "none"
                elif c == 1:
                    child2_name = "none"
                    child2_parent = "none"
                    child2_address = "none"
                elif c == 2:
                    child3_name = "none"
                    child3_parent = "none"
                    child3_address = "none"
                elif c == 3:
                    child4_name = "none"
                    child4_parent = "none"
                    child4_address = "none"
                elif c == 4:
                    child5_name = "none"
                    child5_parent = "none"
                    child5_address = "none"
                elif c == 5:
                    child6_name = "none"
                    child6_parent = "none"
                    child6_address = "none"
                elif c == 6:
                    child7_name = "none"
                    child7_parent = "none"
                    child7_address = "none"
                elif c == 7:
                    child8_name = "none"
                    child8_parent = "none"
                    child8_address = "none"
                elif c == 8:
                    child9_name = "none"
                    child9_parent = "none"
                    child9_address = "none"
                elif c == 9:
                    child10_name = "none"
                    child10_parent = "none"
                    child10_address = "none"
    if protecting_children.lower() == "yes":
        children_members = input("Are the children members of your family or household?(Yes/No) ")
        children_court_order = input("Is there a court order affecting access to the children?(Yes/No) ")
        children_communicate = input("Do you want the respondent not to communicate in any manner with the children?(Yes/No) ")
        children_200yds = input("Would you like the respondent to stay at least two hundred yards away from the children?(Yes/No) ")
        childrenplaces_200yds = input("Do you want the respondent to stay at least 200 yards away from the children's home, or school except as authorized in a possession schedule authorized by the Court?(Yes/No) ")
    else:
        children_members = "no"
        children_court_order = "no"
        children_communicate = "no"
        children_200yds = "no" 
        childrenplaces_200yds = "no"
        
    you_200yds = input("Would you like the respondent to stay at least two hundred yards away from you?(Yes/No) ")
    yourplaces_200yds = input("Would you like the respondent to stay at least two hundred yards away from the residence, workplace, or school of you?(Yes/No) ")
    
    #start of adult section
    protecting_adults = input("Are there other adults needing protection? ")
    if protecting_adults.lower() == "no":
        number_adults = 0
        adult1_name = "none"
        adult1_address = "none"
        adult2_name = "none"
        adult2_address = "none"
    else:
        number_adults = input("How many adults do you want to protect?(up to two adults)",)
        if int(number_adults) != 0:
            for c in range(int(number_adults)):
                if c == 0:
                    adult1_name = input("What is the name of the first adult you want to protect? ")
                    adult1_address = input("What is their address? ")
                elif c == 1:
                    adult2_name = input("What is the name of the second adult you want to protect? ")
                    adult2_address = input("What is their address? ")
        if int(number_children) != 0:
            for c in range(int(number_children)-1,11,1):
                if c == 0:
                    adult1_name = "none"
                    adult1_address = "none"
                elif c == 1:
                    adult2_name = "none"
                    adult2_address = "none"
    #start of more questions
    other_cases = input("Are there other cases including you, the respondent, the children, or the other adults?(Yes/No) ")
    if other_cases.lower() == "yes":
        case_kind = input("What kind of case is it? ")
        complete_active_case = input("Is it completed or active? ")
        copy_finalorder = input("Do you have a copy of the final order?(Yes/No) ")
        file_finalorder = input("Will a copy of the final order be filed before the hearing?(Yes/No) ")
    else:
        case_kind = "no"
        complete_active_case = "no"
        copy_finalorder = "no"
        file_finalorder = "no"
    family_violence = input("Has the respondent commited family violence or is the respondent likely to commit family violence in the future?(Yes/No) ")
    violate_po = input("Has the respondent violated a protective order that has expired or will expire in thirty days or less?(Yes/No) ")
    if violate_po.lower() == "yes":
        copy_previousorder = input("Do you have a copy of the previous order with you?(Yes/No) ")
        file_previousorder = input("Will a copy of the final order be filed before the hearing?(Yes/No) ")
    else:
        copy_previousorder = "no"
        file_previousorder = "no"
    #ask dad abt automatic yeses
    if family_violence.lower() == "no": 
        commit_family_violence = input("Do you want the respondent to not commit any family violence to any of the people previously named?(Yes/No) ")
    else:
        commit_family_violence = "yes"
    communicate_harass = input("Do you want the respondent to not communicate in a threatening or harrassing manner with any of the people previously named?(Yes/No) ") 
    communicate_threat = input("Do you want the respondent not to communicate a threat through any person to any person named previously?(Yes/No) ")
    communicate_you = input("Do you want the respondent not to communicate in any manner with you?(Yes/No) ") 
    communicate_children = input("Do you want the respondent not to communicate in any manner with the children?(Yes/No) ") 
    communicate_adults = input("Do you want the respondent not to communicate in any manner with the other adults previously named?(Yes/No) ") 
    respondent_talks = input("Is it okay if the respondent talks directly to you? ")
    communicate_through = input("Who can the respondent communicate with you through? ")
    a=1
    
print(answers)


# In[ ]:


answers.update({"applicant": applicant})
answers.update({"phone": phone})
answers.update({"email": email})
answers.update({"applicant_address": applicant_address})
answers.update({"respondent": respondent})
answers.update({"lives_with": lives_with})
answers.update({"respondent_address": respondent_address})
answers.update({"same_family": same_family})
answers.update({"married": married})
answers.update({"dating": dating})
answers.update({"children": children})
answers.update({"protecting_children": protecting_children})
answers.update({"number_children": number_children})
answers.update({"child1_name": child1_name})
answers.update({"child1_parent": child1_parent})
answers.update({"child1_address": child1_address})
answers.update({"child2_name": child2_name})
answers.update({"child2_parent": child2_parent})
answers.update({"child2_address": child2_address})
answers.update({"child3_name": child3_name})
answers.update({"child3_parent": child3_parent})
answers.update({"child3_address": child3_address})
answers.update({"child4_name": child4_name})
answers.update({"child4_parent": child4_parent})
answers.update({"child4_address": child4_address})
answers.update({"child5_name": child5_name})
answers.update({"child5_parent": child5_parent})
answers.update({"child5_address": child5_address})
answers.update({"child6_name": child6_name})
answers.update({"child6_address": child6_address})
answers.update({"child7_name": child7_name})
    answers.update({"child7_parent": child7_parent})
    answers.update({"child7_address": child7_address})
    answers.update({"child8_name": child8_name})
    answers.update({"child8_parent": child8_parent})
    answers.update({"child8_address": child8_address})
    answers.update({"child9_name": child9_name})
    answers.update({"child9_parent": child9_parent})
    answers.update({"child9_address": child9_address})
    answers.update({"child10_name": child10_name})
    answers.update({"child10_parent": child10_parent})
    answers.update({"child10_address": child10_address})
    answers.update({"children_members": children_members})
    answers.update({"children_court_order": children_court_order})
    answers.update({"children_communicate": children_communicate})
    answers.update({"children_200yds": children_200yds})
    answers.update({"childrenplaces_200yds": childrenplaces_200yds})
    answers.update({"you_200yds": you_200yds})
    answers.update({"yourplaces_200yds": yourplaces_200yds})
    answers.update({"number_adults": number_adults})
    answers.update({"adult1_name": adult1_name})
    answers.update({"adult1_address": adult1_address})
    answers.update({"adult2_name": adult2_name})
    answers.update({"adult2_address": adult2_address})
    answers.update({"other_cases": other_cases})
    answers.update({"case_kind": case_kind})
    answers.update({"complete_active_case": complete_active_case})
    answers.update({"copy_finalorder": copy_finalorder})
    answers.update({"file_finalorder": file_finalorder})
    answers.update({"family_violence": family_violence})
    answers.update({"violate_po": violate_po})
    answers.update({"copy_previousorder": copy_previousorder})
    answers.update({"file_previousorder": file_previousorder})
    answers.update({"commit_family_violence": commit_family_violence})
answers.update({"communicate_harass": communicate_harass})
answers.update({"communicate_threat": communicate_threat})
answers.update({"communicate_you": communicate_you})
answers.update({"communicate_children": communicate_children})
answers.update({"communciate_adults": communicate_adults})
answers.update({"respondent_talks": respondent_talks})
answers.update({"communicate_through": communicate_through})
    
print(answers)

if int(number_children) != 0:
            for c in range(int(number_children)+1,11,1):
                if c == 0:
                    child1_name = "none"
                elif c == 1:
                    child2_name = "none"
                elif c == 2:
                    child3_name = "none"
                elif c == 3:
                    child4_name = "none"
                elif c == 4:
                    child5_name = "none"
                elif c == 5:
                    child6_name = "none"                   
                elif c == 6:
                    child7_name = "none"
                elif c == 7:
                    child8_name = "none"
                elif c == 8:
                    child9_name = "none"
                elif c == 9:
                    child10_name = "none"


# In[ ]:


# ## Protective Order Application
PO_FormFields = [('CauseNo', answers.get('CauseNo')),
    ('ApplicantName', answers.get('applicant')),
    ('RespondentName', answers.get('respondent')),
    ('CourtType', answers.get('CourtType')),
    ('CourtCounty', answers.get('CourtCounty')),
    ('ApplicantName2', answers.get('applicant')),
    ('ApplicantCounty', answers.get('applicant_address')),
    ('RespondentName2', answers.get('respondent')),
    ('RespondentCounty', answers.get('respondent_address')),
    ('RespondentAddress', answers.get('respondent_address')),
    ('SameFamilyCB', answers.get('Yes')),
    ('SameChildCB', answers.get('Yes')),
    ('WereMarriedCB', answers.get('Yes')),
    ('DatingCB', answers.get('Yes')),
    ('ProtectChildCB', answers.get('Yes')),
    ('DatingSpouseCB', answers.get('Yes')),
    ('Child1Name', answers.get('Child1Name')),
     ('Child1ParentYesCB', answers.get('Yes')),
     ('Child1ParentNoCB', answers.get('Yes')),
     ('Child1County', answers.get('Child1County')),
     ('Child2ParentNoCB', answers.get('Yes')),
     ('Child2ParentYesCB', answers.get('Yes')),
     ('Child2Name', answers.get('Child2Name')),
     ('Child2County', answers.get('Child2County')),
     ('Child3ParentNoCB', answers.get('Yes')),
     ('Child3ParentYesCB', answers.get('Yes')),
     ('Child3Name', answers.get('Child3Name')),
     ('Child3County' , answers.get('Child3County')),
     ('Child4ParentNoCB', answers.get('Yes')),
     ('Child4ParentYesCB', answers.get('Yes')),
     ('Child4Name', answers.get('Child4Name')),
     ('Child4County', answers.get('Child4County')),
     ('OtherChildrenCB', answers.get('Yes')),
     ('ChildrenMembersCB', answers.get('Yes')),
     ('ChildOrdersCB', answers.get('Yes')),
     ('OtherAdult1Name', answers.get('OtherAdult1Name')),
     ('OtherAdult1County', answers.get('OtherAdult1County')),
     ('OtherAdult2County', answers.get('OtherAdult2County')),
     ('OtherAdult2Name', answers.get('OtherAdult2Name')),
     ('OtherCasesYesCB', answers.get('Yes')),
     ('OtherCasesNoCB', answers.get('Yes')),
     ('CaseStatus', answers.get('CaseStatus')),
     ('OrderAttachedCB', answers.get('Yes')),
     ('OrderFiledCB', answers.get('Yes')),
     ('PriorOrderFiledCB', answers.get('Yes')),
     ('PriorOrderAttachedCB', answers.get('Yes')),
     ('NoThreatCB', answers.get('Yes')),
     ('NoViolenceCB', answers.get('Yes')),
     ('DontCommunicateCB', answers.get('Yes')),
     ('ThreatOthersCB', answers.get('Yes')),
     ('CommunicateApplicantCB', answers.get('Yes')),
     ('CommunicateChildrenCB', answers.get('Yes')),
     ('Communicant', answers.get('Communicant')),
     ('CommunicateOtherAdultsCB', answers.get('Yes')),
     ('Stay200CB', answers.get('Yes')),
     ('Applicant200CB', answers.get('Yes')),
     ('OtherAdults200CB', answers.get('Yes')),
     ('ApplicantWork200CB', answers.get('Yes')),
     ('Work200CB', answers.get('Yes')),
     ('School200CB', answers.get('Yes')),
     ('StalkCB', answers.get('Yes')),
     ('CounselingCB', answers.get('Yes')),
     ('CHLCB', answers.get('Yes')),
     ('AnimalCB', answers.get('Yes')),
     ('Animal', answers.get('Animal')),
     ('ProvisionsCB', answers.get('Yes')),
     ('Provisions', answers.get('Provisions')),
     ('ApplicantResidence', answers.get('ApplicantResidence')),
     ('ApplicantOwnedCB', answers.get('Yes')),
     ('JointlyOwnedCB', answers.get('Yes')),
     ('RespondentOwnedCB', answers.get('Yes')),
     ('LEOEscortCB', answers.get('Yes')),
     ('ExclusiveUseCB', answers.get('Yes')),
     ('JointPropertyDescription', answers.get('JointPropertyDescription')),
     ('NoDamageCB', answers.get('Yes')),
     ('SpousalSupportCB', answers.get('Yes')),
     ('ChildSupportOrdersCB', answers.get('Yes')),
     ('ChildSupportOrders', answers.get('ChildSupportOrders')),
     ('RemoveSchoolCB', answers.get('Yes')),
     ('RemoveJurisdictionCB', answers.get('Yes')),
     ('ModifyScheduleCB', answers.get('Yes')),
     ('PayChildSupportCB', answers.get('Yes')),
     ('VacateNowCB', answers.get('Yes')),
     ('ApplicantResidence2', answers.get('ApplicantResidence2')),
     ('ConfidentialCB', answers.get('Yes')),
     ('PayFeesCB', answers.get('Yes')),
     ('ApplicantLocation', answers.get('ApplicantLocation')),
     ('ApplicantPhone', answers.get('ApplicantPhone')),
     ('ApplicantFax', answers.get('ApplicantFax')),
     ('Children200CB', answers.get('Yes')),
     ('JointPropertyCB', answers.get('Yes')),
     ('ApplicantName3', answers.get('applicant')),
     ('Age', answers.get('Age')),
     ('Whathappened', answers.get('Whathappened')),
     ('Month', answers.get('Month')),
     ('Day', answers.get('Day')),
     ('Year', answers.get('Year')),
     ('UsedWeaponYesCB', answers.get('Yes')),
     ('UsedWeaponNoCB', answers.get('Yes')),
     ('WeaponType', answers.get('WeaponType')),
     ('ChildrenThereNoCB', answers.get('Yes')),
     ('ChildrenThereYesCB', answers.get('Yes')),
     ('ChildrenThere', answers.get('ChildrenThere')),
     ('PoliceNoCB', answers.get('Yes')),
     ('PoliceYesCB', answers.get('Yes')),
     ('PoliceCalled', answers.get('PoliceCalled')),
     ('MedicalCareNoCB', answers.get('Yes')),
     ('MedicalCareYesCB', answers.get('Yes')),
     ('DescribeInjuries', answers.get('DescribeInjuries')),
     ('HurtBefore', answers.get('HurtBefore')),
     ('MedicalCarePastYesCB', answers.get('Yes')),
     ('PolicePastYesCB', answers.get('Yes')),
     ('ChildrenTherePastYesCB', answers.get('Yes')),
     ('UsedWeaponPastYesCB', answers.get('Yes')),
     ('UsedWeaponPastNoCB', answers.get('Yes')),
     ('ChildrenTherePastNoCB', answers.get('Yes')),
     ('PolicePastNoCB', answers.get('Yes')),
     ('MedicalCarePastNoCB', answers.get('Yes')),
     ('ChildrenTherePast', answers.get('ChildrenTherePast')),
     ('WeaponTypePast', answers.get('WeaponTypePast')),
     ('DescribeInjuriesPast', answers.get('DescribeInjuriesPast')),
     ('ConvictedYesCB', answers.get('Yes')),
     ('ConvictedNoCB', answers.get('Yes')),
     ('PastConvictions', answers.get('PastConvictions')),
     ('ApplicantName4', answers.get('applicant')),
     ('ApplicantDOB', answers.get('ApplicantDOB')),
     ('ApplicantStreet', answers.get('ApplicantStreet')),
     ('ApplicantCity', answers.get('ApplicantCity')),
     ('ApplicantState', answers.get('ApplicantState')),
     ('ApplicantZipCode', answers.get('ApplicantZipCode')),
     ('ApplicantCountry', answers.get('ApplicantCountry')),
     ('WhathappenedD', answers.get('WhathappenedD')),
     ('MonthD', answers.get('MonthD')),
     ('DayD', answers.get('DayD')),
     ('YearD', answers.get('YearD')),
     ('PolicePastYesDCB', answers.get('Yes')),
     ('ConvictedNoDCB', answers.get('Yes')),
     ('ConvictedYesDCB', answers.get('Yes')),
     ('ChildrenTherePastNoDCB', answers.get('Yes')),
     ('UsedWeaponPastNoDCB', answers.get('Yes')),
     ('ChildrenTherePastYesDCB', answers.get('Yes')),
     ('UsedWeaponPastYesDCB', answers.get('Yes')),
     ('MedicalCarePastNoDCB', answers.get('Yes')),
     ('MedicalCarePastYesDCB', answers.get('Yes')),
     ('PolicePastNoCBD', answers.get('PolicePastNoCBD')),
     ('UsedWeaponYesDCB', answers.get('Yes')),
     ('ChildrenThereYesDCB', answers.get('Yes')),
     ('MedicalCareNoDCB', answers.get('Yes')),
     ('PoliceNoDCB', answers.get('Yes')),
     ('ChildrenThereNoDCB', answers.get('Yes')),
     ('UsedWeaponNoDCB', answers.get('Yes')),
     ('MedicalCareYesDCB', answers.get('Yes')),
     ('PoliceYesDCB', answers.get('Yes')),
     ('ChildrenThereD', answers.get('ChildrenThereD')),
     ('DescribeInjuriesD', answers.get('DescribeInjuriesD')),
     ('HurtBeforeD', answers.get('HurtBeforeD')),
     ('DescribeInjuriesPastD', answers.get('DescribeInjuriesPastD')),
     ('WeaponTypePastD', answers.get('WeaponTypePastD')),
     ('ChildrenTherePastD', answers.get('ChildrenTherePastD')),
     ('PoliceCalledD', answers.get('PoliceCalledD')),
     ('WeaponTypeD', answers.get('WeaponTypeD')),
     ('PastConvictionsD', answers.get('PastConvictionsD')),
     ('CountyFiling', answers.get('CountyFiling'))
                ]


# In[ ]:


fdf = forge_fdf(fdf_data_strings=PO_FormFields)
fdf_file = open("C:\\Users\\karin\\Documents\\GitHub\\protechme\\po_appdata.fdf","wb")
fdf_file.write(fdf)
fdf_file.close()


# In[ ]:


os.system('pdftk C:\\Users\\karin\\Documents\GitHub\\protechme\\po_application_form.pdf fill_form C:\\Users\\karin\\Documents\GitHub\\protechme\\po_appdata.fdf output C:\\Users\\karin\\Documents\GitHub\\protechme\\po_application_complete.pdf')


# In[ ]:


# ## Ex parte temporary protective order

ExparteFields =[
('CauseNo', answers.get('CauseNo')),
('ApplicantName',answers.get('applicant')),
('RespondentName', answers.get('RespondentName')),
('CourtType', answers.get('CourtType')),
('CourtCounty', answers.get('CourtCounty')),
('CourtDate', answers.get('CourtDate')),
('CourtTime', answers.get('CourtTime')),
('CourtTimeAM', answers.get('CourtTimeAM')),
('CourtTimePM', answers.get('CourtTimePM')),
('CourtAddress', answers.get('CourtAddress')),
('RespondentName1', answers.get('RespondentName1')),
('RespondentCounty', answers.get('RespondentCounty')),
('ApplicantName1', answers.get('ApplicantName1')),
('ApplicantCounty', answers.get('ApplicantCounty')),
('Child1County', answers.get('Child1County')),
('Child1Name', answers.get('Child1Name')),
('Child2County', answers.get('Child2County')),
('Child2Name', answers.get('Child2Name')),
('Child3County', answers.get('Child3County')),
('Child3Name', answers.get('Child3Name')),
('OtherAdultCounty', answers.get('OtherAdultCounty')),
('OtherAdultName', answers.get('OtherAdultName')),
('OtherAdult2County', answers.get('OtherAdult2County')),
('OtherAdult2Name', answers.get('OtherAdult2Name')),
('HarmCB', answers.get('Yes')),
('HarrassCB', answers.get('Yes')),
('CommunicateCB', answers.get('Yes')),
('ApplicantCommunicateCB', answers.get('Yes')),
('ChildrenCommunicateCB', answers.get('Yes')),
('OtherAdultCommunicateCB', answers.get('Yes')),
('Communicant', answers.get('Communicant')),
('Dont200CB', answers.get('Yes')),
('Applicant200CB', answers.get('Yes')),
('Children200CB', answers.get('Yes')),
('OtherAdult200CB', answers.get('Yes')),
('WorkResidence200CB', answers.get('Yes')),
('ApplicantWork200CB', answers.get('Yes')),
('OtherAdultWork200CB', answers.get('Yes')),
('ConfidentialAddressCB', answers.get('Yes')),
('AddressDisclosedCB', answers.get('Yes')),
('ApplicantWorkSchool', answers.get('ApplicantWorkSchool')),
('OtherLocation', answers.get('OtherLocation')),
('SchoolDisclosedCB', answers.get('Yes')),
('ConfidentialSchoolCB', answers.get('Yes')),
('ChildrenResidence', answers.get('ChildrenResidence')),
('ChildrenSchool', answers.get('ChildrenSchool')),
('ChildrenOtherLocation', answers.get('ChildrenOtherLocation')),
('StalkCB', answers.get('Yes')),
('RemoveSchoolCB', answers.get('Yes')),
('RemoveJurisdictionCB', answers.get('Yes')),
('ServiceAnimalCB', answers.get('Yes')),
('ServiceAnimal', answers.get('ServiceAnimal')),
('InterfereResidenceCB', answers.get('Yes')),
('InterferePropertyCB', answers.get('Yes')),
('InterfereProperty', answers.get('InterfereProperty')),
('DamagePropertyCB', answers.get('Yes')),
('ApplicantResidenceLocation', answers.get('ApplicantResidenceLocation')),
('JointlyOwnedCB', answers.get('Yes')),
('ApplicantOwnedCB', answers.get('Yes')),
('RespondentOwnedCB', answers.get('Yes')),
('VacateTime', answers.get('VacateTime')),
('VacateTimeAMCB', answers.get('Yes')),
('VacantTimePMCB', answers.get('Yes')),
('VacateDate', answers.get('VacateDate')),
('OrderTimeAMCB', answers.get('Yes')),
('OrderTimePMCB', answers.get('Yes')),
('DontCommunicateCB', answers.get('Yes')),
('ApplicantResidence', answers.get('ApplicantResidence')),
('School200CB', answers.get('Yes')),
]


# In[ ]:


fdf = forge_fdf(fdf_data_strings=ExparteFields)
fdf_file = open("C:\\Users\\karin\\Documents\GitHub\\protechme\\exparte_data.fdf","wb")
fdf_file.write(fdf)
fdf_file.close()


# In[ ]:



os.system('pdftk C:\\Users\\karin\\Documents\\GitHub\\protechme\\temporary_exparteorder.pdf fill_form C:\\Users\\karin\\Documents\GitHub\\protechme\\exparte_data.fdf output C:\\Users\\karin\\Documents\\GitHub\\protechme\\temporary_exparteorder_complete.pdf')


# In[ ]:


po_form_fields = [
('Case_No' ,  answers.get('Case_No')),
('Applicant_Name' ,  answers.get('Applicant_Name')),
('Court_Type' ,  answers.get('Court_Type')),
('Respondent_Name' ,  answers.get('Respondent_Name')),
('Court_County' ,  answers.get('Court_County')),
('Court_Date' ,  answers.get('Court_Date')),
('Court_Time' ,  answers.get('Court_Time')),
('Court_AMCB' ,  answers.get('Court_AMCB')),
('Court_PMCB' ,  answers.get('Court_PMCB')),
('Intimate_PartnersCB' ,  answers.get('Intimate_PartnersCB')),
('AgreedTermsCB' ,  answers.get('AgreedTermsCB')),
('ViolenceLikelyCB' ,  answers.get('ViolenceLikelyCB')),
('ExpiredOrderCB' ,  answers.get('ExpiredOrderCB')),
('ApplicantInPersonCB' ,  answers.get('ApplicantInPersonCB')),
('RespondentAppearedCB' ,  answers.get('RespondentAppearedCB')),
('ApplicantInPersonAttyCB' ,  answers.get('ApplicantInPersonAttyCB')),
('RespondentAppearedAttyCB' ,  answers.get('RespondentAppearedAttyCB')),
('Attorney' ,  answers.get('Attorney')),
('ApplicantInPersonSigCB' ,  answers.get('ApplicantInPersonSigCB')),
('RespondentAppearedSigCB' ,  answers.get('RespondentAppearedSigCB')),
('ApplicantDNACB' ,  answers.get('ApplicantDNACB')),
('RespondentDNACB' ,  answers.get('RespondentDNACB')),
('ApplicantProtectedCB' ,  answers.get('ApplicantProtectedCB')),
('ApplicantName2' ,  answers.get('ApplicantName2')),
('ApplicantResidenceCounty' ,  answers.get('ApplicantResidenceCounty')),
('ChildrenProtectedCB' ,  answers.get('ChildrenProtectedCB')),
('Child1Name' ,  answers.get('Child1Name')),
('Child1County' ,  answers.get('Child1County')),
('Chlid2Name' ,  answers.get('Chlid2Name')),
('Child2County' ,  answers.get('Child2County')),
('Child3Name' ,  answers.get('Child3Name')),
('Child3County' ,  answers.get('Child3County')),
('Child4Name' ,  answers.get('Child4Name')),
('Child4County' ,  answers.get('Child4County')),
('OtherAdultsProtectedCB' ,  answers.get('OtherAdultsProtectedCB')),
('OtherAdult1Name' ,  answers.get('OtherAdult1Name')),
('OtherAdult1County' ,  answers.get('OtherAdult1County')),
('OtherAdult2Name' ,  answers.get('OtherAdult2Name')),
('OtherAdult2County' ,  answers.get('OtherAdult2County')),
('TestimonyMadeCB' ,  answers.get('TestimonyMadeCB')),
('Recorder' ,  answers.get('Recorder')),
('TestimonyWaivedCB' ,  answers.get('TestimonyWaivedCB')),
('NoHarmCB' ,  answers.get('NoHarmCB')),
('NoThreatCB' ,  answers.get('NoThreatCB')),
('NoThreatbyOthersCB' ,  answers.get('NoThreatbyOthersCB')),
('DontCommunicateCB' ,  answers.get('DontCommunicateCB')),
('NoCommApplicantCB' ,  answers.get('NoCommApplicantCB')),
('NoCommChildCB' ,  answers.get('NoCommChildCB')),
('NoCommOtherCB' ,  answers.get('NoCommOtherCB')),
('Communicant' ,  answers.get('Communicant')),
('Away200ChildCB' ,  answers.get('Away200ChildCB')),
('Away200ApplicantCB' ,  answers.get('Away200ApplicantCB')),
('Away200CB' ,  answers.get('Away200CB')),
('Away200OtherCB' ,  answers.get('Away200OtherCB')),
('Away200ResOtherCB' ,  answers.get('Away200ResOtherCB')),
('Away200ResApplicantCB' ,  answers.get('Away200ResApplicantCB')),
('Away200ResCB' ,  answers.get('Away200ResCB')),
('ApplicantAddConfidentialCB' ,  answers.get('ApplicantAddConfidentialCB')),
('ApplicantAddDisclosedCB' ,  answers.get('ApplicantAddDisclosedCB')),
('Away200ApplicantResidence' ,  answers.get('Away200ApplicantResidence')),
('Away200ApplicantSchool' ,  answers.get('Away200ApplicantSchool')),
('Away200ApplicantOther' ,  answers.get('Away200ApplicantOther')),
('ApplicantChildDisclosedCB' ,  answers.get('ApplicantChildDisclosedCB')),
('ApplicantChildConfidentialCB' ,  answers.get('ApplicantChildConfidentialCB')),
('Away200ChildResCB' ,  answers.get('Away200ChildResCB')),
('Away200ChildResidence' ,  answers.get('Away200ChildResidence')),
('Away200ChildSchool' ,  answers.get('Away200ChildSchool')),
('Away200ChildOther' ,  answers.get('Away200ChildOther')),
('NoStalkCB' ,  answers.get('NoStalkCB')),
('RespondentEnrollCB' ,  answers.get('RespondentEnrollCB')),
('EnterMonth' ,  answers.get('EnterMonth')),
('EnterDay' ,  answers.get('EnterDay')),
('EnterYear' ,  answers.get('EnterYear')),
('CompleteMonth' ,  answers.get('CompleteMonth')),
('CompleteDay' ,  answers.get('CompleteDay')),
('CompleteYear' ,  answers.get('CompleteYear')),
('MeetsGuildelinesCB' ,  answers.get('MeetsGuildelinesCB')),
('ViolenceProgram' ,  answers.get('ViolenceProgram')),
('CounselingCB' ,  answers.get('CounselingCB')),
('CounselingOtherCB' ,  answers.get('CounselingOtherCB')),
('OtherProgram' ,  answers.get('OtherProgram')),
('ViolenceProvisionsCB' ,  answers.get('ViolenceProvisionsCB')),
('ViolenceProvisions' ,  answers.get('ViolenceProvisions')),
('ResidenceAddress' ,  answers.get('ResidenceAddress')),
('PropertyOrdersCB' ,  answers.get('PropertyOrdersCB')),
('JointlyOwnedCB' ,  answers.get('JointlyOwnedCB')),
('ApplicantOwnedCB' ,  answers.get('ApplicantOwnedCB')),
('RespondentOwnedCB' ,  answers.get('RespondentOwnedCB')),
('VacateResidenceCB' ,  answers.get('VacateResidenceCB')),
('VacateTime' ,  answers.get('VacateTime')),
('VacateAMCB' ,  answers.get('VacateAMCB')),
('VacatePMCB' ,  answers.get('VacatePMCB')),
('VacateDate' ,  answers.get('VacateDate')),
('LEOEscortCB' ,  answers.get('LEOEscortCB')),
('JointPropertyCB' ,  answers.get('JointPropertyCB')),
('JointProperty' ,  answers.get('JointProperty')),
('SpousalSupportCB' ,  answers.get('SpousalSupportCB')),
('PaymentAmount' ,  answers.get('PaymentAmount')),
('PaymentDayofMonth' ,  answers.get('PaymentDayofMonth')),
('PaymentMonth' ,  answers.get('PaymentMonth')),
('PaymentDay' ,  answers.get('PaymentDay')),
('PaymentYear' ,  answers.get('PaymentYear')),
('PaymentAddress' ,  answers.get('PaymentAddress')),
('ChildrenRemovalCB' ,  answers.get('ChildrenRemovalCB')),
('RemoveSchoolCB' ,  answers.get('RemoveSchoolCB')),
('RemovalJurisdictionCB' ,  answers.get('RemovalJurisdictionCB')),
('ChildrenPossessionCB' ,  answers.get('ChildrenPossessionCB')),
('ChildNoAccessCB' ,  answers.get('ChildNoAccessCB')),
('ChlidScheduleCB' ,  answers.get('ChlidScheduleCB')),
('PreviousScheduleCB' ,  answers.get('PreviousScheduleCB')),
('OldCaseNo' ,  answers.get('OldCaseNo')),
('OldCaseMonth' ,  answers.get('OldCaseMonth')),
('OldCaseDay' ,  answers.get('OldCaseDay')),
('OldCaseYear' ,  answers.get('OldCaseYear')),
('PriorCase' ,  answers.get('PriorCase')),
('ChildSupportCB' ,  answers.get('ChildSupportCB')),
('ChildSupportAmount' ,  answers.get('ChildSupportAmount')),
('ChildSupportMonth' ,  answers.get('ChildSupportMonth')),
('ChildSupportDueDay' ,  answers.get('ChildSupportDueDay')),
('ChildSupportDay' ,  answers.get('ChildSupportDay')),
('ChildSupportYear' ,  answers.get('ChildSupportYear')),
('PreviousChildSupportCB' ,  answers.get('PreviousChildSupportCB')),
('CSOldCaseMonth' ,  answers.get('CSOldCaseMonth')),
('CSOldCaseDay' ,  answers.get('CSOldCaseDay')),
('CSOldCaseYear' ,  answers.get('CSOldCaseYear')),
('OldChildSupportCaseNo' ,  answers.get('OldChildSupportCaseNo')),
('PriorCaseChildSupport' ,  answers.get('PriorCaseChildSupport')),
('FeesandCostsCB' ,  answers.get('FeesandCostsCB')),
('FeesAmount' ,  answers.get('FeesAmount')),
('ServiceFees' ,  answers.get('ServiceFees')),
('CourtCosts' ,  answers.get('CourtCosts')),
('FeesAndCostsAddress' ,  answers.get('FeesAndCostsAddress')),
('AttorneysFeestCB' ,  answers.get('AttorneysFeestCB')),
('AttorneysFees' ,  answers.get('AttorneysFees')),
('AttorneyName2' ,  answers.get('AttorneyName2')),
('AttorneyAddress' ,  answers.get('AttorneyAddress')),
('AttorneysName3' ,  answers.get('AttorneysName3')),
('RespondentName2' ,  answers.get('RespondentName2')),
('AttorneysFees2' ,  answers.get('AttorneysFees2')),
('AttorneysFeesPct' ,  answers.get('AttorneysFeesPct')),
('ServiceLKACB' ,  answers.get('ServiceLKACB')),
('ServicePersonallyCB' ,  answers.get('ServicePersonallyCB')),
('ServiceInCourtCB' ,  answers.get('ServiceInCourtCB')),
('ServiceCertifiedMailCB' ,  answers.get('ServiceCertifiedMailCB')),
('SheriffCB' ,  answers.get('SheriffCB')),
('SheriffCounty' ,  answers.get('SheriffCounty')),
('PoliceCB' ,  answers.get('PoliceCB')),
('PoliceCity' ,  answers.get('PoliceCity')),
('NotifySchoolCB' ,  answers.get('NotifySchoolCB')),
('Expiration' ,  answers.get('Expiration')),
('OrderAM' ,  answers.get('OrderAM')),
('OrderPM' ,  answers.get('OrderPM')),
]


# In[ ]:


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


# In[ ]:


smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.ehlo()
smtpObj.login('marinathechatbot38@gmail.com', "MarinaIsOurChatbot")


# In[ ]:


Applicant_Name = "Marina Chatbot"

message = MIMEMultipart()
message['Subject'] = "Protective Order Application: " + Applicant_Name
message['From'] = 'marinathechatbot38@gmail.com'
message['Reply-to'] = 'marinathechatbot38@gmail.com'
message['To'] = 'scdavis50@gmail.com'

text = MIMEText("Here is the completed PO application for: " + Applicant_Name)
message.attach(text)

with open("C:\\Users\\karin\\Documents\\GitHub\\protechme\\po_application_complete.pdf", "rb") as opened:
    openedfile = opened.read()
attachedfile = MIMEApplication(openedfile, _subtype = "pdf")
attachedfile.add_header('content-disposition', 'attachment', filename = "poapplication" + Applicant_Name + ".pdf")
message.attach(attachedfile)
smtpObj.sendmail(message['From'], message['To'], message.as_string())


# In[ ]:


Applicant_Name = "Marina Chatbot"

message = MIMEMultipart()
message['Subject'] = "Ex Parte Order: " + Applicant_Name
message['From'] = 'marinathechatbot38@gmail.com'
message['Reply-to'] = 'marinathechatbot38@gmail.com'
message['To'] = 'scdavis50@gmail.com'

text = MIMEText("Here is the completed Temporary Exparte Order for: " + Applicant_Name)
message.attach(text)

with open("C:\\Users\\karin\\Documents\\GitHub\\protechme\\temporary_exparteorder_complete.pdf", "rb") as opened:
    openedfile = opened.read()
attachedfile = MIMEApplication(openedfile, _subtype = "pdf")
attachedfile.add_header('content-disposition', 'attachment', filename = "tempexparte_" + Applicant_Name + ".pdf")
message.attach(attachedfile)
smtpObj.sendmail(message['From'], message['To'], message.as_string())


# In[ ]:


Applicant_Name = "Marina Chatbot"

message = MIMEMultipart()
message['Subject'] = "Ex Parte Order: " + Applicant_Name
message['From'] = 'marinathechatbot38@gmail.com'
message['Reply-to'] = 'marinathechatbot38@gmail.com'
message['To'] = 'scdavis50@gmail.com'

text = MIMEText("Here is the completed Protective Order for: " + Applicant_Name)
message.attach(text)

with open('C:\\Users\\karin\\Documents\\GitHub\\protechme\\protective_order_complete.pdf', "rb") as opened:
    openedfile = opened.read()
attachedfile = MIMEApplication(openedfile, _subtype = "pdf")
attachedfile.add_header('content-disposition', 'attachment', filename = "protectiveorder_" + Applicant_Name + ".pdf")
message.attach(attachedfile)
smtpObj.sendmail(message['From'], message['To'], message.as_string())


# In[ ]:


smtpObj.quit()


# In[ ]:


#start of children's section
    #fix undefined/memory
    protecting_children = input("Are you an adult asking for protection for children?(Yes/No) ")
    if protecting_children.lower() == "no":
        number_children = 0
        child1_name = "none"
        child1_parent = "none"
        child1_address = "none"
        child2_name = "none"
        child2_parent = "none"
        child2_address = "none"
        child3_name = "none"
        child3_parent = "none"
        child3_address = "none"
        child4_name = "none"
        child4_parent = "none"
        child4_address = "none"
        child5_name = "none"
        child5_parent = "none"
        child5_address = "none"
        child6_name = "none"
        child6_parent = "none"
        child6_address = "none"
        child7_name = "none"
        child7_parent = "none"
        child7_address = "none"
        child8_name = "none"
        child8_parent = "none"
        child8_address = "none"
        child9_name = "none"
        child9_parent = "none"
        child9_address = "none"
        child10_name = "none"
        child10_parent = "none"
        child10_address = "none"
    else:
        number_children = input("How many children do you want to protect?(up to ten children) ")
        if int(number_children) != 0:
            for c in range(int(number_children)):
                if c == 0:
                    child1_name = input("What is the name of the first child you want to protect? ")
                    child1_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child1_address = input("What is their address? ")
                elif c == 1:
                    child2_name = input("What is the name of the second child you want to protect? ")
                    child2_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child2_address = input("What is their address? ")
                elif c == 2:
                    child3_name = input("What is the name of the third child you want to protect? ")
                    child3_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child3_address = input("What is their address? ")
                elif c == 3:
                    child4_name = input("What is the name of the fourth child you want to protect? ")
                    child4_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child4_address = input("What is their address? ")
                elif c == 4:
                    child5_name = input("What is the name of the fifth child you want to protect? ")
                    child5_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child5_address = input("What is their address? ")
                elif c == 5:
                    child6_name = input("What is the name of the sixth child you want to protect? ")  
                    child6_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child6_address = input("What is their address? ")
                elif c == 6:
                    child7_name = input("What is the name of the seventh child you want to protect? ")
                    child7_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child7_address = input("What is their address? ")
                elif c == 7:
                    child8_name = input("What is the name of the eighth child you want to protect? ")
                    child8_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child8_address = input("What is their address? ")
                elif c == 8:
                    child9_name = input("What is the name of the ninth child you want to protect? ")
                    child9_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child9_address = input("What is their address? ")
                elif c == 9:
                    child10_name = input("What is the name of the tenth child you want to protect? ")
                    child10_parent = input("Is the respondent their biological parent(Yes/No)? ")
                    child10_address = input("What is their address? ")
        if int(number_children) != 0:
            for c in range(int(number_children)-1,11,1):
                if c == 0:
                    child1_name = "none"
                    child1_parent = "none"
                    child1_address = "none"
                elif c == 1:
                    child2_name = "none"
                    child2_parent = "none"
                    child2_address = "none"
                elif c == 2:
                    child3_name = "none"
                    child3_parent = "none"
                    child3_address = "none"
                elif c == 3:
                    child4_name = "none"
                    child4_parent = "none"
                    child4_address = "none"
                elif c == 4:
                    child5_name = "none"
                    child5_parent = "none"
                    child5_address = "none"
                elif c == 5:
                    child6_name = "none"
                    child6_parent = "none"
                    child6_address = "none"
                elif c == 6:
                    child7_name = "none"
                    child7_parent = "none"
                    child7_address = "none"
                elif c == 7:
                    child8_name = "none"
                    child8_parent = "none"
                    child8_address = "none"
                elif c == 8:
                    child9_name = "none"
                    child9_parent = "none"
                    child9_address = "none"
                elif c == 9:
                    child10_name = "none"
                    child10_parent = "none"
                    child10_address = "none"
    if protecting_children.lower() == "yes":
        children_members = input("Are the children members of your family or household?(Yes/No) ")
        children_court_order = input("Is there a court order affecting access to the children?(Yes/No) ")
        children_communicate = input("Do you want the respondent not to communicate in any manner with the children?(Yes/No) ")
        children_200yds = input("Would you like the respondent to stay at least two hundred yards away from the children?(Yes/No) ")
        childrenplaces_200yds = input("Do you want the respondent to stay at least 200 yards away from the children's home, or school except as authorized in a possession schedule authorized by the Court?(Yes/No) ")
    else:
        children_members = "no"
        children_court_order = "no"
        children_communicate = "no"
        children_200yds = "no" 
        childrenplaces_200yds = "no"

