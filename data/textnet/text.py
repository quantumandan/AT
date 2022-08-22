"""
Flow algebra applied to text network analysis:

Algorithmic topology posits that effective computation is dual to the flow of information. If
cognition is represented by the flow of concepts, written natural language is an ontological
projection of a sequence connected ideas.

Every sentence is represented as a path across a directed graph of words in a vocabulary. In
this way, a paragraph is a collection of paths -- a flow. A document is a collection of flows and a
narrative is a path through a collection of flows.
"""

from AT.common.path import Path
from AT.common.flow import Flow
from AT.common.epsilon import Epsilon
import textnets as tn
from typing import *

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.models.dom import ObjectDocumentModel

tn.params["seed"] = 42

LANGUAGE = "english"

def download_links(links: List) -> List[str]:
    """
    Downloads the html from a list of links and converts them to text
    """

