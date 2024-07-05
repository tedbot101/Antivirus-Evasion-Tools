from itertools import zip_longest
def fun(n, i, value=None):
    args = [iter(i)] * n
    return zip_longest(fillvalue=value, *args)
my_string = "California is a major hub for technology companies."
n = 8
op_str = [''.join(l) for l in fun(n, my_string, '')]
op = []
for a in op_str:
    op.append(a)
print(op)