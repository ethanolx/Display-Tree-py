from src.display_tree.tree import Tree

t = Tree('abdcaddashdo', children=[Tree('b', children=[Tree(122), Tree(2)]), Tree('c')])

t.debug()

print('\n---\n')

print(t.__str__().replace(' ', '.'))

#   0         1
#   123456789 12
#   abdcaddashdo
#       /   \
#       b   c
#      /  \
#     122 2
