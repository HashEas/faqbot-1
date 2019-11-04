import csv
import random
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

stopwords = stopwords.words("english")
stopwords.append('.')
stopwords.append('?')
stopwords.append('\'')
stopwords.append(',')
stopwords.append('’')
stopwords.append(')')
stopwords.append('(')
stopwords.append('/')

class DataLoader:
    """ DataLoader Utility """
    def __init__(self, file):
        self.file = file
        self.documents = []
        self.all_words = []
        self.questions = []
        self.answers = []
        self.questions_and_answer = []

    # doc - document words and dictionary - corpus words
    def get_feature(self, doc, dictionary):
        vector = {}
        words = set(doc)
        for w in dictionary:
            vector[w] = (w in words)
        return vector

    def get_documents(self):
        with open(self.file) as file:
            csv_reader = csv.reader(file, delimiter='\t')
            for each_line in csv_reader:
                self.questions.append(each_line[1])
                self.answers.append(each_line[2])
                words = [w.lower() for w in word_tokenize(each_line[1]) if w.lower() not in stopwords]
                for w in words:
                    self.all_words.append(w)
                self.documents.append((words, each_line[0]))
                self.questions_and_answer.append((each_line[0], each_line[1]))
        random.shuffle(self.documents)
        return self.documents

    def get_feature_set(self, question=None):
        if question == None:
            self.get_documents()
            all_words = nltk.FreqDist(self.all_words)
            dictionary = list(all_words.keys())
            feature_set = [(self.get_feature(c, dictionary), d) for c, d in self.documents]
            return feature_set
        else:
            all_words = nltk.FreqDist(self.all_words)
            dictionary = list(all_words.keys())
            feature_set = self.get_feature(word_tokenize(question), dictionary)
            return  feature_set

    def get_questions(self, category=None):
        if category == None:
            print(self.questions_and_answer[0])
            return self.questions
        else:
            res = [q for c, q in self.questions_and_answer if c == category]
            return res
