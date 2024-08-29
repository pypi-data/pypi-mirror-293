from .client import Client
from .mapping_table import mapping_table
from .attributes import attributes
from .response import Response
from .utils import replace_codes_with_strings

base_url = "https://api3.geo.admin.ch/rest/services/ech/MapServer/ch.bfs.gebaeude_wohnungs_register/"
client = Client(base_url)


def get(egid, lang="en", raw=False):
    """
    Get the entry with the given EGID

    :param egid: str of the EGID to get
    :param lang: language to get the entry in
    :return: dict of the entry
    """
    response = client.get(f"{egid}_0", lang=lang)
    res = response.json() if raw else Response(response).attributes()
    return res


def get_attributes():
    """
    Get the attributes of the response

    :return: dict of the attributes
    """
    return attributes


def get_mapping_table():
    """
    Get the mapping table for replacing codes with strings

    :return: dict of the mapping table
    """
    return mapping_table

def map(data, mapping_table=mapping_table):
    """
    Replace codes with strings in the data in the attributes of the data

    :param data: dict of the data
    :param mapping_table: dict of the mapping table
    :return: dict of the data with codes replaced with strings
    """
    return replace_codes_with_strings(data, mapping_table)


