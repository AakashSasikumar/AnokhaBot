import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import tflearn
import tensorflow as tf
import random, json, pickle


stemmer = LancasterStemmer()


def train():
    with open('context.json') as jsonData:
        intents = json.load(jsonData)
    
    with open("EventContext.json") as jsonData:
        intents2 = json.load(jsonData)
    
    with open("WorkshopContext.json") as jsonData:
        intents3 = json.load(jsonData)
    
    for i in intents2["contexts"]:
        intents["contexts"].append(i)
    
    for i in intents3["contexts"]:
        intents["contexts"].append(i)

    words = []
    tags = []
    documents = []
    stopWords = ["?"]

    for intent in intents['contexts']:
        for pattern in intent['patterns']:
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            w = [stemmer.stem(i.lower()) for i in w if i not in stopWords]
            documents.append((w, intent['tag']))
            if intent['tag'] not in tags:
                tags.append(intent['tag'])

    words = [stemmer.stem(w.lower()) for w in words if w not in stopWords]

    words = sorted(list(set(words)))
    # print(documents)

    trainingData = []

    for doc in documents:
        bag = []
        patternWords = doc[0]

        for w in words:
            bag.append(1) if w in patternWords else bag.append(0)

        outputRow = list([0] * len(tags))
        outputRow[tags.index(doc[1])] = 1
        trainingData.append([bag, outputRow])

    random.shuffle(trainingData)
    trainingData = np.array(trainingData)

    trainingDataX = list(trainingData[:,0])
    trainingDataY = list(trainingData[:,1])

    tf.reset_default_graph()

    net = tflearn.input_data(shape=[None, len(trainingDataX[0])])
    net = tflearn.fully_connected(net, 16)
    net = tflearn.fully_connected(net, 16)
    
    net = tflearn.fully_connected(net, len(trainingDataY[0]), activation='softmax')
    net = tflearn.regression(net)

    model = tflearn.DNN(net, tensorboard_dir='data/tflearn_logs')

    model.fit(trainingDataX, trainingDataY, n_epoch=150, batch_size=8, show_metric=True)
    model.save('data/model/model.tflearn')

    pickle.dump({'words': words, 'classes': tags, 'trainX': trainingDataX, 'trainY': trainingDataY}, open("data/trainingData", "wb"))

if __name__ == '__main__':
    train()
