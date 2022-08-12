"""
Contains basic functionality for retrieving data from a URI.
"""


class Corpus:
    """
    A corpus is a collection of documents.
    """

    def __init__(self, uri):
        self.uri = uri
        self.documents = []

    def __iter__(self):
        return iter(self.documents)

    def download(self):
        """
        Download the corpus from the URI.
        """
        raise NotImplementedError

    def tag(self):
        """
        Tag the corpus.
        """
        raise NotImplementedError
