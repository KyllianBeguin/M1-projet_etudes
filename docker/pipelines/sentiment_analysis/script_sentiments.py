import pandas as pd
from afinn import Afinn

def analyse_sentiments_csv(file_path):
    # Lecture du fichier CSV
    df = pd.read_csv(file_path)
    
    # Récupération des éléments de la 3ème colonne dans une liste
    colonne3 = df.iloc[:, 2].tolist()
    
    # Initialisation de l'analyseur de sentiments AFINN
    afinn = Afinn()
    
    # Analyse des sentiments pour chaque élément de la liste
    resultats_sentiments = []
    nb_positifs = 0
    nb_negatifs = 0
    nb_neutres = 0
    
    for element in colonne3 :
        score_sentiment = afinn.score(element)
        resultats_sentiments.append(score_sentiment)
        
        if score_sentiment > 0 :
            nb_positifs += 1
        elif score_sentiment < 0 :
            nb_negatifs += 1
        else:
            nb_neutres += 1
    
    return resultats_sentiments, nb_positifs, nb_negatifs, nb_neutres
