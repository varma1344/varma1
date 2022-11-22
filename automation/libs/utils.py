def parse_multiline_input(data: str):
    """
    Parse multiline key and value pair input into dictionary.
    :param data: Data in string format
    :return: Dict of parsed input
    """
    out = {}
    for info in data.split("\n"):
        info = info.trim()
        if len(info) == 0:
            continue
        key,val = info.split("=")
        out[key.trim()] = val.trim()

    return out

def parse_str_table(table_with_headers):
    """Parse table and create dictionary of rows"""
    list_table_rows = table_with_headers.split("\n")
    headers = str(list_table_rows[0]).strip("|").split("|")
    headers = [h.strip() for h in headers]
    dict_table = []
    for i in range(1, list_table_rows.__len__()):
        list_temp = list_table_rows[i].strip("|").split("|")
        rowvals = [cell.strip() for cell in list_temp]
        row = {}
        for idx,hdr in enumerate(headers):
            row[hdr] = rowvals[idx]
        dict_table.append(row)
    return dict_table