import requests

# Function to send requests to AnkiConnect
def invoke(action, params={}):
    request = {'action': action, 'params': params, 'version': 6}
    response = requests.post('http://localhost:8765', json=request).json()
    if len(response) != 2:
        return None
    if 'error' not in response:
        return None
    if 'result' not in response:
        return None
    if response['error'] is not None:
        return None
    return response['result']

def get_all_card_ids_from_deck(deck_name):
    # Get the list of card IDs in the deck
    card_ids = invoke('findCards', {'query': f'deck:"{deck_name}"'})
    return card_ids

def get_card_info(card_id):
    # Get card info
    card_info = invoke('cardsInfo', {'cards': [card_id]})
    return card_info

def move_cards_to_deck(card_ids, deck_name):
    # Move cards to a different deck
    invoke('changeDeck', {'cards': card_ids, 'deck': deck_name})

def delete_cards(card_ids):
    # Delete cards
    invoke('deleteNotes', {'notes': card_ids})

def create_new_deck(deck_name):
    # Create a new deck
    invoke('createDeck', {'deck': deck_name})

def get_all_decks():
    # Get all deck names
    deck_names = invoke('deckNames')
    return deck_names

def get_all_cards_in_deck(deck_name):
    # Get all cards in a deck
    card_ids = get_all_card_ids_from_deck(deck_name)
    cards = [get_card_info(card_id) for card_id in card_ids]
    return cards

def get_all_note_ids_from_deck(deck_name):
    query = f'deck:"{deck_name}"'
    note_ids = invoke('findNotes', {'query': query})
    return note_ids

def get_note_info(note_id):
    # Get note info
    note_info = invoke('notesInfo', {'notes': [note_id]})
    return note_info

def copy_note_to_other_deck(note_id, destination_deck_name):
    # Fetch the content of the original note
    note_info = invoke('notesInfo', {'notes': [note_id]})
    if note_info is None:
        print("Note not found.")
        return

    original_note = note_info[0]
    fields = original_note['fields']
    # Prepare fields for the new note, preserving the value and without formatting
    new_fields = {field: fields[field]['value'] for field in fields}

    # Create a new note in the destination deck with the same content
    result = invoke('addNote', {
        'note': {
            'deckName': destination_deck_name,
            'modelName': original_note['modelName'],  # Use the same model as the original note
            'fields': new_fields,
            'options': {
                'allowDuplicate': True,  # Set this to False if you don't want duplicates
            },
            'tags': original_note['tags'],  # Copy tags from the original note
        }
    })
    return result

if __name__ == '__main__':
    deck_name = "test_create_deck"
    src_deck = "4000 Essential English Words - Book 1"
    note_ids = get_all_note_ids_from_deck(src_deck)
    copy_note_to_other_deck(note_ids[0], deck_name)