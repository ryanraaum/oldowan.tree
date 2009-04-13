from oldowan.tree.newick import tokenize

def test_tokenize():
    trees = ['(a,b);',
             '(a,b)c;',
             '(a,(b,c));',
             '(a:0.1,b:0.2);',
             '(a:0.1,(b:0.2,c:0.2):0.4);',
             '(,,(,));',                            # no nodes are named
             '(A,B,(C,D));',                        # leaf nodes are named
             '(A,B,(C,D)E)F;',                      # all nodes are named
             '(:0.1,:0.2,(:0.3,:0.4):0.5);',        # all but root node have a distance to parent
             '(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);',    # distances and leaf names (popular)
             '(A:0.1,B:0.2,(C:0.3,D:0.4)E:0.5)F;',  # distances and all names
             '((B:0.2,(C:0.3,D:0.4)E:0.5)F:0.1)A;', # a tree rooted on a leaf node (rare)
             "(B,(A,C,E),D);",
             "(,(,,),);",
             "(_,(_,_,_),_);",
"""
(
  ('Chimp':0.052625,
   'Human':0.042375):0.007875,
  'Gorilla':0.060125,
  ('Gibbon':0.124833,
   'Orangutan':0.0971667):0.038875
); """,
"""
(
  ('Chimp':0.052625,
   'Human':0.042375) 0.71 : 0.007875,
  'Gorilla':0.060125,
  ('Gibbon':0.124833,
   'Orangutan':0.0971667) 1.00 :0.038875
); """,      
             "((raccoon, bear),((sea_lion,seal),((monkey,cat), weasel)),dog);",
             "((raccoon:19.19959,bear:6.80041):0.84600,((sea_lion:11.99700, seal:12.00300):7.52973,((monkey:100.85930,cat:47.14069):20.59201, weasel:18.87953):2.09460):3.87382,dog:25.46154);",
             "((raccoon:19.19959,bear:6.80041)50:0.84600,((sea_lion:11.99700, seal:12.00300)100:7.52973,((monkey:100.85930,cat:47.14069)80:20.59201, weasel:18.87953)75:2.09460)50:3.87382,dog:25.46154);",
             "((raccoon:19.19959,bear:6.80041):0.84600[50],((sea_lion:11.99700, seal:12.00300):7.52973[100],((monkey:100.85930,cat:47.14069):20.59201[80], weasel:18.87953):2.09460[75]):3.87382[50],dog:25.46154);",
             ]
    for t in trees:
        try:
            tokenize(t)
        except Exception, msg:
            assert False, 'Failed on tree %s\n%s' % (t, msg)
    
