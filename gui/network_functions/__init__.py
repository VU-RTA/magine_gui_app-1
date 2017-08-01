import networkx as nx
from gui.network_functions.networkx_tools import from_networkx
import os
from magine.networks.network_subgraphs import NetworkSubgraphs


_dir = os.path.dirname(__file__)
_g_path = os.path.join(_dir, 'networks',
                       'prac_challenge_2017_partial_data_painted.gml')

g = nx.read_gml(_g_path)
subgraph_gen = NetworkSubgraphs(g)


def small_graph():
    g = nx.DiGraph()
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'D')
    x = from_networkx(g)
    return x


def create_subgraph(list_of_species):

    new_g = subgraph_gen.shortest_paths_between_lists(list_of_species)
    for i in new_g.nodes():
        new_g.node[i]['label'] = i
    return from_networkx(new_g)
    # return None