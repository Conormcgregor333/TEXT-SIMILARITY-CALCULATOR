#!/usr/bin/env python
# coding: utf-8

# # PART-A OF THE TASK-
# ## BY SIDDHARTH PAREEK

# ### Build an algorithm/model that can quantify the degree of similarity between the two text-based on Semantic similarity. Semantic Textual Similarity (STS) assesses the degree to which two sentences are semantically equivalent to each other.
# ### 1 means highly similar
# ### 0 means highly dissimilar

# ## Lets import the pandas library first.
# 

# In[1]:


import pandas as pd


# In[2]:


df=pd.read_csv('precily_data.csv')


# ## Lets see how the data frame looks-

# In[3]:


df


# ## To know the informations like column names, data types, number of null values etc we use info() method.

# In[4]:


df.info()


# ## To get the rows and column number-

# In[5]:


df.shape


# ## To get the count of unique elements and total elements we use describe() method-

# In[6]:


df.describe()


# # NOW LETS CHECK FOR THE SIMILARITY BETWEEN THE SENTENCE PAIRS-

# In[7]:


import math
import re
from collections import Counter


# ### LETS DISCUSS ABOUT ALL THE LIBRARIES WE HAVE IMPORTED NOW-
# #### 1) math-  The math library gives us the access to various math functions and constants whcih we can use in complex math calculations.
# #### 2) re- This is very important library we will be using in our code. This is the Regular Expression that specifies a set of strings that matches it .           The functions in this module let you check if a particular string matches a given regular expression.
# #### 3) Importing Counter from collections- Helps in counting the frequency of each word in the sentence.

# In[8]:


word=re.compile(r"\w+")


# #### By using re.compile(r"\w+") we will separate all the words from the sentence. 

# #### Lets see an example of how to find all the words from the sentence using findall() method and then count their occurrences using Counter() method.

# In[9]:


words=word.findall(df['text1'][1])


# In[10]:


#len(words)
Counter(words)


# ## Now let's see the approach to find the similarity between the sentence pairs and represent their similarity using 0's and 1's.

# ## First we need to convert every sentence from the dataset to a vector. 
# ## What is vector and how to convert a sentence to a vector????
# ## We will do this by first finding all the words from each sentence present in he data set by using the re.compile() and findall() methods and then we will use the Counter() method to convert the words set to a vector which is nothing but the frequency of occurrence of all words in the sentence.

# ## Lets create a function which will do the job of converting the sentence into a vector .

# In[11]:



def sent_to_vector(sent):
    words_finded=word.findall(sent)
    vector=Counter(words_finded)
    return vector
    


# ## After we have the corresponding vectors of all the sentences then we will use the cosine similarity method to find out the similarity.
# ## What is Cosine similarity???
# ## Cosine similarity is used to find out the similarity between 2 vectors. We know that Dot product of 2 vectors is equal to products of the modulo of the both vectors and cosine of angle between them. If we bring the cosine in the left hand side and send all the other things on R.H.S then we will have cos(angle)=(vect1.vect2)/(|vect1|*|vect2|). Now if cos(angle) is 1 that means the angle between the 2 vectors is zero that is they are aligned on each other. And in terms of sentence's it means that the pair of sentence's are similar. If cos(angle) is zero that is angle is 90 degrees which means that the 2 vectors are not aligned on each other which results in un-similar sentence. This will be our approach in solving the given problem statement.
# ## Lets implement it now :)

# ## Now we will be creating a function that calculates the cosine similarity of the vectors-

# In[12]:


def vect_to_cos(v1,v2):
    intersection=set(v1.keys()) & set(v2.keys())
    #intersection will give us the common words with their frequency.
    numerator=sum(v1[i]*v2[i] for i in intersection)
    sum1 = sum([v1[x] ** 2 for x in list(v1.keys())])
    sum2 = sum([v2[x] ** 2 for x in list(v2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
        #since we dont want a divide by zero.
    else:
        return float(numerator)/denominator
    


# ### Example for intersection-

# In[14]:


intersection=(Counter(word.findall(df['text1'][0]))) & (Counter(word.findall(df['text2'][0])))


# ## 2 data frames will be created to store all the vectors corresponding to the sentences in the df. 

# In[16]:


df['vect1']=df['text1'].apply(lambda x:sent_to_vector(x))
df['vect2']=df['text2'].apply(lambda x:sent_to_vector(x))


# ## Now we will create a data frame which will contain all the similarity score.

# In[17]:


df['similarity_score']=df.apply(lambda x:vect_to_cos(x['vect1'],x['vect2']),axis=1)


# In[18]:


df['similarity_score']


# ## We can see that the similarity score is in the range of 0 to 1. Therefore we must round it off using round() method to get similarity score in 0 and 1.

# In[19]:


df['similarity_score']=df.apply(lambda x:round(vect_to_cos(x['vect1'],x['vect2'])),axis=1)


# In[20]:


df['similarity_score']


# ## Now we have the similarity score in 0's and 1's.

# ## Now lets make a excel sheet out of the similarity score dataframe.

# In[25]:


d=[]
x=0
for i in range(3000):
    d.insert(x,'similarity score')
    x=x+1


# In[27]:


df_new=pd.DataFrame(d)


# In[32]:


result_df=pd.concat([df_new,df['similarity_score']],axis=1,join='inner')


# ## To make data frame as a excel sheet we must install openpyxl library. :)  

# In[35]:


get_ipython().system('pip install openpyxl')


# In[36]:


result_df.to_excel('similarity_score.xlsx')


# # This was my Schematic similarity data analysis of the data frame given.
# # Thank you :)
