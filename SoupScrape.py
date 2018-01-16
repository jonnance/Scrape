# -*- coding: utf-8 -*-


import urllib2
from bs4 import BeautifulSoup
import pandas as pd
from dateutil.parser import parse
import re

o = urllib2.build_opener(myproxy)
urllib2.install_opener(o)

url = 'http://www.multpl.com/table?f=m'
html = urllib2.urlopen(url).read()

soup = BeautifulSoup( html )
soup.findAll('tr',limit = 5)
column_headers = [th.getText() for th in soup.findAll('tr',limit = 2)[0].findAll('th')]
[th.getText() for th in soup.findAll('tr',limit = 5)[0].findAll('th')]

table = soup

n_columns =0
n_rows=0
column_names = []
for row in table.find_all('tr'):
    
    # Determine the number of rows in the table
    td_tags = row.find_all('td')
    if len(td_tags) > 0:
        n_rows+=1
        if n_columns == 0:
            # Set the number of columns for our table
            n_columns = len(td_tags)
            
    # Handle column names if we find them
    th_tags = row.findAll('th') 
    if len(th_tags) > 0 and len(column_names) == 0:
        for th in th_tags:
            column_names.append(th.get_text())
            print th.find(text=True)
            print th




new_table = pd.DataFrame(columns=range(0,n_columns),  index = range(0,n_rows+1))
row_marker = 0
for row in table.findAll("tr"):
    cells = row.findAll("td")
    #print cells
    #print len(cells)
    #For each "tr", assign each "td" to a variable.
    if len(cells) == 2:
        #area = cells[0].find(text=True)
        #district = cells[1].find(text=True)
        new_table.iat[row_marker,0] = cells[0].find(text=True)
        new_table.iat[row_marker,1] = cells[1].find(text=True)
    #print row_marker
    row_marker +=1

new_table.columns = ['Date','PE']    
df = new_table
df.dropna(inplace = True)

df['PE']=df['PE'].astype(float)
df['Date']= [parse(x) for x in df['Date']]
df.set_index('Date',inplace = True)
df.plot()

        
