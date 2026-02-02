from exceptions import RED, CLEAR

# декоратор для добавления функции языку
def ml_function(function):
    data = {
            "type": "py",
            "call": function
            }
    ml_globals[function.__name__[:-1]] = data
    return function

ml_globals = {
    "true":True,
    "false":False,
    "void":None,
}
active_namespaces = [ml_globals]
def get_value(name: str):
    for namespace in active_namespaces[::-1]:
        if name in namespace:
            return namespace[name]
    else:
        raise NameError(f"{RED}Undefined name {CLEAR}{name}")
def add_namespace():
    active_namespaces.append({})
def pop_namespace():
    active_namespaces.pop(-1)
def write_value(name, value):
    active_namespaces[-1][name] = value
