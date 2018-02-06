import networkx as nx
from gui.network_functions.networkx_tools import from_networkx
import os
from magine.networks.network_subgraphs import NetworkSubgraphs


_g_path = os.path.join(os.path.dirname(__file__),
                       'networks',
                       'background_network.p')


g = nx.read_gpickle(_g_path)
subgraph_gen = NetworkSubgraphs(g)


def create_subgraph(list_of_species):

    new_g = subgraph_gen.shortest_paths_between_lists(list_of_species)
    return from_networkx(new_g)


def neighbors_including_cross_interactions(node, up, down):

    species = [node]
    if up:
        species += g.predecessors(node)
    if down:
        species += g.successors(node)

    sg = g.subgraph(species)
    return from_networkx(sg)


def neighbors(node, up, down, max_dist=1):

    sg = subgraph_gen.neighbors(node, up, down, max_dist)
    sg = _filter_edges(sg, 'complex')
    return from_networkx(sg)


def path_between(source, end, bi_dir):

    new_g = subgraph_gen.shortest_paths_between_two_proteins(source, end,
                                                             single_path=False,
                                                             bidirectional=bi_dir)
    return from_networkx(new_g)


def _filter_edges(graph, edge_type):
    to_remove = set()
    for i, j, d in graph.edges(data=True):
        # print(d.keys())
        if edge_type in d['interactionType']:
            to_remove.add((i, j))

    graph.remove_edges_from(to_remove)
    nodes = set(graph.nodes())
    for i in nodes:
        if graph.degree(i) == 0:
            graph.remove_node(i)
    return graph

if __name__ == '__main__':
    # neighbors('BAX', True, False)
    # neighbors('BAX', False, True)
    neighbors('CEPBP', True, True)
    # create_subgraph('H2AFX,ATM,MRE11,RAD50,TP53BP1'.split(','))
