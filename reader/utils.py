def choices(*args):
    class const_tuple(tuple): pass
    choices = const_tuple(args)
    for t in choices:
        setattr(choices, t[1], t[0])
    return choices
