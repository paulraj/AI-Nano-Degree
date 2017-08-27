import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    words = test_set.get_all_Xlengths()
    for word_id in range(0, len(test_set.get_all_sequences())):
        probability = {}
        best_score = float("-Inf")
        best_guess = None
        X, lengths = words[word_id]
        for word, hmm_model in models.items():
            try:
                current_score = hmm_model.score(X, lengths)
                probability[word] = current_score
                if current_score > best_score:
                    best_score = current_score
                    best_guess = word
            except:
                probability[word] = best_score
        probabilities.append(probability)
        guesses.append(best_guess)
    return probabilities, guesses
