# Imports
import time
import bs4
import selenium
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup

# Cria o web driver para o navegador Google Chrome
driver = webdriver.Chrome()

# Abre a página do Google
driver.get("https://www.google.com")

# Espera 5 segundos para a página carregar
time.sleep(5)

# Fecha o navegador
driver.quit()