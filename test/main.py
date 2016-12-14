import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pprint
import os

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

def connect_edges(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            nodeID1, nodeID2 = get_line_data(line)
            G.add_edge(nodeID1, nodeID2)
            # TODO: check indegree

FEATNAMES_FILE = "108541235642523883716.featnames"
FEATNAMES_FILE_FULL = make_full_path(FOLDER, FEATNAMES_FILE)
def organize_features(filepath):
    feat_names = []
    with open(filepath, 'r') as f:
        for line in f:
            count = 0
            while count < 3:
                line = line.rstrip()
                line_data = line.split(' ')
                feat_name = ' '.join(line_data[1:])
                feat_names.append(feat_name)
                count += 1
    return feat_names

FEAT_FILE = "108541235642523883716.feat"
FEAT_FILE_FULL = make_full_path(FOLDER, FEAT_FILE)
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
                G.node[nodeID][feat_name] = node_data[feat_idx]

def get_centrality():
    male_idxes  = [idx for idx in G if G.node[idx]['gender:1'] == 1]
    female_idxes = [idx for idx in G if G.node[idx]['gender:2'] == 1] 
    centrality = nx.degree_centrality(G)
    male_centrality = np.array([centrality[nodeID] for nodeID in centrality if nodeID in male_idxes])
    female_centrality = np.array([centrality[nodeID] for nodeID in centrality if nodeID in female_idxes])
    data = [male_centrality.T, female_centrality.T]
    return data

