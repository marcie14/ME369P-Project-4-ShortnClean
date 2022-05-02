from time import sleep
import tkinter
from tkinter import ttk
from tkinter import Tk, Text
import numpy as np
from PIL import Image, ImageTk
import cv2
from sqlalchemy import true
import tensorflow as tf

keras = tf.keras

model = keras.models.load_model("rpsedge2.h5")

window=tkinter.Tk()
window.title("Rock Paper Scissors Game")

frame=np.random.randint(0,255,[100,100,3],dtype='uint8')
img = ImageTk.PhotoImage(Image.fromarray(frame))

panel_image=tkinter.Label(window) #,image=img)
panel_image.grid(row=0,column=0,columnspan=3,pady=1,padx=10)

message = "GAME RULES:\n Here, we play Rock, Paper, Scissors, SHOOT.\n Play your hand ON SHOOT.\nPress Play to begin.\nRe-press Play to restart."
panel_text=tkinter.Label(window,text=message)
panel_text.grid(row=1,column=1,pady=1,padx=10)

font = cv2.FONT_HERSHEY_SIMPLEX

global cam

CLASS_MAP =  {
	0: "rock",
	1: "paper",
	2: "scissors",
	3: "none"
}

def mapper(val):
	return CLASS_MAP[val]

def camera():
	global frame
	global cam
	cam = cv2.VideoCapture(0)

	text = Text(window, height = 20)
	#text.pack()
	text.insert('1.0', 'ROCK')
	#text.insert('2.0', "PAPER")
	#text.insert('3.0', "SCISSORS")

	while True:
		ret, frame = cam.read()
		if not ret:
			print("failed to grab frame")
			break
		
		# rectangle to detect player move
		cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)
		
		# Update the image to tkinter...
		frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		img_update = ImageTk.PhotoImage(Image.fromarray(frame))
		panel_image.configure(image=img_update)
		panel_image.image=img_update
		panel_image.update()

		# extracting region of image within rectangle
		player_move = frame[25:300, 25:300]
		rect = cv2.cvtColor(player_move, cv2.COLOR_BGR2RGB)
		#rect = cv2.cvtColor(rect, cv2.COLOR_BGR2RGB)
		rect = cv2.resize(rect, (224, 224))
		rect_blur = cv2.GaussianBlur(rect, (3,3), 0)
		sobelxy = cv2.Sobel(src=rect_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)

		# predict the move made
		pred = model.predict(np.array([sobelxy]))
		player_move_code = np.argmax(pred[0])
		player_move_name = mapper(player_move_code)

		cv2.putText(frame, "Your Move: " + player_move_name, (5, 25), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
		k = cv2.waitKey(10)
		if k == ord('q'):
			break
		cv2.imshow("Rock Paper Scissors", frame)
		

handle_height=10
handle_1=tkinter.Button(window,text="Play",command=camera,height=5,width=20)
handle_1.grid(row=1,column=0,pady=10,padx=10)
handle_1.config(height=1*handle_height,width=20)

#handle_height=10
#handle_1=tkinter.Button(window,text="Stop",command=stop,height=5,width=20)
#handle_1.grid(row=1,column=2,pady=10,padx=10)
#handle_1.config(height=1*handle_height,width=20)

window.mainloop()