def parse_log(s, indent='  ', condense=True):
    indent_num = 0
    s = s.strip()
    res = ''
    skip_space = False
    just_append = False
    for i in range(len(s)):
        c = s[i]
        if i > 0 and s[i] == ',' and s[i - 1] in [']', '}', ')']:
            continue
        if i > 0 and s[i - 1] == '=' and s[i] in ['[']:
            just_append = True
        if just_append:
            res += c
            if c is ']':
                just_append = False
                res += '\n'
                res += indent * indent_num
                skip_space = True
            continue

        if skip_space and c in [' ', '\t']:
            continue
        else:
            skip_space = False

        if c in ['[', '{', '(']:
            indent_num += 1
            res += c
            res += '\n'
            res += indent * indent_num
        elif c in ['}', ']', ')']:
            indent_num -= 1
            res += '\n'
            res += indent * indent_num
            res += c
            if i + 1 < len(s) and s[i + 1] == ',':
                res += s[i + 1]
            res += '\n'
            res += indent * indent_num
        elif not condense and c == ',':
            res += c
            res += '\n'
            res += indent * indent_num
            skip_space = True
        else:
            res += c
    print(res)


# parse_log(s, condense=True)

