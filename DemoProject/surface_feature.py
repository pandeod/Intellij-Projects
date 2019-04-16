import numpy as np

def get_surface_score(docs):
    n=len(docs)

    p=list()
    for i in range(n):
        p.append(1/(i+1))

    position_score=np.array(p)
    # psMax=position_score.max()
    # position_score=(100*position_score)/psMax

    s=list()
    for i in range(n):
        s.append(len(docs[i].split(' ')))

    sent_len=np.array(s)

    total_len=sent_len.sum()
    avg_len=total_len/n

    ls=list()

    for i in range(n):
        if(sent_len[i]<=avg_len):
            ls.append(0)
        else:
            ls.append((sent_len[i]-avg_len)/avg_len)

    length_score=np.array(ls)
    # lsMax=length_score.max()
    # length_score=(100*length_score)/lsMax

    surface_score=position_score+length_score
    maxSurface=surface_score.max()
    surface_score=(100*surface_score)/maxSurface

    return surface_score