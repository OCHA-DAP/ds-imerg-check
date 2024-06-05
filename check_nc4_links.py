import os
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

# URLs to check
urls = {
    "late": "https://gpm1.gesdisc.eosdis.nasa.gov/data/"
    "GPM_L3/GPM_3IMERGDL.06/2024/06/",
    "early": "https://gpm1.gesdisc.eosdis.nasa.gov/data/"
    "GPM_L3/GPM_3IMERGDE.06/2024/06/",
}

# Initialize empty list to hold results
results = []

# Get the current time
current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

for label, url in urls.items():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    nc4_links = [
        a["href"]
        for a in soup.find_all("a", href=True)
        if a["href"].endswith(".nc4")
    ]
    for link in nc4_links:
        results.append(
            {"link": link, "first_seen": current_time, "label": label}
        )

# Check if results.csv exists
if os.path.exists("results.csv"):
    df = pd.read_csv("results.csv")
else:
    df = pd.DataFrame(columns=["link", "first_seen", "label"])

# Add new links
for result in results:
    if result["link"] not in df["link"].values:
        df = df.append(result, ignore_index=True)

# Save to CSV
df.to_csv("results.csv", index=False)
