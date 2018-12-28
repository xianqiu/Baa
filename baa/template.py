from pathlib import Path


def fill_template(value_dict):
    path = Path(__file__).parent / 'mail_template'
    content = ''
    with open(path, 'r', encoding='utf8') as f:
        for line in f.readlines():
            content += fill_braces(line, value_dict)
    return content


def fill_braces(line, value_dict):
    if line.find('{') == -1:
        return line
    left = line.find('{')
    right = line.find('}')
    key = line[left+1: right]
    fill_str = str(value_dict[key]) if key in value_dict.keys() else ''
    return line[0: left] + fill_str + fill_braces(line[right + 1:], value_dict)
