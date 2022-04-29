from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import tensorflow as tf
keras = tf.keras
import numpy as np
from random import choice
import time
import os  

# Create folder where we can capture player's move 

Datos = 'Player Move'
if not os.path.exists(Datos):
    print('Carpeta creada ', Datos)
    os.makedirs(Datos)

# Number of photos taken 
photo_of_move = 0

def visualizar():
    global cap
    if cap is not None:
        ret, frame = cap.read()
        if ret == True:
            frame = imutils.resize(frame, width=640)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image = img
            lblVideo.after(10, visualizar)
        else:
            lblVideo.image = ""
            cap.release()

def game():
    global cap 
    model = keras.models.load_model("rpsedge2.h5")

    CLASS_MAP =  {
        0: "rock",
        1: "paper",
        2: "scissors",
        3: "none"
    }

    def mapper(val):
        return CLASS_MAP[val]

    # SET THE COUNTDOWN TIMER
    # for simplicity we set it to 5
    # We can also take this as input
    TIMER = int(5)

    # Open the camera
    cap = cv2.VideoCapture(0)
    x1, y1 = 25, 25
    x2, y2 = 300, 300 

    while True:

        # Read and display frame 
        ret, frame = cap.read()
        # cv2.imshow('a', img)  
        if not ret:
            continue
        
        imAux = frame.copy()
        # Check for the pressed key 
        # Waits 125 miliseconds to see if someone pressed any key 
        # k = cv2.waitKey(125)

        # rectangle for user to play
        cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)

        objeto = imAux[y1:y2, x1:x2]
        objeto = imutils.resize (objeto, width = 38)
        
        # extract the region of image within the user rectangle
        player_move = frame[25:300, 25:300]
        img = cv2.cvtColor(player_move, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img_blur = cv2.GaussianBlur(img, (3,3), 0)
        sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
        # predict the move made
        pred = model.predict(np.array([sobelxy]))
        player_move_code = np.argmax(pred[0])
        player_move_name = mapper(player_move_code)
        # print(user_move_name)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Your Move: " + player_move_name, (5, 25), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
       
        # set the key for the countdown to begin, here we set it as s 
        k = cv2.waitKey(10)
        if k == ord('s'):
            prev = time.time()

            while TIMER >=0:
                ret, img = cap.read()

                # Display countdown on each frame 
                # Specify the font and draw the coundown 
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(TIMER),
                            (200, 250), font,
                            7, (0, 255, 255),
                            4, cv2.LINE_AA)
                cv2.imshow('Rock Paper Scissors', img)
                cv2.waitKey(10)

                # Current Time 
                cur = time.time()

                # Update and keep track of Countdown
                # if time elapsed is one second
                # than decrease the counter
                if cur-prev >= 1:
                    prev = cur
                    TIMER = TIMER-1

            else: 
                ret, frame = cap.read()

                # Display the clicked frame for 2
                # sec.You can increase time in
                # waitKey also
                # cv2.imshow('a', img)
                cv2.imshow('Rock Paper Scissors', frame)
 
                # time for which image displayed
                cv2.waitKey(2000)
 
                # Save the frame
                # cv2.imwrite('camera.jpg', frame)
                # This will capture the image that was just in the box 
                cv2.imwrite(Datos+'/objeto_{}.jpg'.format(photo_of_move),objeto)
 
                # HERE we can reset the Countdown timer
                # if we want more Capture without closing
                # the camera

                TIMER = 5



        elif k == ord('q'):
            break
        cv2.imshow("Rock Paper Scissors", frame)

    cap.release()
    cv2.destroyAllWindows()



def iniciar():
    global cap 
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # visualizar()
    game()

def finalizar():
    global cap
    cap.release()

cap = None 
root = Tk()

btnIniciar = Button(root, text="Iniciar", width=45, command=iniciar)
btnIniciar.grid(column=0, row=0, padx=5, pady=5)

btnFinalizar = Button(root, text="Finalizar", width=45, command=finalizar)
btnFinalizar.grid(column=1, row=0, padx=5, pady=5)

lblVideo = Label(root)
lblVideo.grid(column=0, row=1, columnspan=2)

root.mainloop()
