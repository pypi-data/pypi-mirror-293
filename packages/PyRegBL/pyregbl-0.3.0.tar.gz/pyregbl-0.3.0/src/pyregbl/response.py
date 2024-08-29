from .mapping_table import mapping_table
from .utils import replace_codes_with_strings


class Response:

    def __init__(self, response, mapping_tables=mapping_table):
        """
        Constructor of the RegBL Response class

        :param response: The response object from the requests library
        :param mapping_tables: The mapping tables to use for replacing codes with strings
        """
        self.response = response
        self.mapping_tables = mapping_tables

    def json(self):
        """
        Get the JSON of the response

        :return: Dict of the JSON in the response
        """
        return self.response.json()

    def attributes(self, raw=False):
        """
        Get the attributes of the response

        :param raw: Bool to return the raw data or the data with codes replaced with strings
        :return: Dict of the attributes in the response
        """
        data = self.response.json()["feature"]["attributes"]
        res = data if raw else replace_codes_with_strings(data, self.mapping_tables)
        return res
