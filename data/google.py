# import requests
from googleapiclient.discovery import build
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.models.dom import ObjectDocumentModel
import os

# do a google search
G_CUSTOM_SEARCH_API_KEY = os.environ["G_CUSTOM_SEARCH_API_KEY"]
G_CSE_ID = os.environ["G_CSE_ID"]


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res["items"]


LANGUAGE = "english"
SENTENCES_COUNT = 10
QUERY = "Automatic summarization"


def concatenate_results(items):
    links = (
        item["link"] for item in google_search(QUERY, G_CUSTOM_SEARCH_API_KEY, G_CSE_ID)
    )
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    for url in links:
        parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
        yield parser.document


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Automatic_summarization"
    results = concatenate_results(url)
