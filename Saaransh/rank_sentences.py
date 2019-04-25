import numpy as np

def get_top_list(score,sumLen):

    s=np.array(score)
    n = len(score)

    x=np.sort(s)[::-1]
    top_list=list()

    sl=int(sumLen)

    if(sl>n):
        sl=n

    for i in range(sl):
        top_list.append(x[i])

    return top_list
