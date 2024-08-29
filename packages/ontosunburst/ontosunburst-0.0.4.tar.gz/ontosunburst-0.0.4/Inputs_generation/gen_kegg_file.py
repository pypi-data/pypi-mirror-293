import inspect
import kegg2bipartitegraph
import os
import json


def update_dict(dict_1, dict_2):
    for key, value in dict_2.items():
        if key not in dict_1:
            dict_1[key] = value
        else:
            dict_1[key].extend(value)
    return dict_1


def get_parents(data_dict):
    parent_child = {}
    for key, values in data_dict.items():
        for value in values:
            if value not in parent_child:
                parent_child[value] = [key]
            else:
                parent_child[value].append(key)
        if isinstance(values, dict):
            parent_child = update_dict(parent_child, get_parents(values))
    return parent_child


k2bg_init_file = inspect.getfile(kegg2bipartitegraph)
data_path = k2bg_init_file.replace('__init__.py', 'data')
json_hierarchy = os.path.join(data_path, 'kegg_model', 'kegg_hierarchy.json')
with open(json_hierarchy, 'r') as open_json_file:
    json_data = json.load(open_json_file)


# Create dictionary for sunburst creation.
sunburst_dict = get_parents(json_data)
root = 'kegg'
for sub_root in json_data.keys():
    sunburst_dict[sub_root] = [root]

# for hierarchy in json_data:
#     sunburst_hierarchy = get_parents(json_data[hierarchy])

with open("kegg_onto.json", 'w') as open_json_file:
    json.dump(sunburst_dict, open_json_file, indent=4)