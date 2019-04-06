def get_top_list(score):
    n = len(score)

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            if score[j] < score[j+1] :
                score[j], score[j+1] = score[j+1], score[j]

    top_list=list()
    i=0
    while(i<3*n/5):
        top_list.append(score[i])
        i+=1

    return top_list
