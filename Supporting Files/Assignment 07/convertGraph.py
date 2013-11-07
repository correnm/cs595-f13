\begin{verbatim}
import json
import csv
import unicodecsv
import networkx as nx
from networkx.readwrite import json_graph

'''
We are given Zachary's karate club network in a GraphML file. The file
metadata describes:
Edge attribute 'weight' based on the number of common interactions.
Vertex attribute 'Faction' either 1 or 2, giving the faction of the
student after the split of the club. 
Vertex attribute 'name' for Author name. 

This function will convert the file to two JSON files for the nodes and links. The data from
the two files is combined into a single CSV file that will be the source for D3 graphing.

Author:  Corren McCoy, 2013
'''


# GraphML format retrieved from the Nexus repository
# http://www.nexus.igraph.org/api/dataset_info?id=1&format=html
G=nx.read_graphml("C:/Python27/myFiles/Assignment 7/karate.GraphML")
# write json formatted data
d = json_graph.node_link_data(G) # node-link format to serialize
# write json 
json.dump(d, open('C:/Python27/myFiles/Assignment 7/karate.json','w'))
jsonFile = open('C:/Python27/myFiles/Assignment 7/karate.json')
data = json.load(jsonFile)

# elements of interest for D3
nodes = data['nodes']
links = data['links']

# print json-formatted string
print json.dumps(nodes, sort_keys=True, indent=4)

# CSV file
nodeFile =open('C:/Python27/myFiles/Assignment 7/karateNodes.csv','wb+')
nodeFileCSV=csv.writer(nodeFile, delimiter=',')
index=0
node_dict={}
node_faction_dict={}
for x in nodes:
    print x['Faction'], x['id'], x['name']
    nodeFileCSV.writerow([index, x['Faction'], x['id'], x['name']])
    node_dict[index]=x['name']
    node_faction_dict[index]=x['Faction']
    index = index+1
nodeFile.close()

# print json-formatted string
print json.dumps(links, sort_keys=True, indent=4)
# CSV file
linkFile =open('C:/Python27/myFiles/Assignment 7/karateLinks.csv','wb+')
linkFileCSV=csv.writer(linkFile, delimiter=',')
for x in links:
    #print x['source'], x['target']
    source = int(x['source'])
    target=int(x['target'])
    linkFileCSV.writerow([node_dict[source], node_dict[target], 
    node_faction_dict[source], node_faction_dict[target]])
    
linkFile.close()
\end{verbatim}