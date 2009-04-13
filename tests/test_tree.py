from oldowan.tree import Tree, Node, Branch

t = Tree()
t.add_branches(Branch('a','b'), Branch('b','c'), Branch('c','d'), Branch('c','e'))

def test_terminal_nodes():
    assert 'a' in t.terminal_nodes_iter()    
    assert 'd' in t.terminal_nodes_iter()
    assert 'e' in t.terminal_nodes_iter()
    assert 'b' not in t.terminal_nodes_iter()
    assert 'c' not in t.terminal_nodes_iter()

    tn = t.terminal_nodes()
    assert 'a' in tn
    assert 'd' in tn
    assert 'e' in tn
    assert 'b' not in tn
    assert 'c' not in tn

