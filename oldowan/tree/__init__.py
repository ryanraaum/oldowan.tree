"""This is the oldowan.tree package."""

import os

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')).read().strip()

__all__ = ['Tree', 'Node', 'Branch']

from tree import Tree, Node, Branch
