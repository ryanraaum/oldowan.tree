from pyparsing import *
from tree import Tree, Branch, Node

lparen  = Literal('(').suppress()
rparen  = Literal(')').suppress()
colon   = Literal(':').suppress()
comma   = Literal(',')
tree_end= Literal(';')
lbrack  = Literal('[').suppress()
rbrack  = Literal(']').suppress()

label   = Word(alphanums + '_-.') | quotedString
fnumber = Combine(Word(nums) + Optional('.' + Optional(Word(nums))))

terms   = Forward()
brlen   = colon + fnumber
boot    = lbrack + fnumber + rbrack
clade   = Group(lparen + terms + rparen + \
            Optional(label).setResultsName('label') + \
            Optional(brlen).setResultsName('brlen') + \
            Optional(boot).setResultsName('boot')).setResultsName('clade')
entry   = Group(label.setResultsName('label') + Optional(brlen).setResultsName('brlen') \
           | brlen.setResultsName('brlen')).setResultsName('entry') 
terms   << OneOrMore(entry | comma | clade)
query   = terms.setResultsName('tree') + tree_end

def tokenize(s):
    return query.parseString(s)

def is_entry(x):
    if not hasattr(x, 'getName'):
        return False
    return x.getName() == 'entry'

def is_clade(x):
    if not hasattr(x, 'getName'):
        return False
    return x.getName() == 'clade'

def is_comma(x):
    return x == ','

def parse(s):
    try:
        tokens = tokenize(s)['tree']
    except:
        raise Exception, "tree could not be parsed"

    t = Tree()

    evaluate(tokens, t)

    return t

def extract_label(item):
    if item.asDict().has_key('label'):
        return item['label']
    return ''

def extract_boot(item):
    if item.asDict().has_key('boot'):
        return item['boot']
    return None

def extract_brlen(item):
    if item.asDict().has_key('brlen'):
        return item['brlen'][0]
    return None

def evaluate(item, tree, from_node=None):
    if is_clade(item):
        interior_node = Node(extract_label(item))
        boot = extract_boot(item)
        if boot is not None:
            interior_node.attributes['bootstrap'] = boot
        if from_node is not None:
            tree.add_branch(Branch(from_node, interior_node, extract_brlen(item)))
        if from_node is None:
            tree.root = interior_node
        for x in item:
            evaluate(x, tree, interior_node)
    elif is_entry(item):
        terminal_node = Node(extract_label(item))
        if from_node is not None:
            tree.add_branch(Branch(from_node, terminal_node, extract_brlen(item)))
    elif is_comma(item):
        pass
    else:
        pass

