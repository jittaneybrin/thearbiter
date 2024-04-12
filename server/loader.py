
import settings as settings
import elastic_search as elastic_search 
import embs as embs
import os

#loads in supported games into ElasticSearch database
def load_supported_games(es_client):
    print("Attempting to load in supported games.")
    #Iterate through supported games from supported_games directory
    supported_games_dir = rf"uploads/supported_games"
    for filename in os.listdir(supported_games_dir):
        if filename.endswith(".pdf"):
            game_name = os.path.splitext(filename)[0]  # Extract the game name without extension
            filedir = os.path.join(supported_games_dir, filename)
            index = game_name.lower().replace(" ", "_") + "_default_index"  # Create index based on game name

            #check if index was already created
            if elastic_search.index_already_exists(es_client, index):
                print(f"ElasticSearch Index \"{index}\" for supported game \"{game_name}\" already exists. A new index was not created.")
            else:
                try:
                    filedir = rf"uploads/supported_games/{game_name}.pdf"
                    elastic_search.new_game_index(es_client, filedir, index=index)
                    print(f"Successfully created new Elastic Search index for supported game: {game_name}, with index: {index}")
                except Exception as e:
                    print(f"Error: Could not create new Elastic Search index for supported game: {game_name}. Exception: {e}")