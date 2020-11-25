
import re

async def opredel_screen(text):
    if "vk.com/" in text:
        r = re.findall(r'/\w+.\w+', text)
        t = r[-1]
        t = t[1:]
        return t

    elif "[id" in text or "[club" in text:
        l = text.find('|')
        l2 = text.find('id')
        k = text[:l]
        k2 = k[l2+2:]
        k = k[1:]
        k = k.replace("club", "")
        k = k.replace("id", "")
        if "[club" in text:
            k = f"-{k}"
    return k
