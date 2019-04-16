import numpy as np

def get_top_list(score,sumLen):

    s=np.array(score)
    n = len(score)

    # for i in range(n):
    #     # Last i elements are already in place
    #     for j in range(0, n-i-1):
    #         if score[j] < score[j+1] :
    #             score[j], score[j+1] = score[j+1], score[j]

    x=np.sort(s)[::-1]
    top_list=list()

    sl=int(sumLen)

    if(sl>n):
        sl=n

    for i in range(sl):
        top_list.append(x[i])

    return top_list
