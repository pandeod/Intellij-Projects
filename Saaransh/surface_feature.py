def get_surface_score(docs):
    n=len(docs)
    sent_len=list()

    position_score=list()

    for i in range(n):
        position_score.append(1/(i+1))

    for i in range(n):
        sent_len.append(len(docs[i].split(' ')))

    total_len=0
    for x in range(n):
        total_len+=sent_len[x]

    avg_len=total_len/n

    length_score=list()

    i=0
    while(i<n):
        if(sent_len[i]<=avg_len):
            length_score.append(0)
        else:
            length_score.append((sent_len[i]-avg_len)/avg_len)
        i+=1

    surface_score=list()
    for i in range(n):
        surface_score.append(position_score[i]+length_score[i])

    return surface_score