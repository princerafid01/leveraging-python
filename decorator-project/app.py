def check(func):
    def inner(*args):
        if(args[1] == 0):
            return f'zero can not passed in second argument'
        return func(*args)
    return inner


@check
def div(a,b):
    return a/b


print(div(4,0))
