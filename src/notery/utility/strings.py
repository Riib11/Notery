def rreplace(s, pattern, replace):
    while pattern in s:
        s = s.replace(pattern, replace)
    return s