import graph

from types import ListType

class Node(object):

    include_bootstrap=False
    
    def __init__(self, label, **kwargs):
        self.label = label
        self.attributes = kwargs

    def __repr__(self):
        repr_str = self.label
        if self.include_bootstrap and self.attributes.has_key('bootstrap'):
            repr_str += '[' + str(self.attributes['bootstrap']) + ']'
        return repr_str

class Branch(object):

    def __init__(self, from_node, to_node, length=None, **attr):
        self.from_node = from_node
        self.to_node = to_node
        self.length = length
        self.attr = attr

class Tree(object):

    root = None
    show_interior_nodes = True
    show_branch_lengths = True

    def __init__(self):
        self._graph = graph.graph()

    def add_nodes(self, *nodes):
        self._graph.add_nodes(nodes)

    def add_branch(self, branch):
        if not self._graph.has_node(branch.from_node):
            self._graph.add_node(branch.from_node)
        if not self._graph.has_node(branch.to_node):
            self._graph.add_node(branch.to_node)
        if branch.length is not None:
            self._graph.add_edge(branch.from_node, branch.to_node, wt=branch.length)
        else:
            self._graph.add_edge(branch.from_node, branch.to_node)
        for k,v in branch.attr.iteritems():
            self._graph.add_edge_attributes(branch.from_node, branch.to_node, (k,v))

    def add_branches(self, *branches):
        for branch in branches:
            self.add_branch(branch)

    def terminal_nodes_iter(self):
        for n in self._graph.nodes():
            if self._graph.order(n) == 1:
                yield n

    def terminal_nodes(self):
        return list(x for x in self.terminal_nodes_iter())

    def internal_nodes_iter(self):
        for n in self._graph.nodes():
            if self._graph.order(n) > 1:
                yield n

    def internal_nodes(self):
        return list(x for x in self.internal_nodes_iter())

    def __repr__(self):

        root = self.root
        if root is None:
            # pick a 'random' internal node to be the root
            root = self.internal_nodes()[0]

        return self.node_to_str(root) + ';'

    def node_to_str(self, node, from_node=None):
        if self._graph.order(node) == 1 and node != self.root:
            node_str = str(node)
            if self.show_branch_lengths and from_node is not None:
                node_str += ':' + str(self._graph.get_edge_weight(from_node, node))
            return node_str
        neighbors = [x for x in self._graph.neighbors(node)]
        if from_node is not None and from_node in neighbors:
            neighbors.remove(from_node)
        str_elements = [self.node_to_str(n, node) for n in neighbors]
        tree_str = '(' + ','.join(str_elements) + ')'
        if self.show_interior_nodes:
            tree_str += str(node)
        if self.show_branch_lengths and from_node is not None:
            tree_str += ':' + str(self._graph.get_edge_weight(from_node, node))
        return tree_str

