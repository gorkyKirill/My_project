import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras import EfficientNetB0
from tensorflow.keras import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.regularizers import l2
import cv2

train_dir = 'C:/Users/gorky/Downloads/artificial_intelligence'
val_dir = 'C:/Users/gorky/Downloads/artificial_intelligence'
test_dir = 'C:/Users/gorky/Downloads/artificial_intelligence'

img_width, img_height = 224, 224
num_classes = 2

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges

train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=preprocess_image,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    preprocessing_function=preprocess_image,
    rescale=1. / 255
)

test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_width, img_height),
    batch_size=32,
    class_mode='categorical'
)

base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 1))
base_model.trainable = True


for layer in base_model.layers[:100]:
    layer.trainable = True

model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu', kernel_regularizer=l2(0.01)),
    Dropout(0.5),
    Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=1e-6)
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

model.fit(train_generator,
          epochs=50,
          validation_data=val_generator,
          callbacks=[reduce_lr, early_stopping])

test_loss, test_acc = model.evaluate(test_generator)
print('Test accuracy:', test_acc)
model.save('3_4_model.h5')