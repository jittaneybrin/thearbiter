
import settings as settings
import elastic_search as elastic_search 
from elasticsearch.helpers import bulk
import embs as embs
import constants as constants

#loads in supported games into ElasticSearch database
def load_supported_games(es_client):
    print("Attempting to load in supported games.")
    supported_games = constants.supported_games
    for game, index in supported_games:
        filedir = rf"uploads/supported_games/{game}.pdf"
        try:
            elastic_search.new_game_index(es_client, filedir, index=index)
            print(f"Successfully created new Elastic Search index for supported game: {game}, with index: {index}")
        except Exception as e:
            print(f"Error: Could not create new Elastic Search index for supported game: {game}. Exception: {e}")
