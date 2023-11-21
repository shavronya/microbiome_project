import requests
from bs4 import BeautifulSoup
import time
import re
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
def get_paperinfo(paper_url):
    response=requests.get(url,headers=headers)
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page')
    paper_doc = BeautifulSoup(response.text,"html.parser")
    return paper_doc
def get_tags(doc):
    paper_tag = doc.select('[data-lid]')
    link_tag = doc.find_all('h3',{"class" : "gs_rt"})
    author_tag = doc.find_all("div", {"class": "gs_a"})
    return paper_tag, link_tag, author_tag
def get_papertitle(paper_tag):
    paper_names = []
    for tag in paper_tag:
        paper_names.append(tag.select('h3')[0].get_text())
    return paper_names
def get_link(link_tag):
    links = []
    for i in range(len(link_tag)):
        links.append(link_tag[i].a['href']) 
    return links 
def get_author_year_publi_info(authors_tag):
    years = []
    publication = []
    authors = []
    journals = []
    for i in range(len(authors_tag)):
        authortag_text = (authors_tag[i].text).split()
        year = int(re.search(r'\d+', authors_tag[i].text).group())
        years.append(year)
        publication.append(authortag_text[-1])
        author = authortag_text[0] + ' ' + re.sub(',','', authortag_text[1])
        journal = re.search("(?<=\-\s)(.*?)(?=\,)", author_tag[i].text).group(0)
        journals.append(journal)
        authors.append(author)
    return years, publication, authors, journals
paper_repos_dict = {
                    'Paper Title' : [],
                    'Year' : [],
                    'Author' : [],
                    'Journal': [],
                    'Publication' : [],
                    'Url of paper' : [] }

def add_in_paper_repo(papername, year, author, journal, publi, link):
    paper_repos_dict['Paper Title'].extend(papername)
    paper_repos_dict['Year'].extend(year)
    paper_repos_dict['Author'].extend(author)
    paper_repos_dict['Journal'].extend(journal)
    paper_repos_dict['Publication'].extend(publi)
    paper_repos_dict['Url of paper'].extend(link)

    return pd.DataFrame(paper_repos_dict)
import pandas as pd
from time import sleep
for i in range (0,110,10):
    url = "https://scholar.google.com/scholar?hl=ru&as_sdt=0%2C5&q=microbiota+dysbiosis+diet+lifestyle+study&btnG=".format(i)
    doc = get_paperinfo(url)
    paper_tag, link_tag, author_tag = get_tags(doc)
    papername = get_papertitle(paper_tag)
    year, publi, author, journal = get_author_year_publi_info(author_tag)
    link = get_link(link_tag)
    final = add_in_paper_repo(papername, year, author, journal, publi, link)
    sleep(30)
print(doc)
final.to_csv('microbita_bs.csv', sep=',', index=False,header=True)
print(final)
