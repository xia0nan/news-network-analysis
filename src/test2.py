from pathlib import Path

import dash
import dash_cytoscape as cyto
import dash_html_components as html

# import pandas as pd

# PATH_SRC = Path(__file__).resolve().parent
# PATH_PROJECT = PATH_SRC.parent
# PATH_DATA = PATH_PROJECT / 'data'

# # print(str(PATH_SRC))
# # print(str(PATH_PROJECT))
# # print(str(PATH_DATA))

# df = pd.read_csv(str(PATH_DATA/'test2.csv'))
# # print(df.head())

# source_list = df['source_id'].tolist()
# target_list = df['target_id'].tolist()
# # print(source_list)
# # print(target_list)

# elem_set = set(source_list)
# elem_set.update(target_list)
# elem_list = list(elem_set)

# node_elements = []
# edge_elements = []

# for i in range(len(elem_list)):
#     # print(elem_list[i])
    
#     # print()
#     # print(i)
#     # print(source_list[i])
#     # print(target_list[i])
#     # print()

#     node = {
#         'data': {'id': f"{elem_list[i]}", 'label': f"{elem_list[i]}"},
#       2*i}
#     }
#     node_elements.append(node)
# # print("node_elements")
# # print(node_elements)

# for i in range(len(source_list)):
#     edge = {'data': {'source': f"{source_list[i]}", 'target': f"{target_list[i]}"}}
#     edge_elements.append(edge)
# # print("edge_elements")
# # print(edge_elements)


# elements = node_elements.copy()
# elements.extend(edge_elements)


app = dash.Dash(__name__)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-network-analysis',
        layout={
            'name': 'cose',
            'nodeRepulsion': 4500,

        },
        style={'width': '100%', 'height': '400px'},
        elements=[
            {'data': {'id': '1', 'label': '1'}, 'style': {'background-color': '#FF4136'}}, 
            {'data': {'id': '2', 'label': '2'}, 'style': {'width': 100, 'height':100}}, 
            {'data': {'id': '3', 'label': '3'},'style': {'background-color': 'blue'}}, 
            {'data': {'id': '4', 'label': '4'}}, 
            {'data': {'id': '5', 'label': '5'}}, 
            {'data': {'id': '6', 'label': '6'}}, 
            {'data': {'source': '1', 'target': '2'}, 'style': {'width': 10}}, 
            {'data': {'source': '1', 'target': '3', 'weight': 10}}, 
            {'data': {'source': '1', 'target': '4'}, 'style': {'line-color': 'orange'}}, 
            {'data': {'source': '2', 'target': '3'}}, 
            {'data': {'source': '2', 'target': '4'}}, 
            {'data': {'source': '2', 'target': '5'}}, 
            {'data': {'source': '3', 'target': '4'}}, 
            {'data': {'source': '3', 'target': '5'}}, 
            {'data': {'source': '3', 'target': '6'}}
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
