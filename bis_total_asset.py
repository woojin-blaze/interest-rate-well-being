import json
import requests
import pprint
import re
import pandas as pd

urls = ["https://stats.bis.org/api/v2/data/dataflow/BIS/WS_CBTA/1.0/A.AE+AR+AU+BR+CA+CH+CL+CN+DK+GB+IN+JP+KR+SA+SE+SG+TH+TR+XM+ZA..USD?startPeriod=2014-01-01&endPeriod=2024-07-25&format=sdmx-json",
        "https://stats.bis.org/api/v2/data/dataflow/BIS/WS_CBTA/1.0/A.US.B.XDC.USD.N?startPeriod=2013-12-31&endPeriod=2024-09-30&format=sdmx-json"]

data = [json.loads(requests.get(url).content) for url in urls]
#pprint.pprint(json.dumps(data[0])[:1200])
#print(data[0]["data"]["dataSets"][0]["series"]["0:0:0:0:0:0"]["observations"])
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
        #s = re.search('0:(\d+):0:0:0:0',item).group(1)
        #print(s)
        #print(value["observations"])
        alist = []
        for k, val in value["observations"].items():
            alist.append(val[0])
        new_list.append(alist)
    
#print(new_list)
#print(data[0]["data"]["dataSets"][0]["series"]["0:0:0:0:0:0"]["observations"])
total_asset_dict = dict(zip(country_list, new_list))
pprint.pprint(total_asset_dict)
years = list(range(2014, 2024))
rows = []
for country, values in total_asset_dict.items():
    for year, value in zip(years, values):
        rows.append({'Country': country, 'Year': year, 'Total Asset':round(float(value), 3)})
df = pd.DataFrame(rows)
print(country_abbv)
df.to_csv('sample_total_assets.csv', index=False)