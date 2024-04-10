import anki_connect
import easy_words
import json
import sys

def copy_the_words_that_not_in_top_n(n, source_deck, dest_deck):
  ret = 0
  vocab_pool = easy_words.get_top_n_words(n)
  notes_id = anki_connect.get_all_note_ids_from_deck(source_deck)
  if notes_id is None:
    print("No note found")
    return
  for note_id in notes_id:
    note_info = anki_connect.get_note_info(note_id)
    if note_info is None:
      print("Note not found.")
      return
    word = note_info[0]['fields']['Keyword']['value']
    if word not in vocab_pool:
      result = anki_connect.copy_note_to_other_deck(note_id, dest_deck)
      if result is None:
        print(f"Word '{word}' FAILED!\n")
        continue
      sys.stdout.write("\033[F")  # ANSI escape code to move up
      sys.stdout.write("\033[K")  # ANSI escape code to clear the line
      print(f"Word '{word}' is copied to deck '{dest_deck}'")
      ret += 1

  return ret

def process_deck(deck_to_process):
  list_of_deck = anki_connect.get_all_decks()
  if (list_of_deck is None):
    print("No deck found")
    return
  # load data from file "data.json"
  with open("data.json", "r") as read_file:
    data = json.load(read_file)
    # iterrate json array
    for mentee in data:
      list_of_already_used_deck = mentee['src_deck_used']
      if deck_to_process in list_of_already_used_deck:
        print(f"Deck '{deck_to_process}' already processed before\n")
        continue
      else:
        print(f"Processing deck '{deck_to_process}'\n")
        # In general, the Dolch Word List, a compilation of frequently used words in the English language,
        # contains about 220 "service words" (which include pronouns, adjectives, adverbs, prepositions,
        # conjunctions, and verbs) and 95 high-frequency nouns. This list is a good starting point for
        # identifying common English words, especially for children's literacy.

        # However, if we consider the broader category of function words, linguistic research suggests
        # there are approximately 200 to 300 function words in English. These include various categories
        # such as determiners, pronouns, prepositions, conjunctions, auxiliary verbs, modal verbs,
        # particles, and more.
        n = mentee['vocab_size'] + 300  # Add 300 very essential words
        dest_deck = mentee['deck'][0]["deck_name"]
        # check if dest deck exits in list of deck
        if dest_deck not in list_of_deck:
          anki_connect.create_new_deck(dest_deck)

        ret = copy_the_words_that_not_in_top_n(n, deck_to_process, dest_deck)
        if ret > 0:
          list_of_already_used_deck.append(deck_to_process)
          mentee['src_deck_used'] = list_of_already_used_deck
          mentee['deck'][0]["total_words"] += ret
          with open("data.json", "w") as write_file:
            json.dump(data, write_file, indent=4)
        else:
          print(f"No word is copied to deck '{dest_deck}'")

if __name__ == "__main__":
  deck_to_process = ['4000 Essential English Words - Book 1',
                      '4000 Essential English Words - Book 2',
                      '4000 Essential English Words - Book 3',
                      '4000 Essential English Words - Book 4',
                      '4000 Essential English Words - Book 5',
                      '4000 Essential English Words - Book 6']
  for deck in deck_to_process:
    process_deck(deck)
  print("Done")
