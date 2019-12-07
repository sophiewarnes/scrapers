#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup
import csv
import codecs
import re

# Open local file
soup = BeautifulSoup(open("local_file_path.htm"), "html.parser")

# Open URL
r = requests.get("url_goes_here")
soup = BeautifulSoup(r.content)

## Scrape the URL or file, and pull out all the links

# Read the file

lines = open('./fw-scraper-files/URLs.csv', 'r').read()

# Open CSV file we're going to append data to...
with open('./fw-scraper-files/URLs.csv','a') as csvfile:
    csv_output = csv.writer(csvfile)
    
    # Find all links where 'Fair Warning' is in the title at the beginning, and extract the href (URL)
    links = soup.find_all('a',{'title': re.compile('Fair Warning.*')})
    
    # For every link found that matches the regex above, add http and domain
    for link in links:
        urls = link.get('href')
        # This bit only needed when scraping live site, as URLs are relative
        urls = "https://www.getrevue.co" + urls
        
        if urls in lines:
            pass
        else:
            # If 'tinyletter' string is not in the URL, then write the row. (Ensures it won't fail)
            if 'tinyletter' not in urls:
                csv_output.writerow([urls])
            
print("Executed successfully! \U0001F600")


## Put all the data into a CSV file and clean all the nonsense up

print("This may take a while... \U0001F643")

lines = open('./fair-warning/data/fw-archive.csv', 'r').read()

# Open URLs CSV, write title, link, date etc to URLS.csv
with open('./fw-scraper-files/URLs.csv','r') as csvfile, open('./fair-warning/data/fw-archive.csv', 'a', encoding='utf-8') as f_output:
    linkreader = csv.reader(csvfile, dialect=csv.excel)
    csv_output = csv.writer(f_output)
    for row in linkreader:
        URL = ', '.join(row)
        r = requests.get(URL)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")
        issue = soup.find("h1").text
        date = soup.find("time").text
        links = soup.find_all("a",{'style': re.compile('text-decoration: none'),'href': re.compile('www.*')})
        for link in links:
            title = link.text
            title = title.strip()
            if title == "" or title == "Tweet" or title == "Share":
                # Do nothing
                pass
            else:
                issue = issue.replace('Fair Warning - ','')
                title = title
                link = link.get('href')
                link = link.strip()
                link = link.replace('?utm_campaign=Fair%20Warning&utm_medium=email&utm_source=Revue%20newsletter','')
                data = [issue, date, title, link]
                if title in lines:
                    pass
                else:
                    print("New data incoming! \U0001F44D")
                    csv_output.writerow([issue,date,title,link])
                
print("\n\nOh look, it's finished. Hurrah! \U0001F600")

