# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 16:00:08 2019

@author: Scott
"""
from helper import *
import pickle
from nltk.util import ngrams
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

tools = ['python','r','java','c++','sql','excel','scala','stata','sas','spark','hadoop',
         'cloudera','mongodb','tableau','hive','tensorflow','django','aws','mahout','matlab','cassandra','mapreduce',
         'nosql','nlp','rdbms','qlikview','spotfire','bi','html',
         'ruby','unix','pig']
         #List of single-word skills to look for
         
tools2=['machine learning','big data','natural language','statistical analysis','web scraping','machine vision','computer vision','data mining']
#List of 2-word skills to look for

jobDict=load_obj('glassDoorDict2')
counts1=np.zeros([3,len(tools)])
counts2=np.zeros([3,len(tools2)])
Jobs=['data scien','data engineer','data analyst']  #Job titles to search for
Jobs_Full=['Data Scientist','Data Engineer','Data Analyst'] #Job titles for display purposes
tot=np.zeros(len(Jobs))
for val in list(jobDict.values())[:]: #Search for skills in listings of the different job titles
    if val[1].find('data scien')>=0 and len(val)>=9:
        tot[0]+=1
        wordlist=[wrd.decode('unicode_escape') for wrd in val[8]]
        (counts1[0,:],counts2[0,:])=CountWords(wordlist,tools,tools2,counts1[0,:],counts2[0,:])
    if val[1].find(Jobs[1])>=0 and len(val)>=9:
        tot[1]+=1
        wordlist=[wrd.decode('unicode_escape') for wrd in val[8]]
        (counts1[1,:],counts2[1,:])=CountWords(wordlist,tools,tools2,counts1[1,:],counts2[1,:])
    if val[1].find(Jobs[2])>=0 and len(val)>=9:
        tot[2]+=1
        wordlist=[wrd.decode('unicode_escape') for wrd in val[8]]
        (counts1[2,:],counts2[2,:])=CountWords(wordlist,tools,tools2,counts1[2,:],counts2[2,:])
        
print(tot)
c=[[],[],[]]
for i in range(3): #Normalize count to percent
    c[i]=np.array(list(counts1[i,:])+list(counts2[i,:]))/tot[i]*100
L=tools+tools2

#for i in range(3):
#    skill_dict[i] = {}
#    for ind,tool in enumerate(L):
#        #print(tool,' : ',tool_freq(tool))
#        skill_dict[i][tool] = c[i][ind]
DFL=[]
for i in range(3):
    for ind, tool in enumerate(L):
        DFL.append([tool,Jobs_Full[i],c[i][ind]])
jobs_DF=pd.DataFrame(DFL)
jobs_DF.columns=['Tool','Title','Frequency']
#Assemble Dataframe

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
jobs_DF.pivot(index='Tool', columns='Title', values='Frequency').sort_values(by ='Data Scientist', ascending = False).plot(kind='bar')
plt.ylabel('Percent of listings mentioning this tool')
plt.subplot()
jobs_DF.pivot(index='Tool', columns='Title', values='Frequency')['Data Scientist'].sort_values( ascending = False).head(10).plot(kind='bar')
plt.ylabel('Percent of listings mentioning this tool')
plt.title('Data Scientist')
jobs_DF.pivot(index='Tool', columns='Title', values='Frequency')['Data Engineer'].sort_values( ascending = False).head(10).plot(kind='bar')
plt.ylabel('Percent of listings mentioning this tool')
plt.title('Data Engineer')
jobs_DF.pivot(index='Tool', columns='Title', values='Frequency')['Data Analyst'].sort_values( ascending = False).head(10).plot(kind='bar')
plt.ylabel('Percent of listings mentioning this tool')
plt.title('Data Analyst')
#Plotting

DF=jobs_DF.pivot(index='Tool', columns='Title', values='Frequency').sort_values(by ='Data Scientist', ascending = False)
DF

    
#skill_dict
#for i in range(3):
#    df_job = pd.DataFrame(skill_dict[0])
#    df_job.columns = ['Data Scientist','Data Engineer','Data Analyst']
#df_job.head()


#for i in range(3):
#    ax=plt.subplot(1,3,i+1)
#    dummy = df_job.sort_values(by ='frequency', ascending = False).plot(kind ='bar', color ='teal',ax=ax)
#    plt.ylabel('Number of jobs')

#fig, ax = plt.subplots()
#ax.bar(np.arange(1,len(c)+1),c)
#plt.xticks(np.arange(1,len(c)+1),L,rotation='vertical')
#plt.show()

    #print(val[1].find('data scien'))
    
def GenerateNgrams(wordlist,n): #Needed to search for multi-word skills
    ngrams = zip(*[wordlist[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def CountWords(wordlist,tools,tools2,counts1,counts2):  #Function that does the actual searching
    NG1=GenerateNgrams(wordlist,1)
    for ind,tool in enumerate(tools):
        for wrd in NG1:
            if wrd==tool:
                counts1[ind]+=1
                break
    NG2=GenerateNgrams(wordlist,2)
    for ind,tool in enumerate(tools2):
        for wrd in NG2:
            if wrd==tool:
                counts2[ind]+=1
                break
    return (counts1,counts2)