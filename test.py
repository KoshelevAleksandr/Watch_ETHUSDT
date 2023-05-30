def func(a, b):
    dict_a = dict()
    for i in range(len(a)):
        dict_a[len(a)-i-1] = int(a[i])
    dict_b = dict()
    for i in range(len(b)):
        dict_b[len(b) - i - 1] = int(b[i])
    dict_c = dict()
    max_step = max(max(dict_a.keys()), max(dict_b.keys()))
    for i in range(max_step+1):
        if i in dict_a:
            if i in dict_b:
                dict_c[i] = dict_a[i] + dict_b[i]
            else:
                dict_c[i] = dict_a[i]
        elif i in dict_b:
            dict_c[i] = dict_b[i]
    c = 0
    for i, j in dict_c.items():
        c += j*(10**i)
    return c


a = '3564686784'
b = '123456789'

if __name__ == '__main__':
    print(func(a, b))
    print(int(a) + int(b))