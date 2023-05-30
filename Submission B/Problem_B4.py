# ===================================================================================================
# PROBLEM B4
#
# Build and train a classifier for the BBC-text dataset.
# This is a multiclass classification problem.
# Do not use lambda layers in your model.
#
# The dataset used in this problem is originally published in: http://mlg.ucd.ie/datasets/bbc.html.
#
# Desired accuracy and validation_accuracy > 91%
# ===================================================================================================
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import pandas as pd


def solution_B4():
    bbc = pd.read_csv(
        'https://github.com/dicodingacademy/assets/raw/main/Simulation/machine_learning/bbc-text.csv')

    # DO NOT CHANGE THIS CODE
    # Make sure you used all of these parameters or you can not pass this test
    vocab_size = 1000
    embedding_dim = 16
    max_length = 120
    trunc_type = 'post'
    padding_type = 'post'
    oov_tok = "<OOV>"
    training_portion = .8

    # YOUR CODE HERE
    # Using "shuffle=False"
    text_train, text_test, cat_train, cat_test = train_test_split(bbc['text'], bbc['category'],
                                                                  train_size=training_portion, shuffle=False)

    # Fit your tokenizer with training data
    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
    tokenizer.fit_on_texts(text_train)
    train_seq = tokenizer.texts_to_sequences(text_train)
    padded = pad_sequences(train_seq, maxlen=max_length, truncating=trunc_type, padding=padding_type)
    test_seq = tokenizer.texts_to_sequences(text_test)
    test_padded = pad_sequences(test_seq, maxlen=max_length, truncating=trunc_type, padding=padding_type)

    tokenizero=Tokenizer()
    tokenizero.fit_on_texts(cat_train)
    seq_train = tokenizero.texts_to_sequences(cat_train)
    cat_train_np = np.array(seq_train).reshape(-1)
    seq_test = tokenizero.texts_to_sequences(cat_test)
    cat_test_np = np.array(seq_test).reshape(-1)


    model = tf.keras.Sequential([
        # YOUR CODE HERE.
        # YOUR CODE HERE. DO not change the last layer or test may fail
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(7, activation='softmax')
    ])

    # Make sure you are using "sparse_categorical_crossentropy" as a loss fuction
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    class myCallback(tf.keras.callbacks.Callback):
        def on_epochs_end(self, epoch, logs={}):
            if(logs.get('accuracy') > 0.91):
                self.model.stop_training = True

    callbacks = myCallback()

    model.fit(padded, cat_train_np,
              epochs = 50,
              validation_data =(test_padded, cat_test_np),
              callbacks=[callbacks])


    return model

    # The code below is to save your model as a .h5 file.
    # It will be saved automatically in your Submission folder.
if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    model = solution_B4()
    model.save("model_B4.h5")
