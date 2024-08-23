import requests
import json
import os
import time

API_KEY = "YOUR_API_KEY"

# Function to fetch random public matches
def fetch_random_ranked_matches():
    url = f"https://api.opendota.com/api/publicMatches?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch public matches")
        return None

# Function to fetch detailed match data for a specific match
def fetch_match_data(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch match data for match_id: {match_id}")
        return None

# Function to extract relevant data from match details
def extract_match_data(match_data):
    extracted_data = {
        'match_id': match_data.get('match_id'),
        'radiant_win': match_data.get('radiant_win'),
        'players': []
    }
    
    for player in match_data.get('players', []):
        player_data = {
            'hero_id': player.get('hero_id'),
            'items': [
                player.get('item_0'),
                player.get('item_1'),
                player.get('item_2'),
                player.get('item_3'),
                player.get('item_4'),
                player.get('item_5'),
                player.get('backpack_0'),
                player.get('backpack_1'),
                player.get('backpack_2')
            ],
            'win': player.get('win')
        }
        extracted_data['players'].append(player_data)
    
    return extracted_data

# Function to save data to a file in the raw folder
def save_data_to_file(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure the directory exists
    with open(file_path, 'a') as f:
        json.dump(data, f)
        f.write(",\n")  # Separate each JSON object with a comma for proper formatting

# Main function to gather match data
def gather_ranked_match_data():
    total_data_size = 0
    data_file = os.path.join(os.path.dirname(__file__), '../data/raw/raw_data.json')

    # Ensure the JSON file starts with an opening bracket to make it an array
    with open(data_file, 'w') as f:
        f.write("[\n")

    try:
        while total_data_size < 5 * (1024**3):  # Target size is 5 GB
            public_matches = fetch_random_ranked_matches()
            
            if not public_matches:
                time.sleep(10)  # wait before retrying
                continue
            
            for match in public_matches:
                if match.get('avg_rank_tier'):  # Only consider ranked matches
                    match_data = fetch_match_data(match['match_id'])
                    if match_data:
                        extracted_data = extract_match_data(match_data)
                        save_data_to_file(extracted_data, data_file)
                        
                        # Update total data size
                        total_data_size += len(json.dumps(extracted_data).encode('utf-8'))

                    time.sleep(1)  # Avoid hitting API rate limits
            
            print(f"Total data size: {total_data_size / (1024**3):.2f} GB")
            time.sleep(1)  # To avoid hitting API rate limits
    finally:
        # Ensure the JSON file ends with a closing bracket to close the array
        with open(data_file, 'a') as f:
            f.seek(f.tell() - 2, os.SEEK_SET)  # Move the cursor back to overwrite the last comma
            f.write("\n]")

    print("Data collection complete!")

# Example usage
gather_ranked_match_data()
