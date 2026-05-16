import requests
from pathlib import Path

ASSESSMENT_URL = "https://data.edmonton.ca/api/views/q7d6-ambg/rows.csv?accessType=DOWNLOAD"
OUTPUT = Path(__file__).parent.parent / "data" / "raw" / "Property_Assessment_Data__Current_Calendar_Year_.csv"

r = requests.get(ASSESSMENT_URL, stream=True)
with open(OUTPUT, "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)
