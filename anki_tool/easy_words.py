import nltk
from nltk.corpus import brown
nltk.download('brown')
nltk.download('punkt')

def get_top_n_words(n):
    # Get all words from the Brown corpus
    words = brown.words()
    # Calculate frequency distribution
    freq_dist = nltk.FreqDist(w.lower() for w in words)
    # Get the top n words
    top_n_words = [word for word, freq in freq_dist.most_common(n)]
    return top_n_words

if __name__ == '__main__':
    top_3000_words = get_top_n_words(3000)
    # N_ow you can use top_3000_words as needed
    # For example, check if a word is in the top 3000 words
    word_to_check = "arrive"
    if word_to_check.lower() in top_3000_words:
        print(f"The word '{word_to_check}' is likely in the vocabulary pool.")
    else:
        print(f"The word '{word_to_check}' is not likely in the vocabulary pool.")