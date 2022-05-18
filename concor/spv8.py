#python sp_analytics_v7.py

import AppKit
from cProfile import label
from datetime import datetime as dt
from textwrap import fill

from tkinter import *
from PIL import ImageTk, Image
import os

from lib2to3.pgen2.pgen import DFAState
from operator import countOf, index
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import nltk
from nltk.corpus import stopwords
from nltk.text import Text
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import string
from IPython.display import clear_output

import pandas as pd
import numpy as np

# error handling, pattern matching:
import traceback as tb
from glob import glob


logo = """
    ____    _____    ,     ,   ____    _____    ___
  /       /      /  /\    /  /       /      /  /  _)
 /       /      /  /  \  /  /       /      /  /  |
 \_____  \_____/  /    \/   \_____  \_____/  /   |
"""

logo_mini = """
    __   __  ,   ,  __   __  __
  /    /  / /\  / /    /  / /  )
  \__  \_/ /  \/  \__  \_/ / |

"""

eng_stops = set(stopwords.words('english'))