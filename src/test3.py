from pathlib import Path

import dash
import dash_cytoscape as cyto
import dash_html_components as html

import pandas as pd

PATH_SRC = Path(__file__).resolve().parent
PATH_PROJECT = PATH_SRC.parent
PATH_DATA = PATH_PROJECT / 'data'

# print(str(PATH_SRC))
# print(str(PATH_PROJECT))
# print(str(PATH_DATA))

# df = pd.read_csv(str(PATH_DATA/'test2.csv'))
df = pd.read_csv(str(PATH_DATA/'network_banks_temp4.csv'))
df.dropna(inplace=True)
# print(df.head())


# source_list = df['source_id'].tolist()
# target_list = df['target_id'].tolist()

source_list = df['source_company'].tolist()
# print(source_list)
target_list = df['target_company'].tolist()
# print('target_list')
# print(target_list)
# print()

width_list = df['c_news'].tolist()

elem_set = set(source_list)
# print('elem_set')
# print(elem_set)
# print()

elem_set.update(target_list)
# print('updated elem_set')
# print(elem_set)
# print()

# remove nan from set
elem_set = {x for x in elem_set if x==x}

elem_list = list(elem_set)
# print('elem_list')
# print(elem_list)
# print()

# calculate node size
node_dict = {}

source_nodes = df[['source_company','c_news']].copy()
# print(source_nodes)

source_nodes = source_nodes.groupby(['source_company']).sum().reset_index()
# print('source_nodes')
# print(source_nodes)
# print()

node_list = source_nodes['source_company'].tolist()
# print(source_list)
node_size = source_nodes['c_news'].tolist()

node_dict = dict(zip(node_list, node_size))
# print('node_dict')
# print(node_dict)
# print()

target_nodes = df[['target_company','c_news']].copy()
target_nodes = target_nodes.groupby(['target_company']).sum().reset_index()

temp_node_list = target_nodes['target_company'].tolist()
# print(source_list)
temp_node_size = target_nodes['c_news'].tolist()

temp_node_dict = dict(zip(temp_node_list, temp_node_size))
# print('temp_node_dict')
# print(temp_node_dict)
# print()

for key in temp_node_dict:
    if key not in node_dict:
        node_dict[key] = temp_node_dict[key]

# print('node_dict')
# print(node_dict)
# print()

node_elements = []
edge_elements = []

# print('elem_list')
# print(elem_list)
# print()

for i in range(len(elem_list)):
    # print(elem_list[i])
    
    # print()
    # print(i)
    # print(source_list[i])
    # print(target_list[i])
    # print()

    if elem_list[i] not in node_dict:
        print('not found')
        print(elem_list[i])

    node = {
        'data': {'id': f"{elem_list[i]}", 'label': f"{elem_list[i]}"},
        'style': {'width': node_dict[elem_list[i]] // 10 + 10, 'height': node_dict[elem_list[i]] // 10 + 10}
        }
    node_elements.append(node)
# print(node_elements)

for i in range(len(source_list)):
    edge = {'data': {'source': f"{source_list[i]}", 'target': f"{target_list[i]}"},
            'style': {'width': width_list[i] // 5 + 2}}
    edge_elements.append(edge)
# print("edge_elements")
# print(edge_elements)


elements = node_elements.copy()
elements.extend(edge_elements)

# Load extra layouts
cyto.load_extra_layouts()

app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-network-analysis',
        layout={'name': 'cose-bilkent', 
                'padding': 10, 
                'nodeRepulsion': 4500000, 
                'idealEdgeLength': 300,
                'edgeElasticity': 0.45,
                'nestingFactor': 0.1,
                'gravity': 0.25,
                },
        style={'width': '100%', 'height': '800px'},
        elements=elements
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
