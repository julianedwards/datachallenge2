import networkx as nx
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
        if counter >= 3:
            break
        line_data = line.split(' ')
        feat_name = ' '.join(line_data[1:])
        feat_names.append(feat_name)
        counter += 1

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
            G.node[nodeID][feat_name] = node_data[feat_idx+1]

print(G.nodes(data=True))
