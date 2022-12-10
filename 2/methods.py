import random
import pandas as pd


def random_square_center(m, n, p):
    groups_nums_count = [0 for _ in range(p)]
    num = random.randint(1000, 9999)
    nums = []
    for i in range(n):
        num *= num
        str_num = str(num)
        if len(str_num) < 8:
            str_num = '0' * (8-len(str_num)) + str_num
        num = int(str_num[2:-2])
        nums.append(str(int(float(num)/10000*m)))
        groups_nums_count[get_group_idx(float(num)/10000*m, m, p)] += 1
    df = pd.DataFrame(data={'group': [i for i in range(p)], 'count': groups_nums_count})
    df.to_csv("square_center.csv", sep='\t')
    return nums


def random_linear_concurent(m, n, p):
    k, c, x = random.randint(10, m), random.randint(10, m), random.randint(0, m)
    groups_nums_count = [0 for _ in range(p)]
    groups_nums_count[get_group_idx(x, m, p)] += 1
    nums = [str(x)]
    for i in range(n-1):
        x = (k * x + c) % m
        nums.append(str(x))
        groups_nums_count[get_group_idx(x, m, p)] += 1
    df = pd.DataFrame(data={'group': [i for i in range(p)], 'count': groups_nums_count})
    df.to_csv("linear_concurent.csv", sep='\t')
    return nums


def random_system(m, n, p):
    groups_nums_count = [0 for _ in range(p)]
    nums = []
    for _ in range(n):
        x = random.randint(0, m-1)
        nums.append(str(x))
        groups_nums_count[get_group_idx(x, m, p)] += 1
    df = pd.DataFrame(data={'group': [i for i in range(p)], 'count': groups_nums_count})
    df.to_csv("system.csv", sep='\t')
    return nums


def get_group_idx(num, m, p):
    return int(num // (m / p))
#
#
# numbers = [random_linear_concurent(100, 50, 5),
#         random_square_center(100, 50, 5),
#         random_system(100, 50, 5)]