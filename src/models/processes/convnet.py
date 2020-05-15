"""
ConvNet process to generate models for the CIFAR-10 dataset.
"""

from tensorflow.keras.activations import *
from tensorflow.keras.layers import *
from tensorflow.keras.metrics import *
from tensorflow.keras.models import *

from src.cifar10 import Cifar10


def create_model(
        optimizer="Adam",
        dropout_values=None,
        activation=relu,
        filters=64,
        padding_value="same",
        kernel_size=(3, 3)
):
    model = Sequential()

    model.add(Conv2D(filters, kernel_size, padding=padding_value, activation=activation,
                     input_shape=(32, 32, 3)))
    for i in range(3):
        model.add(Conv2D(filters, kernel_size, padding=padding_value, activation=activation))
        model.add(MaxPool2D(2, 2))
        if dropout_values is not None and dropout_values[i] is not None:
            model.add(Dropout(dropout_values[i]))

    model.add(Flatten())
    model.add(Dense(256, activation=activation))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation=softmax))

    model.compile(optimizer=optimizer,
                  loss=sparse_categorical_crossentropy,
                  metrics=[sparse_categorical_accuracy])

    return model

def create_model_2(img_width, img_height):
    from tensorflow.keras.optimizers import Adam
    model = Sequential()

    model.add(Conv2D(16, (3, 3), padding='same', activation=relu, input_shape=(img_width, img_height, 3)))
    model.add(MaxPooling2D())
    model.add(Dropout(0.3))

    model.add(Conv2D(32, (3, 3), padding='same'
                     , activation=relu))
    model.add(MaxPooling2D())
    model.add(Dropout(0.3))

    model.add(Conv2D(64, (3, 3), padding='same'
                     , activation=relu))
    model.add(MaxPooling2D())
    model.add(Dropout(0.3))

    model.add(Flatten())

    model.add(Dense(512, activation=relu))  # , kernel_regularizer=l1_l2(l2=0.01) ))
    model.add(Dropout(0.3))

    model.add(Dense(4, activation=softmax))

    # compile the model
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=0.0001),
                  metrics=['accuracy'])
    return model


if __name__ == "__main__":
    cifar10 = Cifar10(dim=3)

    model = create_model(
        "Adam",
        dropout_values=[0.5, 0.5, 0.5, 0.5],
        activation=relu,
        filters=64,
        padding_value="same",
        kernel_size=(3, 3)
    )
    model.build()
    model.summary()
    cifar10.helper.fit(
        model,
        cifar10.x_train,
        cifar10.y_train,
        1024,
        100,
        validation_data=(cifar10.x_test, cifar10.y_test),
        process_name="convnet"
    )
