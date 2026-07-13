'''
Helper module
Generic merge sort
'''
def merge_sort(arr,attr:str):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid],attr)
    right_half = merge_sort(arr[mid:],attr)

    return merge(left_half, right_half,attr)


def merge(left, right,attr:str):
    sorted_arr = []
    i = j = 0

    while i < len(left) and j < len(right):
        if getattr(left[i],attr) < getattr(right[j],attr):
            sorted_arr.append(left[i])
            i += 1
        else:
            sorted_arr.append(right[j])
            j += 1
            
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])

    return sorted_arr

'''
#Mergesort usage example
from apps.core import Node

n=[]
for i in range(0,10): # spawn 10 nodes
    k=Node.Node()
    k.index=i
    n.append(k)

sorted_n = merge_sort(n,"index") # sort the list index-wise

for i in range(0,10):
    print(sorted_n[i].out(fancify=True)) # print them all
'''