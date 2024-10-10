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


# Conecta na página e extrai o código fonte
driver.get("https://www.imdb.com/search/title/?groups=top_100&count=100&sort=user_rating,desc")

# Formata o código fonte com o parser html
soup = BeautifulSoup(driver.page_source, 'html.parser')

print(soup.prettify())    

# Fecha o navegador
driver.quit()

#Extraindo os Dados Relevantes da Página Web

# Listas de controle para receber os dados
title = []
years = []
duration = []
ratings = []
vote_count = []
description = []

# Extrai a tag com o título do filme
titulo_filme = soup.find_all('a', attrs = {'class':'ipc-title-link-wrapper'})

# Extrai o texto e armazena os dados na lista
for titulo in titulo_filme:
    nome = titulo.h3.text
    title.append(nome)

# Visualiza os primeiros registros
title[0:5]    

# Tamanho da lista
len(title)

# Extraindo a tag div com outros detalhes do filme
outros_detalhes = soup.findAll('div', attrs = {'class':'sc-b189961a-7 btCcOY dli-title-metadata'})

# Loop para percorrer os detalhes de cada filme
for detalhe in outros_detalhes:
    
    # Encontra o elemento <span> que contém o ano do filme
    year_span = detalhe.span
    
    # Encontra o próximo elemento <span> que contém a duração do filme
    duration_span = year_span.find_next_sibling('span')
    
    # Adiciona o ano do filme à lista de anos
    years.append(year_span.text)
    
    # Adiciona a duração do filme à lista de durações
    duration.append(duration_span.text)

# Visualiza os primeiros registros
years[0:5]

# Tamanho da lista
len(years)

# Visualiza os primeiros registros
duration[0:5]

# Tamanho da lista
len(duration)

# Extraindo os dados da tag span com as avaliações dos filmes
avaliacoes = soup.findAll('span', attrs = {'class':'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'})

# List comprehension para extrair o texto
avaliacoes = [aval.text for aval in avaliacoes]

# Loop para percorrer as avaliações de cada filme
for aval in avaliacoes:
    
    # Divide a string da avaliação em duas partes: nota e número de votos
    rating, vote = aval.split('\xa0')
    
    # Adiciona a nota do filme à lista de ratings
    ratings.append(rating)
    
    # Remove os parênteses do número de votos e adiciona à lista de contagem de votos
    vote_count.append(vote.strip('()'))

# Visualiza os primeiros registros
ratings[0:5]    

# Tamanho da lista
len(ratings)

# Visualiza os primeiros registros
vote_count[0:5]

# Tamanho da lista
len(vote_count)

# Extraindo a tag div com a descrição
des_lst = soup.findAll('div', attrs = {'class':'ipc-html-content-inner-div'})

# List comprehension para extrair o texto
descriptions = [des.text for des in des_lst]

# Visualiza os primeiros registros
descriptions[0:5]

# Tamanho da lista
len(descriptions)

#Salvando o Resultado do Web Scraping
print(f"Tamanho de 'title': {len(title)}")
print(f"Tamanho de 'description': {len(descriptions)}")
print(f"Tamanho de 'release_year': {len(years)}")
print(f"Tamanho de 'duration': {len(duration)}")
print(f"Tamanho de 'ratings': {len(ratings)}")
print(f"Tamanho de 'votes_count': {len(vote_count)}")

# Prepara o dataframe final
df_movie_dsa = pd.DataFrame({'titulo': title, 
                             'descricao': descriptions, 
                             'ano_lancamento': years, 
                             'duracao': duration,
                             'avaliacao': ratings, 
                             'votos': vote_count})

# Shape
df_movie_dsa.shape

# Visualiza os primeiros registros
df_movie_dsa.head()

# Salva o dataframe em CSV
df_movie_dsa.to_csv("dataset.csv", index = False)

