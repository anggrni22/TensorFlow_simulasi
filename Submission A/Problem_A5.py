# =======================================================================================
# PROBLEM A5
#
# Build and train a neural network model using the Sunspots.csv dataset.
# Use MAE as the metrics of your neural network model.
# We provided code for normalizing the data. Please do not change the code.
# Do not use lambda layers in your model.
#
# The dataset used in this problem is downloaded from kaggle.com/robervalt/sunspots
#
# Desired MAE < 0.15 on the normalized dataset.
# ========================================================================================

import csv
import tensorflow as tf
import numpy as np
import urllib

# DO NOT CHANGE THIS CODE
def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(window_size + 1, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(window_size + 1))
    ds = ds.shuffle(shuffle_buffer)
    ds = ds.map(lambda w: (w[:-1], w[1:]))
    return ds.batch(batch_size).prefetch(1)


def solution_A5():
    data_url = 'https://github.com/dicodingacademy/assets/raw/main/Simulation/machine_learning/sunspots.csv'
    urllib.request.urlretrieve(data_url, 'sunspots.csv')

    time_step = []
    sunspots = []

    with open('sunspots.csv') as csvfile:
      reader = csv.reader(csvfile, delimiter=',')
      next(reader)
      for row in reader:
        sunspots.append(float(row[2]))
        time_step.append(int(row[0]))

    series = np.array(sunspots)
    time = np.array(time_step)

    # Normalization Function. DO NOT CHANGE THIS CODE
    min=np.min(series)
    max=np.max(series)
    series -= min
    series /= max
    time=np.array(time_step)

    # DO NOT CHANGE THIS CODE
    split_time=3000


    time_train=  time[:split_time]
    x_train=  series[:split_time]
    time_valid=  time[split_time:]
    x_valid= series[split_time:]

    # DO NOT CHANGE THIS CODE
    window_size=30
    batch_size=32
    shuffle_buffer_size=1000


    train_set=windowed_dataset(x_train, window_size=window_size,
                               batch_size=batch_size, shuffle_buffer=shuffle_buffer_size)


    model=tf.keras.models.Sequential([
      tf.keras.layers.Conv1D(filters=32, kernel_size=1,
                             activation='relu',
                             input_shape=(None, 1)),
      tf.keras.layers.LSTM(32, return_sequences=True),
      tf.keras.layers.Dense(10, activation="relu"),
      tf.keras.layers.Dense(1)
    ])

    # YOUR CODE
    optimizer = tf.keras.optimizers.SGD(learning_rate=1e-4, momentum=0.9)
    model.compile(loss=tf.keras.losses.Huber(),
                  optimizer=optimizer,
                  metrics=["mae"])

    class myCallback(tf.keras.callbacks.Callback):
        def on_epochs_end(self, epoch, logs={}):
            if(logs.get('mae') < 0.15):
                self.model.stop_training = True

    callbacks = myCallback()

    model.fit(train_set, epochs=100, callbacks=[callbacks])
    return model


# The code below is to save your model as a .h5 file.
# It will be saved automatically in your Submission folder.
if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    model=solution_A5()
    model.save("model_A5.h5")
