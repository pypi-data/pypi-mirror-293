def replace_codes_with_strings(data, mapping_tables):
    """
    Replace codes with strings in the data
    :param data:
    :param mapping_tables:
    :return:
    """
    for key, value in data.items():
        if key.lower() in mapping_tables:
            mapping_table = mapping_tables[key.lower()]
            if isinstance(value, list):
                data[key] = [mapping_table.get(item, item) for item in value]
            else:
                data[key] = mapping_table.get(value, value)
    return data
