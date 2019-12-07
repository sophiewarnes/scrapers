#!/usr/bin/env python
# coding: utf-8

import os
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

# Set up connection to Google API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('./fw-scraper-files/secret.json', scope)
client = gspread.authorize(creds)

# Open the Google sheet I want
sheet = client.open('fair-warning-stats').sheet1

## Open URLs and save all the data 

# Get list of all titles in current sheet
current_rows = sheet.col_values(4)

with open('URLs.csv','r') as csvfile:
    linkreader = csv.reader(csvfile, dialect=csv.excel)
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
                # Do nothing :)
                pass
            else:
                issue = issue.replace('Fair Warning - ','')
                link = link.get('href')
                link = link.strip()
                link = link.replace('?utm_campaign=Fair%20Warning&utm_medium=email&utm_source=Revue%20newsletter','')
                data = [issue, date, title, link]
                # Check if this data not already in the sheet. If it is, do nothing :) If not, write it in!
                if link in current_rows:
                    pass
                else:
                    sheet.insert_row(data, 2)
                    time.sleep(10)

