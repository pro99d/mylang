from exceptions import RED, CLEAR
ml_globals = {
    "True":True,
    "False":False,
    "Void":None
}
active_namespaces = [ml_globals]
def get_value(name: str):
    for namespace in active_namespaces[::-1]:
        if name in namespace.keys():
            return namespace[name]
    else:
        raise NameError(f"{RED}Undefined name {CLEAR}{name}")
def add_namespace():
    active_namespaces.append({})
def pop_namespace():
    active_namespaces.pop(-1)
def write_value(name, value):
    active_namespaces[-1][name] = value
