import requests

url = "https://api-eit.refinitiv.com/permid/calais"

TITLE = "Seattle Passes Minimum Pay Rate for Uber and Lyft Drivers"
BODY = """
The Seattle City Council approved a minimum pay standard for Uber and Lyft drivers on Tuesday, becoming the second city in the country to do so.\n\nUnder the law, effective in January, ride-hailing companies must pay a sum roughly equivalent, after expenses, to the city’s $16 minimum hourly wage for businesses with more than 500 employees.\n\n“The pandemic has exposed the fault lines in our systems of worker protections, leaving many frontline workers like gig workers without a safety net,” Mayor Jenny Durkan said in a statement.\n\nSeattle’s law, passed in a 9-to-0 vote, is part of a wave of attempts by cities and states to regulate gig-economy transportation services. It is modeled on a measure that New York City passed in 2018. Last year, California approved legislation effectively requiring Uber and Lyft to classify drivers as employees rather than independent contractors, which would assure them of protections like a minimum wage, overtime pay, workers’ compensation and unemployment insurance. The companies are backing an initiative on the November ballot that would exempt their drivers from the California law.\n\nUber and Lyft have received more favorable treatment from federal regulators. Last week, the Labor Department proposed a rule that would probably classify their drivers as contractors, though it would not override state laws like California’s.\n\nAs in New York, the Seattle law will create a formula for minimum compensation for each trip — a combination of per-minute and per-mile rates that are “scaled up” by what is known as the utilization rate, or the fraction of each hour during which drivers have a passenger in their car. The idea is that a lower utilization rate should correspond to a higher per-minute and per-mile rate, to compensate drivers for being less busy.\n\nThe formula is intended to produce hourly pay of just under $30 before expenses and to motivate the companies to keep their drivers busier rather than flood the market with cars to reduce passengers’ waits.\n\nA Lyft spokesman, CJ Macklin, said, “The city’s plan is deeply flawed and will actually destroy jobs for thousands of people — as many as 4,000 drivers on Lyft alone — and drive ride-share companies out of Seattle.”\n\nUber declined to comment, but said in a recent letter to the Seattle City Council that New York’s policy had resulted in fewer rides and higher prices for passengers, and that it had led the company to restrict the number of drivers on the platform at once.\n\nHow Yurts and Heat Lamps Will Save New York’s Restaurants\nMichael Reich, a labor economist at the University of California, Berkeley, who was an architect of the New York measure and advised Seattle on its new law, said that average driver pay had increased in New York and that overall revenue had risen enough to offset the drop in demand because of higher fares.\n\nThe growth in rides slowed after the policy went into effect, Mr. Reich said, but added that this was largely for reasons unrelated to the policy.\n\nBeyond the pay standard, the Seattle measure stipulates that the companies must hand over all tips to drivers, that the tips cannot count toward the minimum and that the companies must provide protective equipment like masks to drivers or reimburse them for these costs.\n\nA broader program proposed by Ms. Durkan, Fare Share, was approved last fall. The agenda included a tax on Uber and Lyft of 51 cents a ride, part of which has helped fund a streetcar project downtown and provide support for drivers, including help with appeals if they are removed from either platform.\n\nThe Fare Share measure required the city to set a minimum pay standard for ride-hailing drivers, but mandated a study to determine the amount.
"""

payload = f"<Document>\n<Title> {Title} </Title>\n<Body> {BODY} </Body>\n</Document>"


headers = {
  'Content-Type': 'text/html',
  'x-ag-access-token': 'THRhYE6zoRop67WudW2CVofKADFGemsb',
  'outputformat': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))