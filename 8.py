import os
import tensorflow as tf
from tensorflow.keras import preprocess_input
from tensorflow.keras import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.regularizers import l2

dataset_path = 'C:/Users/gorky/Downloads/artificial_intelligence'
suitable_dataset_path = os.path.join(dataset_path, 'suitable')
unsuitable_dataset_path = os.path.join(dataset_path, 'unsuitable')

image_sizes = []
for root, dirs, files in os.walk(dataset_path):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(root, file)
            image = tf.keras.preprocessing.image.load_img(image_path)
            image_sizes.append(image.size)

avg_image_size = tuple(sum(d) // len(image_sizes) for d in zip(*image_sizes))

input_shape = (*avg_image_size, 3)
batch_size = 32
epochs = 20

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_dataset = train_datagen.flow_from_directory(
    dataset_path,
    target_size=input_shape[:2],
    batch_size=batch_size,
    class_mode='binary',
    subset='training'
)

val_dataset = train_datagen.flow_from_directory(
    dataset_path,
    target_size=input_shape[:2],
    batch_size=batch_size,
    class_mode='binary',
    subset='validation'
)

base_model = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)

for layer in base_model.layers[-10:]:
    layer.trainable = True

model = tf.keras.Sequential([
    tf.keras.layers.Resizing(*input_shape[:2]),
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=l2(0.01)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-6)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

model.fit(train_dataset, epochs=epochs, validation_data=val_dataset, callbacks=[reduce_lr, early_stopping])

model.save('correct_framing_model.h5')