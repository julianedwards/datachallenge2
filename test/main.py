import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=4)
G = nx.DiGraph()

FOLDER = ""
EDGE_FILE = "108541235642523883716.edges"
def make_full_path(folder, filename):
    # TODO: make this work
    return filename
    #return "/".join([folder, filename])

def get_line_data(line):
    return [int(nodeID) for nodeID in line.split()]

EDGE_FILE_FULL = make_full_path(FOLDER, EDGE_FILE)
with open(EDGE_FILE_FULL, 'r') as f:
    for line in f:
        nodeID1, nodeID2 = get_line_data(line)
        G.add_edge(nodeID1, nodeID2)
        # TODO: check indegree

FEATNAMES_FILE = "108541235642523883716.featnames"
feat_names = []
FEATNAMES_FILE_FULL = make_full_path(FOLDER, FEATNAMES_FILE)
with open(FEATNAMES_FILE_FULL, 'r') as f:
    # TODO: read more data
    counter = 0
    for line in f:
        line = line.rstrip()
        #if counter >= 3:
        #    break
        line_data = line.split(' ')
        feat_name = ' '.join(line_data[1:])
        feat_names.append(feat_name)
        #counter += 1

FEAT_FILE = "108541235642523883716.feat"
FEAT_FILE_FULL = make_full_path(FOLDER, FEAT_FILE)
with open(FEAT_FILE_FULL, 'r') as f:
    for line in f:
        line_data = get_line_data(line)
        nodeID = line_data[0]
        if nodeID not in G:
            G.add_node(nodeID)

        node_data = line_data[1:]
        for feat_idx in range(len(feat_names)):
            feat_name = feat_names[feat_idx]
            G.node[nodeID][feat_name] = node_data[feat_idx]

count1 = 0
count2 = 0
count3 = 0
for node_idx in G.nodes():
    node = G.node[node_idx]
    if node['last_name:jennifer'] == 1:
        if node['gender:1'] == 1:
            count1 += 1
        elif node['gender:2'] == 1:
            count2 += 1
        else:
            count3 += 1

#print(count1, count2, count3)
# plot male and female
male_idxes  = [idx for idx in G if G.node[idx]['gender:1'] == 1]
female_idxes = [idx for idx in G if G.node[idx]['gender:2'] == 1] 
centrality = nx.degree_centrality(G)
male_centrality = np.array([centrality[nodeID] for nodeID in centrality if nodeID in male_idxes])
female_centrality = np.array([centrality[nodeID] for nodeID in centrality if nodeID in female_idxes])
#central_vals = list(centrality.values())
#import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

x = np.random.normal(1, 2, 5000)
y = np.random.normal(-1, 3, 5000)
data = [male_centrality.T, female_centrality.T]
#data = np.vstack([male_centrality, female_centrality]).T
#bins = np.linspace(-10, 10, 30)

plt.hist(data, alpha=0.7, label=['x', 'y'])
plt.legend(loc='upper right')
plt.show()

#plt.hist(female_centrality)
#plt.title("Centrality Histogram")
#plt.xlabel("Centrality val")
#plt.ylabel("Frequency")
#plt.show()

'''
457 last_name:adam
458 last_name:adrian
556 last_name:nick
'''
'''
518 last_name:jennifer
539 last_name:laura
559 last_name:pamela
'''

#centrality = nx.degree_centrality(G)
#pp.pprint(centrality)
#print(centrality)
