OFFSET = -59

def colorGen(tag: str) -> str:
    h = int(''.join(str(ord(c)) for c in tag))
    return f"hsl({(h-OFFSET)%360}, 75%, 70%)"
