import csv

problem = 'fl'

def get_bag_o_words(list_of_sentences):
    bag_o_words_dict = {}
    for sentence in list_of_sentences:
        bag_o_words = sentence.lower().split()
        clean_words = [word.replace(",", "").replace(".", "") for word in bag_o_words]
        for word in clean_words:
            if word in bag_o_words_dict:
                bag_o_words_dict[word] += 1
            else:
                bag_o_words_dict[word] = 1
    return bag_o_words_dict

def get_bigram_frequency(list_of_bigrams):
    bigram_dict = {}
    for item in list_of_bigrams:
        if item in bigram_dict:
            bigram_dict[item] += 1
        else:
            bigram_dict[item] = 1
    return bigram_dict

def get_bigrams(sentence):
    bigrams = []
    words = sentence.lower().split()
    clean_words = [word.replace(",", "").replace(".", "") for word in words]
    for i in range(len(clean_words) - 1):
        bigrams.append((clean_words[i], clean_words[i + 1]))
    return bigrams

def get_bigram_probability(list_of_sentences):
    bag_o_words_freq = get_bag_o_words(list_of_sentences)
    bigrams = []
    for sentence in list_of_sentences:
        bigrams += get_bigrams(sentence)
    frequencies = get_bigram_frequency(bigrams)

    # try to remove frequencies of less than one
    filtered_frequencies = {key: value for key, value in frequencies.items() if value >= 2}
    bigram_probs = {bigram: count / bag_o_words_freq[bigram[0]] for bigram, count in filtered_frequencies.items()}
    return bigram_probs

def get_likelihood_correct(submission_bigrams, right_prob, wrong_prob):
    likelihood_correct = 0
    likelihood_incorrect = 0
    for bigram in submission_bigrams:
        if bigram in right_prob:
            likelihood_correct += right_prob[bigram]
        if bigram in wrong_prob:
            likelihood_incorrect += wrong_prob[bigram]

    return likelihood_correct > likelihood_incorrect

def classify_submission(bigrams_right, bigrams_wrong, submissions):
    correctly_graded = 0
    incorrectly_graded = 0

    for submission, validity in submissions.items():
        submission_bigrams = get_bigram_frequency(get_bigrams(submission))
        likelihood_correct = get_likelihood_correct(submission_bigrams, bigrams_right, bigrams_wrong)
        if likelihood_correct: # it is correct
            if int(validity) == 1: # it should be graded correct 
                correctly_graded += 1
            else: 
                incorrectly_graded += 1
        else: # it is incorrect
            if int(validity) == 0: # it should be graded incorrect
                correctly_graded += 1
            else:
                incorrectly_graded += 1 
    return correctly_graded, incorrectly_graded

def train():
    right = []
    wrong = []
    with open(f'./{problem}_right_training.txt') as infile:
        right = infile.readlines()
    with open(f'./{problem}_wrong_training.txt') as infile:
        wrong = infile.readlines()

    bigrams_right = get_bigram_probability(right)
    bigrams_wrong = get_bigram_probability(wrong)

    return bigrams_right, bigrams_wrong

def test(bigrams_right, bigrams_wrong):
    correctly_graded = 0
    incorrectly_graded = 0

    submissions = {}
    with open(f'./{problem}_test_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            submissions[row[1]] = row[2]
    del submissions['Student.answer']

    correctly_graded, incorrectly_graded = classify_submission(bigrams_right, bigrams_wrong, submissions)

    print("Number graded correctly: ", correctly_graded)
    print("Number graded incorrectly: ", incorrectly_graded)


if __name__ == '__main__':
    bigrams_right, bigrams_wrong = train()
    test(bigrams_right, bigrams_wrong)