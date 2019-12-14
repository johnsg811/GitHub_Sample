#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import lxml.html as lh
import pandas as pd


# In[2]:


url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'


# In[3]:


page = requests.get(url)


# In[4]:


doc = lh.fromstring(page.content)


# In[5]:


tr_elements = doc.xpath('//tr')


# In[6]:


[len(T) for T in tr_elements[:12]]


# In[7]:


tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0


# In[15]:


for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))


# In[16]:


for j in range(1,len(tr_elements)):
    T=tr_elements[j]
    
    if len(T)!=3:
        break
    i=0
    
    for t in T.iterchildren():
        data=t.text_content() 
        if i>0:
            try:
                data=int(data)
            except:
                pass
        col[i][1].append(data)
        i+=1


# In[17]:


[len(C) for (title,C) in col]


# In[18]:


Dict={title:column for (title,column) in col}
dfCanada=pd.DataFrame(Dict)


# In[19]:


dfCanada


# In[20]:


#discard "Not Assigned" columns
dfCanada = pd.read_html(url, header=0, na_values = ['Not assigned'])[0]
dfCanada.dropna(subset=['Borough'], inplace=True)
dfCanada


# In[ ]:





# In[14]:


#removing '\n'
#dfCanada = dfCanada.replace('\n',' ', regex=True)


# In[21]:


dfCanada


# In[24]:


#Rearranging and renaming
dfCanada.columns = ['Borough', 'Neighbourhood','Postcode']
cols = dfCanada.columns.tolist()
cols

cols = cols[-1:] + cols[:-1]

dfCanada = dfCanada[cols]
dfCanada


# In[25]:


#Check Neighborhood isEmpty but Borough exists
empty_row = dfCanada[dfCanada['Neighbourhood'].isna()].shape[0]
print('Empty Neighborhood rows: {}'.format(empty_row))


# In[26]:


#Show which neighborhood is emtpy but Borough exists
dfCanada[dfCanada['Neighbourhood'].isna()]


# In[27]:


#Replace empty Neighborhood with Borough name and check again
dfCanada['Neighbourhood'].fillna(dfCanada['Borough'], inplace=True)
empty_row = dfCanada[dfCanada['Neighbourhood'].isna()].shape[0]
print('Empty Neighborhood rows: {}'.format(empty_row))


# In[28]:


dfCanada.shape
dfCanada.to_csv(r'df_final.csv')


# In[373]:


#