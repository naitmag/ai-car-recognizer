import numpy as np
import tensorflow as tf
from keras import Sequential
from keras.src import layers

from model.config import DATASET_DIR, img_height, img_width, batch_size, MODEL_PATH

def load_model():
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=[img_height, img_width],
        batch_size=batch_size
    )

    class_names = train_ds.class_names
    print(f"Class names: {class_names}")

    num_classes = len(class_names)
    model = Sequential([
        layers.Input(shape=(img_height, img_width, 3)),
        layers.Rescaling(1. / 255),

        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1),

        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),

        layers.Dropout(0.2),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    ),

    model.load_weights(MODEL_PATH)

    return model, class_names


model, class_names = load_model()


def get_result(image):
    img = tf.keras.utils.load_img(image, target_size=(img_height, img_width))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    result = "На изображении скорее всего {} (Вероятность {:.2f}%)".format(
        class_names[np.argmax(score)],
        100 * np.max(score)
    )
    return result


if __name__ == "__main__":
    get_result('requests/1.jpg')
