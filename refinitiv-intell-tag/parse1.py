import json
import pandas as pd


def parse_response(fname):

	with open(fname) as json_file:
	    data = json.load(json_file)


	entity_list = []

	for key, value in data.items():
		if key == 'doc':
			continue
		# print(data[key]['_typeGroup'])
		try:
			if data[key]['_typeGroup'] == 'entities' \
				and data[key]['_type'] in ['City', 'Person', 'Organization', 'Company']:
				
				if data[key]['_type'] == 'City':
					name = data[key]['name']
					permid = '-1'
					dtype = data[key]['_type']

				if data[key]['_type'] == 'Person':
					name = data[key]['name']
					permid = data[key]['permid']
					dtype = data[key]['_type']

				if data[key]['_type'] == 'Organization':
					name = data[key]['name']
					permid = data[key]['permid']
					dtype = data[key]['_type']

				if data[key]['_type'] == 'Company':
					name = data[key]['name']
					permid = data[key]['resolutions'][0]['permid']
					dtype = data[key]['_type']

				entity_list.append([name, dtype, permid])

		except Exception:
			print("%%%%")
			print(data[key])
			break


	df = pd.DataFrame (entity_list, columns=['name','dtype','permid'])

	df.to_csv(fname.replace('json', 'csv'), index=False)

if __name__ == '__main__':
	parse_response('refinitiv_response.json')
