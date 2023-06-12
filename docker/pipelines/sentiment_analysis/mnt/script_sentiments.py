# Zone d'import des bibliothèques
# Analyse de sentiment
from afinn import Afinn
# Connexion à la base de données
from pymongo import MongoClient

# Zone de création des fonctions
def get_mongo_raw_tweets() -> list:
    """
    Fonction de récolte des tweets depuis la base mongodb

    Un Tweet est composé de
    * _id : l'id du tweet CHANGERA PROCHAINEMENT
    * Date : la date du tweet
    * Tweet : Le text du tweet

    :Retourne: une liste de Tweets
    """

    # Connextion à mongodb, bdd TweetsDB, Collection RawDataCollection
    host = "mongodb://mongo:27017"
    client = MongoClient(host)
    db = client['TweetsDB']
    collection = db['RawDataCollection']

    # Récolte de tous les tweets et stockage en liste
    raw_tweets = [tweet for tweet in collection.find()]

    return raw_tweets


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
