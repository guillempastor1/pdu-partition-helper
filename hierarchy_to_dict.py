import json

# hierarchical_text = [("/A", 30),
#                      ("/A/B", 10),
#                      ("/A/C", 20),
#                      ("/A/C/D", 10),
#                      ("/A/C/E", 10)]

hierarchical_text = []
file_path = "directory_structure.txt"

with open(file_path, "r") as file:
    for line in file:
        parts = line.split('\t')
        if len(parts) == 2:
            size = int(parts[0])
            directory = parts[1].strip()
            hierarchical_text.append((directory, size))

sep_char = "/"

def fillAreas(node, tree, areas):
    if len(tree[node]) == 0: return areas[node]

    areas[node] = 0
    for child in tree[node]:
        areas[node] += fillAreas(child, tree, areas)
    
    return areas[node]


def make_tree(h_text):
    h_text = [(s.replace(sep_char, chr(0)), w) for s, w in h_text]
    print("begin")
    h_text.sort()
    print("sorting is done")
    h_text = [(s.replace(chr(0), sep_char), w) for s, w in h_text]

    root, root_ar = h_text[0]

    tree = {root: []}
    areas = {root: root_ar}
    for i in range(1, len(h_text)):
        dir, dir_area = h_text[i]

        parent = dir[:dir.rfind(sep_char)]
        tree[parent].append(dir)
        
        tree[dir] = []
        areas[dir] = dir_area

    # fill areas properly
    fillAreas(root, tree, areas)
    return tree, root, areas

def dfs(tree, node, areas, depth, max_depth = 100):
    if depth > max_depth: return
    print("  " * depth, node, areas[node])

    for child in tree[node]:
        dfs(tree, child, areas, depth + 1, max_depth)

def build_tree(node, parent, tree, areas):
    return {
        "parent": parent,
        "name": node[node.rfind(sep_char):],
        "full_name": node,
        "in_cut": False,
        "area": areas[node],
        "uncut_area": areas[node],
        "children": [build_tree(child, node, tree, areas) for child in tree.get(node, [])]
    }

tree, root, areas = make_tree(h_text=hierarchical_text)
dfs(tree, root, areas, 0, 1)

json_tree = build_tree(root, "null", tree, areas)

json_string = json.dumps(json_tree)
with open("/home/guillem/projects/Floorplanning/input_graph_tree.json", "w") as f:
    f.write(json_string)
