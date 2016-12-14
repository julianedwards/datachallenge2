from scipy.stats import linregress
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os
import pprint
import pickle
import sys

pp = pprint.PrettyPrinter(indent=4)
G = nx.DiGraph()

# TODO set this differently for Julian
DATA_FOLDER = "/Users/benjaminlerner/Documents/Columbia/SocNet/datachallenge2/gplus"
EDGE_FILE = "108541235642523883716.edges"
def make_full_path(folder, filename):
    # TODO: make this work
    return filename
    #return "/".join([folder, filename])

def get_line_data(line):
    return [int(nodeID) for nodeID in line.split()]

def connect_edges(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            nodeID1, nodeID2 = get_line_data(line)
            G.add_edge(nodeID1, nodeID2)

FEATNAMES_FILE = "108541235642523883716.featnames"
FEATNAMES_FILE_FULL = make_full_path(DATA_FOLDER, FEATNAMES_FILE)
def organize_features(filepath):
    feat_names = []
    with open(filepath, 'r') as f:
        count = 0
        for line in f:
            if count >= 3:
                break
            line = line.rstrip()
            line_data = line.split(' ')
            feat_name = ' '.join(line_data[1:])
            feat_names.append(feat_name)
            count += 1
    return feat_names

FEAT_FILE = "108541235642523883716.feat"
FEAT_FILE_FULL = make_full_path(DATA_FOLDER, FEAT_FILE)
def assign_gender(filepath, feat_names):
    with open(filepath, 'r') as f:
        for line in f:
            line_data = get_line_data(line)
            nodeID = line_data[0]
            if nodeID not in G:
                G.add_node(nodeID)

            node_data = line_data[1:]
            for feat_idx in range(len(feat_names)):
                feat_name = feat_names[feat_idx]
                if len(feat_names) >= len(node_data):
                    print(len(feat_names), len(node_data))
                try:
                    G.node[nodeID][feat_name] = node_data[feat_idx]
                except:
                    print(filepath)
                    sys.exit(1)

def get_centrality():
    male_idxes  = [idx for idx in G if G.node[idx]['gender:1'] == 1]
    female_idxes = [idx for idx in G if G.node[idx]['gender:2'] == 1]
    # TODO: try different things
    #centrality = nx.degree_centrality(G)
    centrality = nx.in_degree_centrality(G)
    male_centrality = np.array([centrality[nodeID] for nodeID in centrality if nodeID in male_idxes])
    female_centrality = np.array([centrality[nodeID] for nodeID in centrality if nodeID in female_idxes])
    data = [male_centrality, female_centrality]
    return data

def get_regression(data):
    male_cent, female_cent = data
    num_males, num_females = male_cent.shape[0], female_cent.shape[0]
    zeros = np.zeros((num_males, 1))
    ones = np.ones((num_females, 1))
    X = np.concatenate((zeros, ones))
    Y = np.concatenate((male_cent, female_cent))
    # TODO: why are we getting errors in sqrt?
    res = linregress(X.T, Y.T)
    return res

def collect_filenames(folder):
    paths = os.listdir(folder)
    num_files = len(paths)
    edge_files, feat_files = [], []
    for idx in range(0, num_files, 6):
        edge_file = folder + os.sep + paths[idx+1]
        edge_files.append(edge_file)

        feat_file = folder + os.sep + paths[idx+3]
        feat_files.append(feat_file)

    return edge_files, feat_files

if __name__ == "__main__":
    SAVED = True
    GRAPH_PICKLE = "graph.pickle"
    FEAT_PICKLE = "feat.pickle"
    DATA_FILE = "data.pickle"

    if SAVED:
        G = pickle.load(open(GRAPH_PICKLE, "rb"))
        feat_names = pickle.load(open(FEAT_PICKLE, 'rb'))
        #data = pickle.load(open(DATA_FILE, 'rb'))
    else:
        edge_files, feat_files = collect_filenames(DATA_FOLDER)
        feat_names = organize_features(FEATNAMES_FILE_FULL)
        for edge_file, feat_file in zip(edge_files, feat_files):
            connect_edges(edge_file)
            # TODO: make this better than a hardcode puhlease
            assign_gender(feat_file, feat_names)

        pickle.dump(G, open(GRAPH_PICKLE, 'wb'))
        pickle.dump(feat_names, open(FEAT_PICKLE, 'wb'))
        #pickle.dump(data, open(DATA_FILE, 'wb'))

    data = get_centrality()
    regression = get_regression(data)
    print(regression)
