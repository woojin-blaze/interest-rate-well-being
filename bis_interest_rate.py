import json
import requests
import pprint
import pandas as pd

urls = ["https://stats.bis.org/api/v2/data/dataflow/BIS/WS_CBPOL/1.0/M.AR+AU+BR+CA+CH+CL+CN+CO+CZ+DK+GB+HK+HR+HU+ID+IL+IN+IS+JP+KR+MA+MK+MX+MY+NO+NZ+PE+PH+PL+RO+RS+RU+SA+SE+TH+TR+US+XM+ZA?startPeriod=2000-01-01&endPeriod=2024-10-16&format=sdmx-json"]
data = [json.loads(requests.get(url).content) for url in urls]
#pprint.pprint(json.dumps(data[0])[:1200])
country_abbv = []
for i, val in enumerate(data):
    for item in data[i]["data"]["structure"]["dimensions"]["series"][1]['values']:
        country_abbv.append(item)
        
country_list = []
for item in country_abbv: 
    country_list.append(item["id"])
    
new_list = []
for i, val in enumerate(data):
    for key, value in data[i]["data"]["dataSets"][0]["series"].items():
        alist = []
        for k, val in value["observations"].items():
            alist.append(val[0])
        new_list.append(alist)
        
interest_rate_dict = dict(zip(country_list, new_list))
dates = pd.date_range(start="2000-01", end="2024-09", freq='MS') 
rows = []
us_rows = []
for country, values in interest_rate_dict.items():
    for date, value in zip(dates, values):
        rows.append({'Country': country, 'Date': date.strftime("%Y-%m"), 'Interest Rate': round(float(value), 2)})
        if country == 'US': 
            us_rows.append({'Country': country, 'Date': date.strftime("%Y-%m"), 'Interest Rate': round(float(value), 2)})
        
df = pd.DataFrame(rows)
df.to_csv('interest_rate.csv', index=False)
df=pd.DataFrame(us_rows)
df.to_csv('us_interest_rate.csv', index=False)