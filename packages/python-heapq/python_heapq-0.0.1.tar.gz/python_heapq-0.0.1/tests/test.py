import random
import time
import heapq
import copy
from python_heapq import priorityq


GREEN = '\033[92m'
RED = '\033[31m'
END = '\033[0m'

def my_test(lst:list):
    print("length",len(lst),lst[0:5],"...",lst[-6:-1], end = "")
    pq=priorityq([])
    for i in lst:
        pq.push(i)
    # print(pq.data)
    push_test(pq.data)
    pre_poped = -100
    iter100 = (i for i in sorted(lst))
    while pq.data:
        j = pq.pop()
        assert(j == next(iter100))
        push_test(pq.data)
        assert(j >= pre_poped)
        pre_poped = j
    print(GREEN + " ----> OK" + END)

def py_test(lst:list):
    print("length",len(lst),lst[0:5],"...",lst[-6:-1], end = "")
    pq=[]
    for i in lst:
        heapq.heappush(pq,i)
    # print(pq.data)
    push_test(pq)
    pre_poped = -100
    iter100 = (i for i in sorted(lst))
    while pq:
        j = heapq.heappop(pq)
        assert(j == next(iter100))
        push_test(pq)
        assert(j >= pre_poped)
        pre_poped = j
    print(GREEN + " ----> OK" + END)

def push_test(lst:list):
    current_index = 0
    last_index = len(lst) - 1
    while True:
        # 長さを超えたら終わり
        if current_index > last_index:
            break
    
        child_index = current_index*2 + 1
        if child_index > last_index:
            current_index += 1
            continue
    
        if not (lst[current_index] <= lst[child_index]):
            print(RED + "heap structure is wrong" + END)
        
        child_index += 1
        if child_index > last_index:
            current_index += 1
            continue
    
        if not (lst[current_index] <= lst[child_index]):
            print(RED + "heap structure is wrong" + END)
        current_index += 1
    
if __name__ == "__main__":
    lst_lst:list[list[int]] = []
    for i in range(10):
        lst = list(range(10001))
        random.shuffle(lst)
        lst_lst.append(lst)
    lst_lst2 = copy.deepcopy(lst_lst)

    now = time.perf_counter()
    for i in lst_lst:
        my_test(i)
    print(GREEN + f"{time.perf_counter() - now} msec" + END)
    print(GREEN + "my random test (length 100) ---> Ok" + END)
    now = time.perf_counter()

    for i in lst_lst2:
        py_test(i)
    print(GREEN + f"{time.perf_counter() - now} msec" + END)
    print(GREEN + "py random test (length 100) ---> Ok" + END)