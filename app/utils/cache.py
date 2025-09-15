from collections import OrderedDict

CACHE_SIZE = 100  # máximo 100 elementos
tools_cache = OrderedDict()


def set_cached_tool(tool_name: str, params: dict, result):
    key = f"{tool_name}:{str(params)}"
    if key in tools_cache:
        tools_cache.move_to_end(key)
    tools_cache[key] = result
    if len(tools_cache) > CACHE_SIZE:
        tools_cache.popitem(last=False)


def get_cached_tool(tool_name: str, params: dict):
    key = f"{tool_name}:{str(params)}"
    return tools_cache.get(key)
