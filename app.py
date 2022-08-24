import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import pandas as pd
import datetime
import time

def appendaBase(url, id, titulo):
    df = pd.read_csv('videos.csv')
    lista = [url, id, titulo, datetime.datetime.now()]
    df = df.append(pd.DataFrame([lista], columns=["url","id","titulo","data"]), ignore_index=True)
    df.to_csv('videos.csv', index=False)

def lenBase():
    df = pd.read_csv('videos.csv')
    return len(df)

def pegaID(url):
    url_clean = url.replace('https://www.youtube.com/watch?v=', '')\
    .replace('http://www.youtube.com/watch?v=', '')\
    .replace('youtube.com/watch?v=', '')
    return url_clean

def pegaTitulo(url):
    soup = BeautifulSoup(urlopen(url), 'lxml')
    return soup.title.get_text()

def pegaLegenda(video):
    formatter = TextFormatter()
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video, languages=['pt'])
        texto = formatter.format_transcript(transcript)
        return texto
    except:
        return "Transcrição não disponível para esse vídeo."



if __name__ == '__main__':
    st.set_page_config(page_title="LêAih! - Baixador de Transcrições do Youtube", page_icon="🦑", layout="centered", initial_sidebar_state="auto", menu_items=None)

    st.title('LêAih!')
    st.subheader('Baixe a transcrição de um vídeo do Youtube')
    st.caption("Desenvolvido por Matheus C. Pestana (matheus.pestana@iesp.uerj.br) - Versão 0.3")


    baixado = True

    url_video = st.text_input('Digite a URL completa do vídeo',
                                value='https://www.youtube.com/watch?v=azjU-Sve1cg',
                                help='Coloque a URL completa(incluindo o https://)')

    titulo_video = pegaTitulo(url_video).replace('- YouTube', '')
    id_video = pegaID(url_video)

    btn_ler, btn_baixar, total_baixado = st.columns(3, gap='small')

    with btn_ler:
        ler = st.button('Ler')
        if ler:
            with st.spinner("Baixando transcrição..."):
                texto = pegaLegenda(id_video)
                baixado = False
                appendaBase(url_video, id_video, titulo_video)



    with btn_baixar:
        if baixado==False:
            baixar = st.download_button('Baixar transcrição em .txt', texto, file_name=f'{titulo_video}.txt', disabled=baixado)
    
    if ler:
        st.markdown(f'#### Transcrição do vídeo "{titulo_video}" ')
        st.write(texto)

    with total_baixado:
        st.metric("Transcrições já processadas", lenBase())