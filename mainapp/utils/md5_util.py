import hashlib

"""
对文本进行md5加密
"""
def md5(text):
    hl = hashlib.md5()
    hl.update(text.encode(encoding='utf8'))
    md5 = hl.hexdigest()
    return md5