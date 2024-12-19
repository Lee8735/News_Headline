from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeSrvice
from selenium.webdriver.chrome.options import Options as ChrimeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

