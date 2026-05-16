import requests

ASSESSMENT_URL = "https://data.edmonton.ca/api/views/q7d6-ambg/rows.csv?accessType=DOWNLOAD"

r = requests.get(ASSESSMENT_URL, stream=True)
with open("data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv", "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)
