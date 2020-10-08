import requests
import json
from xml.etree import ElementTree as ET

# Step 2: Provide input content. (Use the default or provide your own.)
# Step 2A, leave the default URL, or enter a URL to any HTML content.
# OR Step 2B, type or copy plain text content. 
# If you choose Step 2B, comment the lines under Step 2A, and uncomment the lines under Step 2B.
# (Finally, click to select this cell and click Run.)

# Step 2A Provide URL to html content.
url = "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15"
headers = {}
HTMLResponse = requests.request("GET", url, headers=headers)
contentText = HTMLResponse.text
headType = "text/xml"

# Step 2B Alternatively, provide plain text.
# contentText = "Type or copy your plain text here."
# headType = "text/raw"

root = ET.fromstring(contentText)

for child in root.iter('item'):
    print(child.attrib)