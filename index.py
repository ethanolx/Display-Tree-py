from src.display_tree.tree import Tree

t = Tree('abdcaddashdo', children=[Tree('b', children=[Tree(122), Tree(2)]), Tree('c')])

# t.debug()
print(t.__str__().replace(' ', '+'))
# print(t)
