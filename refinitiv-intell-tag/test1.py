# This Python code example does the following:
# - Uses the Refinitiv Intelligent Tagging (TRIT) API to tag content.
# - Extracts the primary RICs (Reuters Instrument Codes) from the tagging output.
# - Passes these instruments to the Monitor application on Eikon Desktop.

# How to use this sample code
# Run the code in Steps 1, 2, 3, 4 to observe the Intelligent Tagging API call and output.

# Step 1: Import required libraries (Click to select this cell and click Run.)
import requests
import json

# Step 2: Provide input content. (Use the default or provide your own.)
# Step 2A, leave the default URL, or enter a URL to any HTML content.
# OR Step 2B, type or copy plain text content. 
# If you choose Step 2B, comment the lines under Step 2A, and uncomment the lines under Step 2B.
# (Finally, click to select this cell and click Run.)

# Step 2A Provide URL to html content.
url = "http://feeds.reuters.com/reuters/topNews"
headers = {}
HTMLResponse = requests.request("GET", url, headers=headers)
contentText = HTMLResponse.text
headType = "text/html"

# Step 2B Alternatively, provide plain text.
# contentText = "Type or copy your plain text here."
# headType = "text/raw"

print(contentText)

# Step 3: Trigger the Intelligent Tagging API and get the tagging response.

# Provide a valid access token. And then click to select this cell and click Run.
token = 'THRhYE6zoRop67WudW2CVofKADFGemsb'
url = "https://api-eit.refinitiv.com/permid/calais"
payload = contentText.encode('utf8')
headers = {
    'Content-Type': headType,
    'X-AG-Access-Token': token,
    'outputformat': "application/json"
    }
 
TRITResponse = requests.request("POST", url, data=payload, headers=headers)
TRITTextResponse = TRITResponse.text

print(TRITTextResponse)

# Step 4 Extract Instrument Codes from the Intelligent Tagging response and put in RICList variable. (Select this cell and click Run.)
TRITJsonResponse = json.loads(TRITTextResponse)
TRITJsonResponse

RICList = []

for entity in TRITJsonResponse:
    #print(entity)
    for info in TRITJsonResponse[entity]:
        if (info =='resolutions'):
            #print("\t" + info)
            #print(type(info))
            for companyinfo in (TRITJsonResponse[entity][info]):
                #print(companyinfo)
                if 'primaryric' not in companyinfo:
                    continue
                print(companyinfo['primaryric'])
                RICList.append(companyinfo['primaryric'])
                
                
print(RICList)


####### Recap: Steps 1 to 4 used the Intelligent Tagging API to get the companies mentioned in the text.#######


# Next, we'll use the Intelligent Tagging data as input for the Eikon Side by Side Integration API (SxS API).
# Step 1: Test that Eikon is running on port 9000. The Eikon Desktop should be running on your machine.
url = "http://127.0.0.1:9000/ping"
headers = {}
response = requests.request("GET", url, headers=headers)

print(response.text)

# Step 2: Get Side by Side API token from Eikon Desktop.
# Provide a valid productId and ApiKey.
productId = "<valid_eikon_product_id>"
ApiKey = "<valid_eikon_apikey>"

url = "http://127.0.0.1:9000/sxs/v1"

payloadJson = json.loads("{}")
payloadJson['command'] = 'handshake'
payloadJson['productId'] = productId
payloadJson['apiKey'] = ApiKey

payload = json.dumps(payloadJson)
headers = {'Content-Type': "application/json"}

response = requests.request("POST", url, data=payload, headers=headers)

EikonJsonResponse = json.loads(response.text)
sessionKey = EikonJsonResponse['sessionToken']

print(sessionKey)

# Step 3: Prepare SxS command from RICList (extracted from the Intelligent Tagging output)

EntitiesJson = json.loads("{}")
EntitiesJson['entities'] = []

for ric in RICList:
    EntityJson = json.loads("{}")
    EntityJson['RIC'] = ric
    EntitiesJson['entities'].append(EntityJson)
    

commandJson = json.loads("{}")
commandJson['command'] = 'launch'
commandJson['sessionToken'] = sessionKey
commandJson['appId'] = "THOMSONREUTERS.REALTIME.THINMONITOR"
commandJson['context'] = json.dumps(EntitiesJson)

commandString = json.dumps(commandJson)

print(commandString)

# Step 4: Call SxS API to open a monitor app on Eikon Desktop.
# This should open a new Monitor app on Eikon Desktop with the relevant instrument codes displayed.
url = "http://127.0.0.1:9000/sxs/v1"
headers = {
    'Content-Type': "application/json",
    }

response = requests.request("POST", url, data=commandString, headers=headers)

print(response.text)
