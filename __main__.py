from .registry import get_nodes
import json

print(json.dumps(get_nodes(), indent=4, sort_keys=True))
