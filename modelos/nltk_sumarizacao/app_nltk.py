import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from heapq import nlargest

# URL do site de notícias
url = 'https://g1.globo.com/economia/noticia/2024/04/24/governo-propoe-que-imposto-do-pecado-seja-cobrado-sobre-cigarros-bebidas-alcoolicas-acucaradas-carros-e-petroleo.ghtml'  # Substitua pela URL do site de notícias desejado

# Realiza o request para a página
response = requests.get(url)

# Extrai o conteúdo HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Extrai os títulos das notícias
titles = [title.text.strip() for title in soup.find_all('h2')]

# Extrai os conteúdos das notícias
contents = [content.text.strip() for content in soup.find_all('p')]

# Combina os títulos e conteúdos das notícias
news_articles = zip(titles, contents)

# Função para sumarização de texto
def summarize_text(text, num_sentences=2):
    sentences = sent_tokenize(text)
    summarized_sentences = nlargest(num_sentences, sentences, key=len)
    summary = ' '.join(summarized_sentences)
    return summary

# Imprime as notícias com título e resumo
for title, content in news_articles:
    print("Título:", title)
    print("Resumo:", summarize_text(content))
    print()