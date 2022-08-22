"""
This module connects to the blockchain and provides a simple interface to the data.
"""
import json
import logging
import os
import time
from datetime import datetime
from typing import *
import requests


class Blockchain:
    def __init__(self, url, port, protocol_version="BTC") -> None:
        self.logger = logging.getLogger(__name__)
        self.protocol_version = protocol_version
        self.port = port
        self.url = url


def connect_to_blockchain(address: str, port: int) -> str:
    """
    Connects to the blockchain and returns the data.
    """
    r = requests.get(f"http://{address}:{port}/chain")
