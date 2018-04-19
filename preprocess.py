import re

def readDatas():
    datas = {}
    items = []
    print('Read part1.............')
    with open('../part1.txt', 'r', encoding='utf-8') as data1:
        line = data1.readline()
        while line:
            try:
                line = data1.readline()
                if len(line) == 0:
                    continue
                item = line.split("$")
                if not datas.get(item[1]):
                    datas[item[1]] = 1
                    items.append(item[1])
            except Exception as e:
                print(e)
                print(len(datas))
                print(len(items))
        data1.close()

    print('Read part2.............')
    with open('../part2.txt', 'r', encoding='utf-8') as data1:
        line = data1.readline()
        while line:
            try:
                line = data1.readline()
                if len(line) == 0:
                    continue
                item = line.split("$")
                if not datas.get(item[1]):
                    datas[item[1]] = 1
                    items.append(item[1])
            except Exception as e:
                print(e)
                print(len(datas))
                print(len(items))
        data1.close()

    print('Count.............')
    output = open('item.txt', 'w')
    line = ""
    items.sort()
    for i in items:
        line += i + "$"
    output.write(line)
    output.close()


def combine_files():
    data1 = open('../part1.txt', 'r', encoding='utf-8')
    data2 = open('../part2.txt', 'r', encoding='utf-8')

    datas = []
    line = data1.readline()
    while line:
        try:
            line = data1.readline()
            if len(line) == 0:
                continue
            datas.append(line)
        except Exception as e:
            print(e)
    data1.close()

    line = data2.readline()
    while line:
        try:
            line = data2.readline()
            if len(line) == 0:
                continue
            datas.append(line)
        except Exception as e:
            print(e)
    data2.close()

    datas.sort()
    output = open('combine.txt', 'w')
    for i in datas:
        output.write(i)
    output.close()


def generate_csv():
    items = {}
    print("Get items..........")
    combine = open('table.txt', 'w', encoding='utf-8')
    with open('item_new', 'r') as item_file:
        line = item_file.readline()
        lines = line.split("$")
        for i in range(len(lines)):
            items[lines[i]] = i
    user = ""
    user_infos = ['-' for _ in range(len(items))]
    print("Write csv..........")
    combine.write("user$" + line + '\n')
    with open('combine.txt', 'r') as file:
        count = 0
        while line:
            try:
                line = file.readline()[:-1]
                infos = line.split("$")
                if len(line) == 0 or infos[0] != user:
                    if user != "":
                        item_line = ""
                        for i in range(len(items)):
                            item_line += user_infos[i]
                            item_line += "$"
                        combine.write(user + "$" + item_line[: -1] + "\n")
                    user = infos[0]
                    user_infos = ['-' for _ in range(len(items))]

                    # count += 1
                    # if count > 20:
                    #     break
                user_infos[items[infos[1]]] = infos[2].replace(" ", "").replace("\t", "") \
                    if len(infos[2].replace(" ", "").replace("\t", "")) > 0 else "-"

            except Exception as e:
                print(e)

    combine.close()


def extract_sample():
    train = open("../train.csv", 'r')
    line = train.readline()
    users = []
    while line:
        try:
            line = train.readline()
            if len(line) > 0:
                users.append(line.split(",")[0])
        except Exception as e:
            print(e)
    train.close()

    users.sort()
    table = open('table.txt', 'r', encoding='utf-8')
    table2 = open('table2.txt', 'w', encoding='utf-8')

    line = table.readline()
    table2.write(line)
    count = 0
    while line:
        try:
            line = table.readline()
            if len(line) == 0:
                break
            user = line[0: line.index("$")]
            if user == users[count]:
                table2.write(line)
                count += 1
                if count > len(users):
                    break
        except Exception as e:
            print(e)
            print(count)
    table.close()
    table2.close()


def count_column():
    threshold = 1
    data = open('table2.txt', 'r', encoding='utf-8')
    line = data.readline()
    features_map = [{} for _ in range(2795)]
    while line:
        try:
            line = data.readline()[: -1]
            if len(line) == 0:
                continue
            infos = line.split("$")
            for i in range(len(infos)):
                if i != 0 and infos[i] != '-':
                    if not features_map[i-1].get(infos[i]):
                        features_map[i-1][infos[i]] = 1
        except Exception as e:
            print("[line:" + line + "]")
            print(e)
    data.close()

    colunms = []
    feature_file = open('features.txt', 'w')
    for i in range(2795):
        line = ""
        if len(features_map[i]) <= threshold:
            colunms.append(i)
            continue
        for feature in features_map[i]:
            line += feature + "$"
        feature_file.write(line + "\n")
    feature_file.close()

    del_columns = open('del_columns.txt', 'w')
    del_line = ""
    for column in colunms:
        del_line += str(column) + '$'
    del_columns.write(del_line[: -1])
    del_columns.close()


def delete_column():
    del_columns = open('del_columns.txt', 'r')
    columns = del_columns.readline().split("$")
    del_columns.close()
    data = open('table2.txt', 'r', encoding='utf-8')
    table3 = open('table3.txt', 'w', encoding='utf-8')

    line = data.readline()[: -1]
    features = line.split("$")
    feature_line = ""
    count = 0
    for i in range(len(features)):
        if count >= len(columns) or str(i - 1) != columns[count]:
            feature_line += features[i] + "$"
        else:
            count += 1
    table3.write(feature_line[: -1] + '\n')

    while line:
        try:
            line = data.readline()[: -1]
            infos = line.split("$")

            line_data = ""
            count = 0
            for i in range(len(infos)):
                if count >= len(columns) or str(i - 1) != columns[count]:
                    line_data += infos[i]
                    line_data += "$"
                else:
                    count += 1
            table3.write(line_data[: -1] + '\n')
        except Exception as e:
            print(e)
    data.close()
    table3.close()


def delete_column_name():
    table2 = open('table2.txt', 'r', encoding='utf-8')
    del_features = open('del_columns.txt', 'r')
    dels = del_features.readline().split("$")
    origin_features = table2.readline()[: -1].split("$")[1:]

    table2.close()
    del_features.close()

    line = "user"
    count = 0
    for i in range(len(origin_features)):
        if str(i) != dels[count]:
            line += " " + origin_features[i]
        else:
            count += 1


def recorrect_item():
    item_file = open('item.txt', 'r')
    new_item_file = open('item_new', 'w')

    items = item_file.readline()[: -1]
    line = ""
    for i in items.split(" "):
        line += i + "$"
    new_item_file.write(line[: -1])
    item_file.close()
    new_item_file.close()


def check_chinese():
    features_file = open('features.txt', 'r')
    chinese_items = []
    count = 0
    line = features_file.readline()
    while line:
        match = re.match(r"([0-9]+(.[0-9]+)?\$)+", line)
        if not match or match.span()[0] != 0:  # or match.span()[1] != len(line):
            chinese_items.append(count)
        count += 1
        line = features_file.readline()
    features_file.close()

    table = open('table3.txt', 'r', encoding='utf-8')
    table4 = open('table4.txt', 'w', encoding='utf-8')

    line = table.readline()[: -1]
    while line:
        write_line = ""
        features = line.split("$")
        count = 0
        for i in range(len(features)):
            if count >= len(chinese_items) or i - 1 != chinese_items[count]:
                write_line += features[i] + "$"
            else:
                count += 1

        for i in chinese_items:
            write_line += features[i + 1] + "$"

        table4.write(write_line[: -1] + "\n")
        line = table.readline()[: -1]

    table.close()
    table4.close()


def chinese_redundancy():
    file = open('features.txt', 'r')
    re_file = open('redundancy', 'w')
    line = file.readline()[: -2]
    count = 0
    while line:
        values = line.split("$")
        buf = []
        for i in values:
            match = re.match(r"([0-9]+(.[0-9]+)?)", i)
            if not match or match.span()[1] - match.span()[0] != len(i):
                buf.append(i)
        if 0 < len(buf) < len(values):
            line = ""
            for i in buf:
                line += i + "$"
            re_file.write(str(count) + "   " + line[: -1] + "\n")
        line = file.readline()[: -2]
        count += 1
    file.close()
    re_file.close()


chinese_redundancy()


