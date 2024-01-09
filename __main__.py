from .registry import get_nodes
import json
import pathlib

f = pathlib.Path(__file__).parent / 'node_list.json'
j = json.dumps(get_nodes(), indent=4, sort_keys=True)
print(j)
f.write_text(j)
