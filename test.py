lst = ['\n', 'CF21, B738, KBOS-KORD\n', 'CF5, B732, KIAD-KLGA\n', 'CF24, B732, KLGA-KPIT\n', 'CF19, A300F, KPHX-KLAX\n', 'CF19, B732, KIAD-KIND']

tst = ["YES O NO", "YES, O, NO", "YES O NO"]


def delstr2(lst):
    return [
        {' '.join(elem.split()[1:]).rstrip(), ' '.join(elem.split()[2:]).rstrip(-1)}
        for elem in lst
    ]




print(lst)
print("----------------------------------------------------------------")
print(delstr2(lst))
print("----------------------------------------------------------------")