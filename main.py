import cv2
import numpy as np
from datetime import datetime


net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]


cap = cv2.VideoCapture(0)


working_zone_top_left = (100, 100)
working_zone_bottom_right = (500, 500)


def is_inside_working_zone(bbox):
    x, y, w, h = bbox
    obj_center_x = x + w // 2
    obj_center_y = y + h // 2

    return (working_zone_top_left[0] <= obj_center_x <= working_zone_bottom_right[0] and
            working_zone_top_left[1] <= obj_center_y <= working_zone_bottom_right[1])


def get_objects(frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    result_boxes = []
    for i in range(len(boxes)):
        if i in indexes:
            result_boxes.append(boxes[i])
    return result_boxes


while True:
    ret, frame = cap.read()
    if not ret:
        break

    depth_frame = np.zeros(frame.shape[:2], dtype=np.float32)
    objects = get_objects(frame)

    for (x, y, w, h) in objects:
        min_depth = np.min(depth_frame[y:y + h, x:x + w])
        max_depth = np.max(depth_frame[y:y + h, x:x + w])
        time_appeared = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        inside_working_zone = is_inside_working_zone((x, y, w, h))
        if inside_working_zone:
            print(
                f"Обьект в зоне: {w}, {h}, {min_depth}, {max_depth}, {time_appeared}")
        else:
            print(
                f"Обьект вне зоны: {w}, {h}, {min_depth}, {max_depth}, {time_appeared}")

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0) if inside_working_zone else (0, 0, 255), 2)

    cv2.rectangle(frame, working_zone_top_left, working_zone_bottom_right, (255, 0, 0), 2)

    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
