import requests
import json
from bs4 import BeautifulSoup

LIMIT = 50
URL = "https://www.indeed.ca/jobs?as_and=software+engineer&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=fulltime&st=&as_src=&salary=&radius=25&l=Canada&fromage=15&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"


def extract_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class": "pagination"})
    anchors = pagination.find_all('a')
    pages = []
    for anchor in anchors[:-1]:
        pages.append(int(anchor.string))
    return pages[-1]


def extract_jobs(lastPage):
    jobs = []
    for page in range(lastPage):
        print("Scrapping page {}".format(page))
        result = requests.get(URL+"&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            title = result.find("h2", {"class": "title"}).find('a')["title"]
            company = result.find("span", {"class": "company"})
            anchor_check = company.find("a")
            if company.find("a"):
                company = str(company.find("a").string)
            else:
                company = str(company.string)
            company = company.strip()
            location = result.find("div", {"class": "recJobLoc"})[
                "data-rc-loc"]
            job_id = result["data-jk"]
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "link": "https://www.indeed.ca/viewjob?jk="+job_id
            })
    return eval(json.dumps(jobs))
