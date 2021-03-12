
import re

async def opredel_skreen(g, text):
    if "vk.com/" in str(text):
        r = re.findall(r'/\w+.\w+', g)
        t = r[-1]
        t = t[1:]
        return t

    elif "[id" in str(text) or "[club" in str(text):
        l = g.find('|')
        l2 = g.find('id')
        k = g[:l]
        k2 = k[l2 +2:]
        k = k[1:]
        k = k.replace("club", "")
        k = k.replace("id", "")
        if "[club" in str(text):
            k = "- " +str(k)
        return k
    return g



async def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))
