def map(func, obj):
    return _map_dispatch[obj.__class__](func, obj)

_map_dispatch = {
    dict: lambda f, d: {k: func(v) for k, v in d.items()}
    list: lambda f, l: [f(_) for _ in l]
    tuple: lambda f, t: tuple([f(_) for _ in t])
}