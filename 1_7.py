import tensorflow as tf

dataset_path = "C:/Users/gorky/Downloads/artificial_intelligence"
input_shape = (1024, 1024, 3)

batch_size = 32
epochs = 10

class_names = ['negative', 'positive']

train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset='training',
    seed=123,
    image_size=input_shape[:2],
    batch_size=batch_size,
    class_names=class_names
)

validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset='validation',
    seed=123,
    image_size=input_shape[:2],
    batch_size=batch_size,
    class_names=class_names
)


preprocess_input = tf.keras.applications.efficientnet.preprocess_input
train_dataset = train_dataset.map(lambda x, y: (preprocess_input(x), y))
validation_dataset = validation_dataset.map(lambda x, y: (preprocess_input(x), y))


data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip('horizontal'),
    tf.keras.layers.RandomRotation(0.1)
])


base_model = tf.keras.applications.EfficientNetB0(input_shape=input_shape, include_top=False, weights='imagenet')
base_model.trainable = False

model = tf.keras.Sequential([
    data_augmentation,
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-6)
early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=epochs,
    callbacks=[reduce_lr, early_stopping]
)


loss, accuracy = model.evaluate(validation_dataset)
print(f'Validation Loss: {loss:.4f}, Validation Accuracy: {accuracy:.4f}')

model.save('model.h5')
