import requests


class Client:
    """
    The Client class for the RegBL API
    """

    def __init__(self, url):
        """
        Constructor of the RegBL Client class

        :param url: str of the base URL of the RegBL API
        """
        self.url = url

    def get(self, egid, lang="en"):
        """
        Get the entry with the given EGID

        :param egid: str of the EGID to get
        :param lang: str of the language to get the entry in
        :return: Response object of the entry
        """
        return requests.get(f"{self.url}/{egid}?lang={lang}")
