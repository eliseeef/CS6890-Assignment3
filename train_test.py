import csv

problem = 'fl'

def get_bag_o_words(list_of_sentences):
    bag_o_words_dict = {}
    for sentence in list_of_sentences:
        bag_o_words = sentence.lower().split()
        for word in bag_o_words:
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
    for i in range(len(words) - 1):
        bigrams.append((words[i], words[i + 1]))
    # print("BIGRM ", bigrams)
    return bigrams

def get_bigram_probability_two(list_of_sentences):
    bag_o_words_freq = get_bag_o_words(list_of_sentences)
    bigrams = []
    for sentence in list_of_sentences:
        words = sentence.lower().split()
        for i in range(len(words) - 1):
            bigrams.append((words[i], words[i + 1]))
    frequencies = get_bigram_frequency(bigrams)

    bigram_probs = {bigram: count / bag_o_words_freq[bigram[0]] for bigram, count in frequencies.items()}
    print(bigram_probs)
    return bigram_probs

def get_bigram_probability(list_of_sentences):
    bigrams = []
    for sentence in list_of_sentences:
        words = sentence.lower().split()
        for i in range(len(words) - 1):
            bigrams.append((words[i], words[i + 1]))
    frequencies = get_bigram_frequency(bigrams)
    # print("FREQU ", frequencies)
    total_bigram_count = len(frequencies)
    bigram_probs = {bigram: count / total_bigram_count for bigram, count in frequencies.items()}
    return bigram_probs

#update bigram probailities, add and divide by the count of hte seoncd word and weight it and then add it and then 

def get_likelihood_correct(submission_bigrams, right_prob, wrong_prob):
    likelihood_correct = 0
    likelihood_incorrect = 0
    for bigram in submission_bigrams:
        # print("BIGRAM likeli ", bigram)
        if bigram in right_prob:
            # print("BIGRAM ", bigram)
            # print("RIGHT PROB ", right_prob[bigram])
            likelihood_correct += right_prob[bigram]
            # likelihood_correct *= right_prob[bigram]
            # likelihood_correct += 1
            # print("LIKELIHOOD COORECT ", likelihood_correct)
        if bigram in wrong_prob:
            # print("BIGRAM ", bigram)
            # print("WRONG PROB ", wrong_prob[bigram])
            likelihood_incorrect += wrong_prob[bigram]
            # likelihood_incorrect *= wrong_prob[bigram]
            # likelihood_incorrect += 1
            # print("LIKELIHOOD INCOORECT ", likelihood_incorrect)

    
    print("LIKELIHOOD CORRECT ", likelihood_correct)
    print("LIKELIHOOD INCORRECT ", likelihood_incorrect)

    return likelihood_correct >= likelihood_incorrect

def classify_submission(bigrams_right, bigrams_wrong, submissions):
    print("CLASSIFY SUBMISSION ")
    correctly_graded = 0
    incorrectly_graded = 0

    for submission, validity in submissions.items():
        submission_bigrams = get_bigram_frequency(get_bigrams(submission))
        likelihood_correct = get_likelihood_correct(submission_bigrams, bigrams_right, bigrams_wrong)
        # print(" CORRECT?? ", likelihood_correct)
        if likelihood_correct: # it is correct
            # print("IT IS CORRECT ", validity)
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
    print("TRAINNNNN")
    right = []
    wrong = []
    with open(f'./{problem}_right_training.txt') as infile:
        right = infile.readlines()
    with open(f'./{problem}_wrong_training.txt') as infile:
        wrong = infile.readlines()

    bigrams_right = get_bigram_probability_two(right)
    bigrams_wrong = get_bigram_probability_two(wrong)

    return bigrams_right, bigrams_wrong

    # TODO: use training data to calculate some bigram probabilities

def test(bigrams_right, bigrams_wrong):
    correctly_graded = 0
    incorrectly_graded = 0

    submissions = {}
    with open(f'./{problem}_test_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            submissions[row[1]] = row[2]
    del submissions['Student.answer']

    print("CLASSIFYING...")
    correctly_graded, incorrectly_graded = classify_submission(bigrams_right, bigrams_wrong, submissions)

    # TODO Use your bigrams to grade each student input and check if you graded
    # it correctly

    print("Number graded correctly: ", correctly_graded)
    print("Number graded incorrectly: ", incorrectly_graded)


if __name__ == '__main__':

    bigrams_right, bigrams_wrong = train()
    test(bigrams_right, bigrams_wrong)

# false or true
# how many biagrams in a sentence are in the false list
# how many bigrams in a sentence are in the true list