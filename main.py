# find maths expressions in text
# and calculate them to fixed variables
import re


def calculate(text, data):
    matches = re.findall(r"([abc])([+-]?)=([abc]?)([+-]?\d+)?", text)
    for v1, s, v2, n in matches:
        if s == "":
            data[v1] = data.get(v2, 0) + int(n or 0)
        else:
            bad_expr = s + str(data.get(v2, 0) + int(n or 0))
            if bad_expr[0] == '+' and bad_expr[1] == '-':
                bad_expr = '-' + bad_expr[2:]
            if bad_expr[0] == '-' and bad_expr[1] == '+':
                bad_expr = '-' + bad_expr[2:]
            if bad_expr[0] == '+' and bad_expr[1] == '+':
                bad_expr = '+' + bad_expr[2:]
            if bad_expr[0] == '-' and bad_expr[1] == '-':
                bad_expr = '+' + bad_expr[2:]
            data[v1] = data[v1] + int(bad_expr or 0)

    return data
