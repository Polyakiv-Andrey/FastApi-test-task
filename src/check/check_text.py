def adjust_string(s, max_line_length):
    if len(s) < max_line_length:
        parts = s.split()
        return parts[0] + " " * (max_line_length - len(s)) + parts[1]

    return s


def center_text(s, max_line_length):
    if len(s) < max_line_length:
        spaces = (max_line_length - len(s)) // 2
        s = " " * spaces + s + " " * spaces
        s = s.strip("\n")
        s = "\n".join(s[i:i + max_line_length] for i in range(0, len(s), max_line_length))
    elif len(s) == max_line_length:
        pass
    else:
        s = "\n".join(s[i:i + max_line_length] for i in range(0, len(s), max_line_length))
    return s