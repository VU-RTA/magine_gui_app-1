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
    for i in new_g.nodes():
        new_g.node[i]['label'] = i
    return from_networkx(new_g)


def neighbors_including_cross_interactions(node, up, down):

    species = [node]
    if up:
        species += g.predecessors(node)
    if down:
        species += g.successors(node)

    sg = nx.subgraph(g, species)
    for i in sg.nodes():
        sg.node[i]['label'] = i
    return from_networkx(sg)


def neighbors(node, up, down, max_dist=1):

    sg = subgraph_gen.neighbors(node, up, down, max_dist)

    for i in sg.nodes():
        sg.node[i]['label'] = i
    return from_networkx(sg)


def path_between(source, end, bi_dir):

    new_g = subgraph_gen.shortest_paths_between_two_proteins(source, end,
                                                             bidirectional=bi_dir)
    for i in new_g.nodes():
        new_g.node[i]['label'] = i
    return from_networkx(new_g)


if __name__ == '__main__':
    # neighbors('BAX', True, False)
    # neighbors('BAX', False, True)
    # neighbors('BAX', True, True)
    create_subgraph('H2AFX,ATM,MRE11,RAD50,TP53BP1'.split(','))
