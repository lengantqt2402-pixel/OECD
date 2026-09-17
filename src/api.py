import requests
import xml.etree.ElementTree as ET

url = (
    "https://sdmx.oecd.org/public/rest/v1/"
    "data/OECD.SDD.TPS,DSD_PDB@DF_PDB,2.0/all"
    "?startPeriod=2014"
    "&endPeriod=2023"
    "&dimensionAtObservation=AllDimensions"
)

headers = {
    "Accept": "text/csv"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print(response.text[:3000])