from indeed import get_indeed_jobs
import csv

indeed_jobs = get_indeed_jobs()
file = open("jobsearch.csv", mode='w')
writer = csv.writer(file)
writer.writerow(["company", "link", "location", "title"])
for job in indeed_jobs:
    writer.writerow(job.values())
file.close()
