#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML


# In[2]:


import matplotlib
import matplotlib.colors as mc
import colorsys
from random import randint
import re


# In[3]:


import glob 
import numpy as np


# In[4]:


#Oridinally tried combining my data but the formats were different, had to clean the two sets differently
#Here's set 1


# In[5]:


fmt1 = pd.DataFrame()


# In[6]:


for reports1 in glob.glob("C:\\Users\\nchin\\DataViz\\covid_timeseries\\fmt1\\*.csv"):
    df = pd.read_csv(reports1)
    fmt1 = fmt1.append(df,ignore_index = True)


# In[7]:


fmt1.head()


# In[8]:


fmt1['Location'] = fmt1[['Province/State', 'Country/Region']].apply(lambda x: ', '.join(x[x.notnull()]), axis = 1)


# In[9]:


fmt1['Datetime'] = pd.to_datetime(fmt1['Last Update'])


# In[10]:


fmt1 = fmt1.rename(columns = {"Province/State":'Province_State', 'Country/Region':'Country_Region'})


# In[11]:


#fmt1 = fmt1[['Location', 'Date','Confirmed', 'Deaths', 'Recovered']]
fmt1 = fmt1[['Province_State','Country_Region', 'Datetime','Confirmed', 'Deaths', 'Recovered']]


# In[12]:


fmt1['Province_State'] = fmt1['Province_State'].fillna(fmt1['Country_Region'])


# In[13]:


fmt1.head()


# In[14]:


fmt1['Date'] = fmt1['Datetime'].dt.normalize()


# In[15]:


fmt1_clean = fmt1[['Province_State','Country_Region', 'Date','Confirmed', 'Deaths', 'Recovered']]


# In[16]:


fmt1_clean.head()


# In[17]:


#Set 2


# In[18]:


fmt2 = pd.DataFrame()


# In[19]:


for reports2 in glob.glob("C:\\Users\\nchin\\DataViz\\covid_timeseries\\fmt2\\*.csv"):
    df = pd.read_csv(reports2)
    fmt2 = fmt2.append(df,ignore_index = True)


# In[20]:


fmt2.tail()


# In[21]:


fmt2['Location'] = fmt2[['Province_State', 'Country_Region']].apply(lambda x: ', '.join(x[x.notnull()]), axis = 1)


# In[22]:


fmt2.loc[(fmt2['Country_Region'] == 'Zimbabwe')]


# In[23]:


fmt2['Datetime'] = pd.to_datetime(fmt2['Last_Update'])
fmt2['Date'] = fmt2['Datetime'].dt.normalize()


# In[24]:


#fmt2.loc[(fmt2['Location'] == 'Vietnam')]


# In[ ]:





# In[25]:


fmt2 = fmt2[['Province_State','Country_Region', 'Date','Confirmed', 'Deaths', 'Recovered']]


# In[26]:


fmt2['Province_State'] = fmt2['Province_State'].fillna(fmt2['Country_Region'])


# In[27]:


fmt2.head()


# In[28]:


fmt2_clean = fmt2


# In[29]:


#fmt2_clean.tail()


# In[30]:


covid = pd.concat([fmt1_clean, fmt2_clean], axis = 0, sort = False)


# In[31]:


covid = covid.fillna(0)


# In[32]:


covid['Date'] = covid['Date'].dt.strftime('%Y-%m-%d')


# In[33]:


covid.info()


# In[34]:


def week_num(date):
    if date == '2020-01-22':
        return 1
    elif date == '2020-01-29':
        return 2
    elif date == '2020-02-05':
        return 3
    elif date == '2020-02-12':
        return 4
    elif date == '2020-02-19':
        return 5
    elif date == '2020-02-26':
        return 6
    elif date == '2020-03-04':
        return 7
    elif date == '2020-03-11':
        return 8
    elif date == '2020-03-18':
        return 9
    elif date == '2020-03-25':
        return 10
    elif date == '2020-04-01':
        return 11


# In[35]:


covid['Week'] = covid['Date'].apply(week_num)


# In[36]:


covid.tail()


# In[37]:


fmt1_clean.count()


# In[38]:


fmt2_clean.count()


# In[ ]:





# In[39]:


covid.count() 
#wanted to make sure they add up


# In[40]:


covid['Country_Region'].nunique()


# In[ ]:





# In[ ]:





# In[41]:


earliest_date = '2020-01-29'
dff = (covid[covid['Date'].eq(earliest_date)]
       .sort_values(by='Confirmed', ascending=False)
       .head(10))
dff


# In[42]:


df=covid


# In[43]:


current_year = '2020-04-01'
dff = (df[df['Date'].eq(current_year)]
       .sort_values(by='Confirmed', ascending=False)
       .head(10))
dff


# In[50]:


colors = dict(zip(
    ['Italy', 'China', 'South Korea', 'Korea, South', 'Iran',
     'Spain', 'France', 'Germany', 'Switzerland', 'United Kingdom',
    'US', 'Turkey', 'Others'],
    ['#adb0ff', '#ffb3ff', '#90d595' , '#90d595', '#e48381',
     '#aafbff', '#f7bb5f', '#eafb50', 'darksalmon', 'royalblue',
    'r', 'gold', "orange"]
))


# In[45]:


group_lk = covid.set_index('Province_State')['Country_Region'].to_dict()


# In[46]:


#covid.loc[(covid['Week'] == 6)]


# In[51]:


fig, ax = plt.subplots(figsize=(15, 8))
#dff = dff[::-1]   # flip values from top to bottom
# pass colors values to `color=`
ax.barh(dff['Province_State'], dff['Confirmed'], color=[colors[group_lk[x]] for x in dff['Province_State']])
# iterate over the values to plot labels and values (Tokyo, Asia, 38194.2)
for i, (Confirmed, Province_State) in enumerate(zip(dff['Confirmed'], dff['Province_State'])):
    ax.text(Confirmed, i,     Province_State,            ha='right')  # Tokyo: name
    ax.text(Confirmed, i-.25, group_lk[Province_State],  ha='right')  # Asia: group name
    ax.text(Confirmed, i,     Confirmed,           ha='left')   # 38194.2: value
# Add year right middle portion of canvas
ax.text(1, 0.4, current_year, transform=ax.transAxes, size=40, ha='right')


# In[52]:


fig, ax = plt.subplots(figsize=(15, 8))
def draw_barchart(week):
    dff = df[df['Week'].eq(week)].sort_values(by='Confirmed', ascending=True).tail(10)
    ax.clear()
    ax.barh(dff['Province_State'], dff['Confirmed'], color=[colors[group_lk[x]] for x in dff['Province_State']])
    dx = dff['Confirmed'].max() / 200
    for i, (value, name) in enumerate(zip(dff['Confirmed'], dff['Province_State'])):
        ax.text(value-dx, i,     name,           size=15, weight=600, ha='right', va='bottom')
        ax.text(value-dx, i-.25, group_lk[name], size=12, color='#444444', ha='right', va='baseline')
        ax.text(value+dx, i,     f'{value:,.0f}',  size=15, ha='left',  va='center')
    
    ax.text(1, 0.4, week, transform=ax.transAxes, color='#444444', size=46, ha='right', weight=800)
    ax.text(0.9, 0.4, 'Week', transform=ax.transAxes, color='#444444', size=46, ha='right', weight=800)
    
    def date(week):
        if week == 1:
            return '2020-01-22'
        elif week == 2:
            return '2020-01-29'
        elif week == 3:
            return '2020-02-05'
        elif week == 4:
            return '2020-02-12'
        elif week == 5:
            return '2020-02-19'
        elif week == 6:
            return '2020-02-26'
        elif week == 7:
            return '2020-03-04'
        elif week == 8:
            return '2020-03-11'
        elif week == 9:
            return '2020-03-18'
        elif week == 10:
            return '2020-03-25'
        elif week == 11:
            return'2020-04-01'
                
    
    ax.text(0.99, 0.3, date(week), transform=ax.transAxes, color='#444444', size=46, ha='right', weight=800)
    
    ax.text(0, 1.06, 'Confirmed Cases', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.12, 'Locations with Most Confirmed Cases',
            transform=ax.transAxes, size=24, weight=600, ha='left')
    ax.text(1, 0, 'by Nick Chin', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)
    
draw_barchart(6)


# In[53]:


import matplotlib.animation as animation
from IPython.display import HTML
fig, ax = plt.subplots(figsize=(15, 8))

animator = animation.FuncAnimation(fig, draw_barchart, frames= range(1,12))
HTML(animator.to_jshtml()) 


# In[ ]:




