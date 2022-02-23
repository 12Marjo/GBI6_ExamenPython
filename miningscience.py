def download_pubmed (keyword):
    """
    La función input se usa como función de entrada arrojando  como resultado una lista de todos mis id de la busqueda en pubmed
    """
    from Bio import Entrez
    from Bio import SeqIO
    from Bio import GenBank 
    Entrez.email = 'marjorie.bonilla@est.ikiam.edu.ec'
    marjo = Entrez.read(Entrez.esearch(db="pubmed", 
                            term=keyword,
                            usehistory="y"))
    webenv = marjo ["WebEnv"]
    query_key = marjo ["QueryKey"]
    handle = Entrez.efetch(db="pubmed",
                           rettype="medline", 
                           retmode="text", 
                           retstart=0,
                           retmax=543, webenv=webenv, query_key=query_key)
    lectura = handle.read()
    return lectura

import csv 
import re
import pandas as pd 
from collections import Counter

def mining_pubs(tipo,lectura):
    """
  Se necesitan tres variables "DP", "AU","AD" en la función para que de resultado se muestre una dataframe
    """
    if tipo == "DP":
        PMID = re.findall("PMID- (\d*)", lectura) 
        year = re.findall("DP\s{2}-\s(\d{4})", lectura)
        pmid_y = pd.DataFrame()
        pmid_y["PMID"] = PMID
        pmid_y["Año de publicación"] = year
        return (pmid_y)
    elif tipo == "AU": 
        PMID = re.findall("PMID- (\d*)", lectura) 
        autores = lectura.split("PMID- ")
        autores.pop(0)
        num_autores = []
        for i in range(len(autores)):
            numero = re.findall("AU -", autores[i])
            n = (len(numero))
            num_autores.append(n)
        pmid_a = pd.DataFrame()
        pmid_a["PMID"] = PMID 
        pmid_a["Numero de autores"] = num_autores
        return (pmid_a)
    elif tipo == "AD": 
        texto = re.sub(r" [A-Z]{1}\.","", lectura)
        texto = re.sub(r"Av\.","", lectura)
        texto = re.sub(r"Vic\.","", lectura)
        texto = re.sub(r"Tas\.","", lectura)
        AD = texto.split("AD  - ")
        n_paises = []
        for i in range(len(AD)): 
            pais = re.findall("\S, ([A-Za-z]*)\.", AD[i])
            if not pais == []: 
                if not len(pais) >= 2:  
                    if re.findall("^[A-Z]", pais[0]): 
                        n_paises.append(pais[0])
        conteo=Counter(n_paises)
        resultado = {}
        for clave in conteo:
            valor = conteo[clave]
            if valor != 1: 
                resultado[clave] = valor 
        veces_pais = pd.DataFrame()
        veces_pais["pais"] = resultado.keys()
        veces_pais["numero de autores"] = resultado.values()
        return (veces_pais)

