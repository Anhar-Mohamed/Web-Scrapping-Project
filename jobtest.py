import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
from selenium import webdriver
browser = webdriver.Chrome()


url = "https://wuzzuf.net/search/jobs/?q=python&a=hpb"
page = requests.get(url).text
soup = BeautifulSoup(page, "html.parser")
#print(soup.prettify())
job_title = []
company_name = []
location_name = []
job_skill = []
job_links = []
salary = []
links = []
Job_Requirements = []


job_titles = soup.find_all("h2", class_="css-m604qf")
company_names = soup.find_all("a", class_="css-17s97q8")
location_names = soup.find_all("span", class_="css-5wys0k")
job_skills = soup.find_all("div", class_="css-y4udm8")

base_url = soup.find("div",class_="css-1gatmva e1v1l3u10").div.a['href'][:18]
#print(base_url)


#for skill in job_skills:
#    print(skill.text)
for i in range(len(job_titles)):
    job_title.append(job_titles[i].text)
    job_links.append(job_titles[i].find('a').attrs['href'])
    company_name.append(company_names[i].text)
    location_name.append(location_names[i].text)
    job_skill.append(job_skills[i].text)
#print(job_links)
for link in job_links:
    links.append(base_url+link)
#print(links)


#print(job_title , company_name , location_name , job_skill )

#Using Selenium Libareries
for link in links:
    browser.get(link)
    html = browser.page_source
    soup2 = BeautifulSoup(html,"html.parser")
    salaries = soup2.find_all("span",class_="css-4xky9y")[3]
    salary.append(salaries.text)
    Requirements = soup2.find("div",class_="css-1t5f0fr").find("ul")
    Requirements_text = ""
    for li in Requirements.find_all("li"):
        Requirements_text += li.text+"...."
    Job_Requirements.append(Requirements_text)
#print(Job_Requirements)
print(Requirements)


file_list = [job_title,company_name,location_name,job_skill,links,salary,Job_Requirements]
exported = zip_longest(*file_list)

#Creat CSV file
with open("D:\Data Analysis Professional Track\Web Scraping Python\jobtest.csv", "w") as file:
    wr = csv.writer(file)
    wr.writerow(["job title","comapany name","job location","job skill","links","salary","Job Requirements"])
    wr.writerows(exported)
