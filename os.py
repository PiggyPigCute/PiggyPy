
def read(path, encoding="utf-8") -> str:
    file = open(path, 'r', encoding=encoding)
    φ = file.read()
    file.close()
    return φ

def write(path, content, encoding="utf-8"):
    file = open(path, 'w', encoding=encoding)
    φ = file.write(content)
    file.close()

