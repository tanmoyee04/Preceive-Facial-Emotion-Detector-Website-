import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model


prototxt_path='E:/F drive docs/tushi/TUSHI/sem/deploy.prototxt.txt'
caffemodel_path='E:/F drive docs/tushi/TUSHI/sem/weights.caffemodel'

print("Loading models...")
face_model = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
emotion_model=load_model("F:/anaconda3/Workplace/models/fer2013_mini_XCEPTION.102-0.66.hdf5",compile=False)
print("Done")


target_size=emotion_model.input_shape[1:3]
emotion_labels={0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}
color={0: (0,0,255), 1: (0,0,100), 2: (230,200,0), 3: (0,255,0), 4: (100,0,0), 5: (0,255,255), 6: (255,0,255)}


def detect_emotion(image):
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image=cv2.resize(image,(target_size))
    input1=np.float32(image)
    input1=input1/255.0
    input1=input1-0.5
    input1=input1*2.0
    input1=np.expand_dims(input1,0)
    input1=np.expand_dims(input1,-1)
    output=emotion_model.predict(input1)
    return np.argmax(output)


def process(image):
    (h, w) = image.shape[:2]
    output=image.copy()
    blob = cv2.dnn.blobFromImage(cv2.resize(image.copy(), (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_model.setInput(blob)
    detections = face_model.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence>0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            frame=image[startY:endY, startX:endX]
            if frame.shape[0]<30 or frame.shape[1]<30:
                break
            emotion=detect_emotion(frame)
            text = emotion_labels[emotion]
            y = startY - 10 if startY - 10 > 10 else startY + 10
            res=cv2.rectangle(output, (startX, startY), (endX, endY),color[emotion], 2)
            cv2.putText(output, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color[emotion], 2)
    return output


def real_time_feed(video,outpath):
    cap=cv2.VideoCapture(video)
    res,frame=cap.read()
    h,w=frame.shape[:2]
    fourcc=cv2.VideoWriter_fourcc(*"XVID")
    out=cv2.VideoWriter(outpath,fourcc,20.0,(w,h))
    print("Press 'a' to stop...")
    while(True):
        res,frame=cap.read()
        if frame is None:
            break
        output=process(frame)
        out.write(output)
        #cv2.imshow("Emotion detection", output)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            break
    cap.release()
    out.release()
    key=cv2.waitKey(1000)
    cv2.destroyAllWindows()

def main(in_loc, out_loc, idx):
    if idx:
        image=cv2.imread(in_loc)
        output=process(image)
        cv2.imwrite(out_loc,output)
    else:
        real_time_feed(in_loc,out_loc)