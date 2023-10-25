import csv

problem = 'fl'

def train():
    right = []
    wrong = []
    with open(f'./{problem}_right_training.txt') as infile:
        right = infile.readlines()
    with open(f'./{problem}_wrong_training.txt') as infile:
        wrong = infile.readlines()

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

    # TODO Use your bigrams to grade each student input and check if you graded
    # it correctly

    print("Number graded correctly: ", correctly_graded)
    print("Number graded incorrectly: ", incorrectly_graded)


if __name__ == '__main__':

    bigrams_right, bigrams_wrong = train()
    test(bigrams_right, bigrams_wrong)
