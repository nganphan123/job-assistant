import requests
from bs4 import BeautifulSoup

import pandas as pd
import time

# URL = 'https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10'
# page = requests.get(URL)
#
# soup = BeautifulSoup(page.content, 'html.parser')

#Find summaries contain words
def find(soup,word1,word2,word3):
    results = []
    td = soup.find(id='resultsCol')
    lis = td.find_all('li', string=lambda x: x and (word1 in x.lower() or word2 in x.lower() or word3 in x.lower()))
    for li in lis:
        results.append(li.parent.parent.parent)
    return results
# Get title
def jobTitle(div):
    return (div.find('h2',class_='title').a['title'])

#Get company
def company(div):
    span = div.find('span',class_='company')
    if span.a is None:
        return span.text.strip()
    else:
        return span.a.text.strip()

#Get location
def location(div):
    if div.find('div',class_='location accessible-contrast-color-location') is None:
        return div.find('span',class_='location accessible-contrast-color-location').text
    else:
        return div.find('div',class_='location accessible-contrast-color-location').text


#Get salary
def salary(div):
    span = div.find('span',class_='salaryText')
    if span is None:
        return 'No Value'
    else:
        return span.text

#Get summary
def summary(div):
    return str(div.find('div',class_='summary').text).strip('\n')

#Get URL
def URL(div):
    return (div['data-jk'])

def findJob(type,city,skills):
    # max_results_per_city = 20

    # columns = ['city', 'job_title', 'company_name', 'location', 'summary', 'salary']

    # sample_df = pd.DataFrame(columns=columns)
    list=[]

    # for start in range(0, max_results_per_city, 10):
    page = requests.get('https://ca.indeed.com/jobs' + '?q=' + str(type) + '&l=' + str(city) + '&start=' + str(10))
    time.sleep(1)
    soup = BeautifulSoup(page.content, 'html.parser')
    for div in find(soup,skills[0],skills[1],skills[2]):
        # num = (len(sample_df) + 1)
        job_post = []
        job_post.append(jobTitle(div)),
        job_post.append(company(div)),
        job_post.append(location(div)),
        job_post.append(salary(div)),
        job_post.append(summary(div)),
        job_post.append('https://ca.indeed.com/viewjob?jk='+ URL(div))
        # sample_df.loc[num] = job_post
        list.append(job_post)
    print(list)
    return list

# findJob('developer','kelowna',[' ',' ',' '])

