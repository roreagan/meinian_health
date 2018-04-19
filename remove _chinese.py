import re


# 全角符转为半角符
def DBC2SBC(ustring):
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if not (0x0021 <= inside_code <= 0x7e):
            rstring += uchar
            continue
        rstring += chr(inside_code)
    return rstring


# 先将全角符转为半角符再提取首先看到的数字
def deal_line_107(istring):
    istring = DBC2SBC(istring)
    match = re.search(r"[0-9]+", istring)
    return istring[match.span()[0]: match.span()[1]]


def deal_line_108(istring):
    match = re.search(r"[0-9]+", istring)
    if match:
        istring = istring[match.span()[0]: match.span()[1]]
    elif istring == '缓慢':
        istring = '15'
    elif istring == '急促':
        istring = '21'
    else:
        istring = '18'
    return istring


def replace_chinese():
    table3 = open('table3.txt', 'r')
    table = open('digit_replace.txt', 'w')
    line = table3.readline()

    table.write(line)
    line = table3.readline()[: -1]
    while line:
        features = line.split("$")

        try:
            # TODO: Replace Chinese words to numbers
            features[4] = features[3].replace("心内各结构未见明显异常", "-")
            features[7] = features[7].replace("未查", "-")
            features[36] = features[36].replace("<", "-")
            features[38] = features[38].replace("阴性", "-")
            features[107] = deal_line_107(features[107])
            # 108为呼吸次数，超过20为急促，低于16次为缓慢，这里取默认值
            features[108] = deal_line_108(features[108])
            # ENDTODO
        except Exception as e:
            print(e)
            print(features)

        write_line = ""
        for i in features:
            write_line += i + "$"
        table.write(write_line[: -1] + "\n")
        line = table3.readline()[: -1]

    table3.close()
    table.close()
