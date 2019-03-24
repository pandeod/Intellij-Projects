def get_top_list(total_score):
    n = len(total_score)

    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            if total_score[j] < total_score[j+1] :
                total_score[j], total_score[j+1] = total_score[j+1], total_score[j]

    top_list=list()
    i=0
    while(i<3*n/5):
        top_list.append(total_score[i])
        i+=1

    return top_list
