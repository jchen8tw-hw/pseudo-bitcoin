import hashlib

def sum256(*strings):
    m = hashlib.sha256()
    for string in strings:
        m.update(string.encode('utf-8'))
    return m.hexdigest()

def encode(string,code='utf-8'):
    return string.encode(code)

def decode(string,code='utf-8'):
    return string.decode(code)

if __name__ =='__main__':
    #print(sum256(b'123456',b'54321'))
    pass