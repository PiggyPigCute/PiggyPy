
def from_wiki_table(table:str) -> str:

    # delete < >
    i = 0
    while i < len(table):
        close = False
        if table[i] == "<":
            j = i
            while j < len(table) and not close:
                if table[j] == "<":
                    i = j
                elif table[j] == ">":
                    table = table[:i] + table[j+1:]
                    close = True
                j += 1
        if not close:
            i += 1

    # manage {{ }}
    i = 0
    while i+1 < len(table):
        close = 0

        if table[i] == "{" and table[i+1] == "{":

            pipes = []
            j = i
            while j+1 < len(table) and close < 1:
                j += 1
                if table[j] == "|":
                    pipes.append(j)
                elif table[j] == "{" and table[j+1] == "{":
                    close -= 1
                elif table[j] == "}" and table[j+1] == "}":
                    close += 1
        
        if close == 1:
            if len(pipes) == 0:
                table = table[:i] + table[i+2:j] + table[j+2:]
                i = (j+2) - 4
            else:
                if table[i+2:pipes[0]] == "unité":
                    text = ""
                    for k in range(len(pipes)-1):
                        text += " " + table[pipes[k]+1:pipes[k+1]]
                    if len(pipes) == 3 and table[pipes[2]+1:j] == "2":
                        text += "²"
                    else:
                        text += " " + table[pipes[2]+1:j]
                    table = table[:i] + text[1:] + table[j+2:]
                    i += len(text)-1
                else: # unknown type of {{ }} (so i delete)
                    table = table[:i] + table[j+2:]
        else:
            i += 1
    
    # manage [[ ]]
    i = 0
    while i+1 < len(table):
        closed = False

        if table[i] == "[" and table[i+1] == "[":

            pipe = i+1
            j = i
            while j+1 < len(table) and not closed:
                j += 1
                if table[j] == "|":
                    pipe = j
                elif table[j] == "]" and table[j+1] == "]":
                    closed = True
        
        if closed:
            table = table[:i] + table[pipe+1:j] + table[j+2:]
            i += j - 1 - pipe
        else:
            i += 1

    # delete \n
    i = 0
    while i < len(table):
        if table[i] == "\n":
            table = table[:i] + table[i+1:]
        else:
            i += 1

    # turn |-| into \n
    i = 0
    first_raw = 0
    while i+2 < len(table):
        if table[i:i+3] == "|-|":
            table = table[:i] + "\n" + table[i+3:]
            if first_raw == 0:
                first_raw = i
        i += 1
    
    # Manage first raw
    table = "|".join([column.split("|")[-1] for column in table[:first_raw].split("!")[1:]]) + table[first_raw:]

    # turn || into |
    i = 0
    while i+1 < len(table):
        if table[i:i+2] == "||":
            table = table[:i] + "|" + table[i+2:]
        i += 1

    # # manage rowspan
    # i = 0
    # pipe = 0
    # while i+11 < len(table):
    #     if table[i] == "|":
    #         pipe += 1
    #     if table[i] == "\n":
    #         pipe = 0
    #     if table[i:i+9] == 'rawspan="':
    #         j = i+1
    #         while j < len(table) and table[j] in "0123456789":
    #             j += 1
    #         x = int(table[i+9:j])
    #         while j < len(table) and table[j] != "|":
    #             j += 1
    #         if j-i > 15:
    #             print("⚠️ piggypy.csv, rawspan system deleted this: " + table[i::j])
    #         lines = table[j:].split("\n")
    #         for k in range(1,x):
    #             λ = lines[k].split("|")
    
    return table

def to_header_table(csv:str, delimiter:str) -> tuple[list[str], list[list[str]]]:
    lines = [line.split(delimiter) for line in csv.split('\n')]
    return lines[0], lines[1:]

def from_table(table:list[list[str]], delimiter:str) -> str:
    return '\n'.join([delimiter.join(line) for line in table])

def from_header_table(header:list[str], table:list[list[str]], delimiter:str) -> str:
    return from_table([header] + table, delimiter)

def append(csv_1:str, csv_2:str, delimiter_1:str, delimiter_2:str, join_1:str, join_2:str, append_columns:list[str]) -> str:
    header_1, table_1 = to_header_table(csv_1, delimiter_1)
    header_2, table_2 = to_header_table(csv_2, delimiter_2)

    i_join_1 = header_1.index(join_1)
    i_join_2 = header_2.index(join_2)
    i_appends = [header_2.index(column) for column in append_columns]

    len_header_1 = len(header_1)

    for i in i_appends:
        header_1.append(header_2[i])
    
    for x in table_2:
        x_join = x[i_join_2]
        y_find = False
        for y in table_1:
            if len(y)>i_join_1 and y[i_join_1] == x_join:
                while len(y) < len_header_1:
                    y.append("")
                for i in i_appends:
                    y.append(x[i])
                    y_find = True
        if not y_find:
            print("⚠️ Aucun terme correspondant à " + x_join)

    return from_header_table(header_1, table_1, delimiter_1)
        
def to_dict_list(csv:str, delimiter:str) -> list[dict]:
    header,table = to_header_table(csv, delimiter)
    result = []
    for line in table:
        result.append({})
        for i in range(len(line)):
            result[-1][header[i]] = line[i]
    return result

def from_dict_list(dict_list:list[dict], header, delimiter):
    table = [[line[column] for column in header] for line in dict_list]
    return from_header_table(header, table, delimiter)

def shuffle_columns(csv, delimiter, header):
    return from_dict_list(to_dict_list(csv, delimiter), header, delimiter)

def sort(csv:str, delimiter:str, key, add_rank=False, rank_name="rank", add_key_value=False, key_value_name="key_value", reverse:bool=False) -> str:
    header,_ = to_header_table(csv, delimiter)
    dict_list = to_dict_list(csv, delimiter)
    if isinstance(key,str):
        key = lambda x: x[key]
    dict_list.sort(key=key, reverse=reverse)
    if add_rank:
        for i in range(len(dict_list)):
            dict_list[i][rank_name] = str(i)
        header.append(rank_name)
    if add_key_value:
        for dico in dict_list:
            dico[key_value_name] = str(key(dico))
        header.append(key_value_name)
    return from_dict_list(dict_list, header, delimiter)

