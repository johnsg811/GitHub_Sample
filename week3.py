import requests
import lxml.html as lh
import pandas as pd

url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'


page = requests.get(url)

doc = lh.fromstring(page.content)


tr_elements = doc.xpath('//tr')



[len(T) for T in tr_elements[:12]]


tr_elements = doc.xpath('//tr')
#Create empty list
col=[]
i=0


for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))

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


[len(C) for (title,C) in col]




dfCanada.columns = ['Borough', 'Neighbourhood','Postcode']
cols = dfCanada.columns.tolist()
cols

cols = cols[-1:] + cols[:-1]

dfCanada = dfCanada[cols]
dfCanada


dfCanada = dfCanada.replace('\n',' ', regex=True)



dfCanada.drop(dfCanada.index[dfCanada['Borough'] == 'Not assigned'], inplace = True)

# Reset the index and dropping the previous index
dfCanada = dfCanada.reset_index(drop=True)

dfCanada.head(10)


dfCanada = dfCanada.astype(str)

dfCanada = dfCanada.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(','.join).reset_index()
dfCanada.columns = ['Postcode','Borough','Neighbourhood']


dfCanada.loc[dfCanada['Neighbourhood'] == 'Not assigned', 'Neighbourhood'] = dfCanada['Borough']
dfCanada[dfCanada['Borough'] == 'Queen\'s Park']

dfCanada.shape
dfCanada.to_csv(r'df_can.csv')