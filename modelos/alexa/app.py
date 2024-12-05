import speech_recognition as sr
import pyttsx3
#import pywhatkit
import datetime
import wikipedia
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests
import pywhatkit as kit


audio = sr.Recognizer()
maquina = pyttsx3.init()

def obter_conteudo(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança uma exceção para status de erro
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None
    
def obter_primeiro_link(termo_pesquisa):
    #url = 'https://www.google.com/search?q=' + termo_pesquisa.replace(' ', '+')
    url = 'https://html.duckduckgo.com/html/?q=' + termo_pesquisa.replace(' ', '+')
    print('url', url)
    html = obter_conteudo(url)
    print(html)
    if not html:
        return None

    soup = BeautifulSoup(html, 'html.parser')

    # Encontrar o primeiro link orgânico
    for a in soup.select('a'):
        href = a.get('href')
        if href and isinstance(href, str) and href.strip() and href.startswith('https://'):
            # Extrair o link limpo
            ##link_limpo = href.split('https://')[1].split('&')[0]
            return href

    return None

def executar():
    try:
        with sr.Microphone() as source:
            print('Ouvindo...')
            voice = audio.listen(source)
            comando = audio.recognize_google(voice, language='pt-BR')
            comando = comando.lower()
            if 'alexa' in comando:
                comando = comando.replace('alexa', '')
                print(comando)
                maquina.say(comando)
                maquina.runAndWait()
    except:
        print('microfone não está ok')

    return comando


def comando_voz():
    ecomando  = executar()
    if 'horas' in ecomando:
        hora = datetime.datetime.now().strftime('%H:%M')
        maquina.say('Agora sao ' + hora)
        maquina.runAndWait()
    if 'procure por' in ecomando:
        procurar = ecomando.replace('procure por', '')
        wikipedia.set_lang('pt')
        resultado = wikipedia.summary(procurar, 3)
        print(resultado)
        maquina.say(resultado)
        maquina.runAndWait()
    if 'pesquise por' in ecomando:
        procurar = ecomando.replace('pesquise por', '')
        print(procurar)
        resultado = DDGS().text(procurar, max_results=1)
        print(resultado)
        maquina.say(resultado[0]['body'])
        maquina.runAndWait()
    if 'google' in ecomando:
        procurar = ecomando.replace('google', '')
        #url = 'https://www.google.com/search?q=' + procurar.replace(' ', '+')
        link = obter_primeiro_link(procurar)
        resultado = obter_conteudo(link)
        print(resultado)
        maquina.say(resultado)
        maquina.runAndWait()

    if 'toque' in ecomando:
        procurar = ecomando.replace('toque', '')
        kit.playonyt(procurar)  
        maquina.say('Tocando ' + procurar)
        maquina.runAndWait()


comando_voz()
