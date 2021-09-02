import collections
import sys
import itertools
import numpy as np


def minion_game(string):
    # BANANA
    stuart = {}  # consonants
    kevin = {}
    vowels = ["A", "E", "I", "O", "U"]
    for index, c in enumerate(string):
        if c not in vowels:
            ch = c
            while index < len(string):
                if ch not in stuart:
                    stuart[ch] = 1
                else:
                    stuart[ch] += 1

                index += 1
                if index < len(string):
                    ch = ch + string[index]

        else:
            ch = c
            while index < len(string):
                if ch not in kevin:
                    kevin[ch] = 1
                else:
                    kevin[ch] += 1

                index += 1
                if index < len(string):
                    ch = ch + string[index]

    st_r = sum(stuart.values())
    kv_r = sum(kevin.values())

    if st_r > kv_r:
        return print("Stuart", st_r)
    elif st_r == kv_r:
        return print("Draw")
    else:
        return print("Kevin", kv_r)


def main(s):
    vowels = 'AEIOU'
    kevsc = 0
    stusc = 0
    for i in range(len(s)):
        if s[i] in vowels:
            kevsc += (len(s) - i)
        else:
            stusc += (len(s) - i)

    if kevsc > stusc:
        print("Kevin", kevsc)
    elif kevsc < stusc:
        print("Stuart", stusc)
    else:
        print("Draw")

# https://www.hackerrank.com/challenges/python-sort-sort/problem
def sort_athletes(arr, k):
    nm = input().split()
    n = int(nm[0])
    m = int(nm[1])
    arr = []
    for index in range(n):
        lst = list(map(int, input().rstrip().split()))
        lst.append(index)
        arr.append(lst)
    k = int(input())
    a = sorted(arr, key=lambda tup: (tup[k], tup[-1]))
    for at in a:
        print(*at[:-1])


def compress_String(string):
    i = 0
    c = 1
    r = []
    while i < len(string) - 1:
        if string[i] == string[i+1]:
            c += 1
            i += 1
        else:
            r.append((c, int(string[i])))
            i += 1
            c = 1
            continue
    r.append((c, int(string[i])))  # append last letter analized
    print(*r)
    # alternatively using intertools groupby
    # [(k, list(g)) for k, g in itertools.groupby(string)]


def merge_the_tools(string, k):
    # output = [string[i:i + k] for i in range(0, len(string), k)]
    # r = []
    # for ti in output:
    #     ui = []
    #     for i in ti:
    #         if i not in ui:
    #             ui.append(i)
    #         else:
    #             continue
    #     r.append("".join(ui))
    #
    # print(*r, sep="\n")
    # Alternatively
    # S, N = input(), int(input())
    for part in zip(*[iter(s)] * k):
        d = dict()
        print(''.join([d.setdefault(c, c) for c in part if c not in d]))


def maximize_it(k, m):
    pass


def word_order(arr):
    d = {}
    for i in arr:
        if i not in d:
            d[i] = 1
        else:
            d[i] += 1
    print(len(d))
    print(*d.values())
    # using ordered dict
    # from collections import Counter, OrderedDict
    # class OrderedCounter(Counter, OrderedDict):
    #     pass
    #
    # d = OrderedCounter(input() for _ in range(int(input())))
    # print(len(d))
    # print(*d.values())

def isValidSubsequence(array, sequence):
    # Write your code here.
    i = 0
    for s in array:
        if s == sequence[i]:
            i += 1  # check if next sequence item is in array
            if i == len(sequence):  # reach end of sequence
                print("sequence is in array!")
                return True
    return False


if __name__ == '__main__':
    array = [5, 1, 22, 25, 6, -1, 8]
    sequence = [1, 6, -1, 10]
    isValidSubsequence(array, sequence)
    # data = [int(i) for i in input().split(" ")]
    # k = data[0]
    # m = data[1]
    # # # minion_game(s)
    # # # main("BANANA")
    # arr = []
    # for n in range(int(k)):
    #     s = list(map(int, input().split()))
    #     arr.append(max(s))

    # print(sum([x*x for x in arr]) % m)
    #     # lst = list(map(int, input().rstrip().split()))
    #     s = input().split()
    #     arr.append(*s)
    # word_order(arr)
    # merge_the_tools("AABCAAADA", 3)

