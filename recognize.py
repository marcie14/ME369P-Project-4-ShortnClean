import tensorflow as tf
keras = tf.keras
import cv2
import numpy as np
from random import choice

model = keras.models.load_model("rps.h5")


CLASS_MAP =  {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
}

def mapper(val):
    return CLASS_MAP[val]


cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # rectangle for user to play
    cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)
    
    # extract the region of image within the user rectangle
    player_move = frame[25:300, 25:300]
    img = cv2.cvtColor(player_move, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))

    # predict the move made
    pred = model.predict(np.array([img]))
    player_move_code = np.argmax(pred[0])
    player_move_name = mapper(player_move_code)
    # print(user_move_name)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Your Move: " + player_move_name, (5, 25), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
    cv2.imshow("Rock Paper Scissors", frame)
cap.release()
cv2.destroyAllWindows()