import csv

problem = 'fl'

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
    return bigrams

def get_bigram_probability(list_of_sentences):
    bigrams = []
    for sentence in list_of_sentences:
        words = sentence.lower().split()
        for i in range(len(words) - 1):
            bigrams.append((words[i], words[i + 1]))
    frequencies = get_bigram_frequency(bigrams)
    total_bigram_count = len(frequencies)
    bigram_probs = {bigram: count / total_bigram_count for bigram, count in frequencies.items()}
    return bigram_probs

def get_submissions_lists(submissions):
    valid_submissions = []
    invalid_submissions = []
    for sentence, validity in submissions.items():
        if int(validity) == 1:
            valid_submissions.append(sentence.lower())
        else:
            invalid_submissions.append(sentence.lower())
    return valid_submissions, invalid_submissions

def get_likelihood_correct(submission_bigrams, right_prob, wrong_prob):
    likelihood_correct = 1.0
    likelihood_incorrect = 1.0
    for bigram in submission_bigrams:
        if bigram in right_prob:
            likelihood_correct *= right_prob[bigram]
        if bigram in wrong_prob:
            likelihood_incorrect *= wrong_prob[bigram]
    
    return likelihood_correct > likelihood_incorrect

def classify_submission(bigrams_right, bigrams_wrong, submissions):
    print("CLASSIFY SUBMISSION ")
    correct_count = 0
    incorrect_count = 0
    for submission in submissions:
        print("SUBMISSION ", submission)
        print("BIGRAMS ", get_bigram_frequency(get_bigrams(submission)))
        submission_bigrams = get_bigram_frequency(get_bigrams(submission))
        correct = get_likelihood_correct(submission_bigrams, bigrams_right, bigrams_wrong)
        if correct: 
            correct_count += 1
        else:
            incorrect_count += 1
    return correct_count, incorrect_count

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

    # print("SUBMISSIONS ", submissions)
    valid_submissions, invalid_submissions = get_submissions_lists(submissions)
    print("CLASSIFYING...")
    correctly_graded, incorrectly_graded = classify_submission(bigrams_right, bigrams_wrong, valid_submissions)

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