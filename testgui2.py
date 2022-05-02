<<<<<<< HEAD
'''
M E 369P - Team 4 - Short n' Clean 
Allen Hewson, Brenda Miltos, Marcie Legarde, Pranay Srivastava

GUI File:
    This file creates the GUI for the game of rock paper scissors
    Much of this file was extrapolated from https://pythonistaplanet.com/rock-paper-scissors-game-using-python-tkinter/
    Changes made for this project: 
        -Winner/Loser Comments
        -Not-So-Random computer hand selection
        -Incorporating OpenCV for Main File
'''

# importing used libraries
from sre_parse import State
import tkinter as tk
import random
import numpy as np
from PIL import Image, ImageTk
import cv2
import tensorflow as tf
keras = tf.keras

model = keras.models.load_model("rpsedge2.h5")

# importing referenced files
#from project_modelCV import *
#from project_main import *
#from recognize_edge import * # importing modelCV file

CLASS_MAP =  {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
}

def mapper(val):
    return CLASS_MAP[val]

# creating game window
window = tk.Tk()
#window.geometry("400x400")
window.title("Rock Paper Scissors Game") 

# from test GUI
frame=np.random.randint(0,255,[100,100,3],dtype='uint8')
img = ImageTk.PhotoImage(Image.fromarray(frame))

panel_image=tk.Label(window) #,image=img)
panel_image.grid(row=0,column=0,columnspan=3,pady=1,padx=10)

message="You can see some \nclassification results \nhere after you add some intelligent  \nadditional code to your combined and handy \n tkinter & CV2 solution!"
panel_text=tk.Label(window,text=message)
panel_text.grid(row=1,column=1,pady=1,padx=10)

# end from test GUI

global cam

def camera():
    global frame
    global cam
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        # update image to tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_update = ImageTk.PhotoImage(Image.fromarray(frame))
        panel_image.configure(image=img_update)
        panel_image.image=img_update
        panel_image.update()

        # rectangle for user to play
        cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)
    
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

        if not ret:
            print("failed to grab frame")
            break

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")

            cam.release()
            cv2.destroyAllWindows()
            break
        cv2.imshow("Rock Paper Scissors", frame)

def stop():
    global cam
    cam.release()
    cv2.destroyAllWindows()
    print("Stopped!")

handle_height=10
handle_1=tk.Button(window,text="Start",command=camera,height=5,width=20)
handle_1.grid(row=1,column=0,pady=10,padx=10)
handle_1.config(height=1*handle_height,width=20)

handle_height=10
handle_1=tk.Button(window,text="Stop",command=stop,height=5,width=20)
handle_1.grid(row=1,column=2,pady=10,padx=10)
handle_1.config(height=1*handle_height,width=20)

window.mainloop()

# initializing global variables
USER_SCORE = 0      # keeps track of user's score for RPS game
COMP_SCORE = 0      # keeps track of computer's score for RPS game
USER_CHOICE = ""#player_move_name    # initialize user choice variable using variable from recognize_edge.py
COMP_CHOICE = ""    # initialize computer choice variable


def choice_to_number(choice):
    rps = {'rock':0,'paper':1,'scissors':2}
    return rps[choice]
def number_to_choice(number):
    rps={0:'rock',1:'paper',2:'scissors'}
    return rps[number]

def random_computer_choice():
    return random.choice(['rock','paper','scissors']) 

# random win statement
def random_win_statement():
    r = random.randint(1,5)
    match r:
        case 1:
            statement = 'That was all luck...'
        case 2:
            statement = 'You got lucky'
        case 3:
            statement = 'I let you win that one...'
        case 4:
            statement = 'Your awkward hands were distracting me...'
        case 5:
            statement = 'You cheated!'
    return statement

# random lose statement
def random_lose_statement():
    r = random.randint(1,5)
    match r:
        case 1:
            statement = 'Ha I dont even have hands and I won'
        case 2:
            statement = 'Like playing against a baby'
        case 3:
            statement = 'You kinda suck'
        case 4:
            statement = 'Do you even know how to play?'
        case 5:
            statement = 'How many times do I have to tell you? Paper beats Rock beats Scissors beats Paper!'
    return statement

# determine winner of game
def result(human_choice,comp_choice):
    # declare variables
    global USER_SCORE
    global COMP_SCORE
    user=choice_to_number(human_choice)
    comp=choice_to_number(comp_choice)
    
    if(user==comp):
        print("Tie")
    
    elif((user-comp)%3==1):
        print("You win")

        # getting random win statement
        s = random_win_statement()
        print(s)
        USER_SCORE+=1
    
    else:
        print("Comp wins")
        # getting random lose statement
        s = random_lose_statement()
        print(s)
        COMP_SCORE+=1

    # adjusting text on window    
    text_area = tk.Text(master=window,height=12,width=30,bg="#FFFF99")
    text_area.grid(column=0,row=4)
    answer = "Your Choice: {uc} \nComputer's Choice : {cc} \n Your Score : {u} \n Computer Score : {c} ".format(uc=USER_CHOICE,cc=COMP_CHOICE,u=USER_SCORE,c=COMP_SCORE)    
    text_area.insert(tk.END,answer)
    
def rock():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='rock'
    # modified code to cheat
    #COMP_CHOICE=random_computer_choice()
    COMP_CHOICE='paper'
    result(USER_CHOICE,COMP_CHOICE)
def paper():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='paper'
    # modified code to cheat
    #COMP_CHOICE=random_computer_choice()
    COMP_CHOICE='scissors'
    result(USER_CHOICE,COMP_CHOICE)
def scissor():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='scissors'
    # modified code to cheat
    #COMP_CHOICE=random_computer_choice() 
    COMP_CHOICE='rock'
    result(USER_CHOICE,COMP_CHOICE)
    
# commenting out button functions
#button1 = tk.Button(text="       Rock       ",bg="skyblue",command=rock)
#button1.grid(column=0,row=1)
#button2 = tk.Button(text="       Paper      ",bg="pink",command=paper)
#button2.grid(column=0,row=2)
#button3 = tk.Button(text="      Scissors     ",bg="lightgreen",command=scissors)
#button3.grid(column=0,row=3)

=======
'''
M E 369P - Team 4 - Short n' Clean 
Allen Hewson, Brenda Miltos, Marcie Legarde, Pranay Srivastava

GUI File:
    This file creates the GUI for the game of rock paper scissors
    Much of this file was extrapolated from https://pythonistaplanet.com/rock-paper-scissors-game-using-python-tkinter/
    Changes made for this project: 
        -Winner/Loser Comments
        -Not-So-Random computer hand selection
        -Incorporating OpenCV for Main File

FUSED RECOGNIZED_EDGE AND PROJECT_GUI AND RESOURCE FROM INTERNET
'''

# importing used libraries
from sre_parse import State
import tkinter as tk
import random
import numpy as np
from PIL import Image, ImageTk
import cv2
import tensorflow as tf
keras = tf.keras

model = keras.models.load_model("rpsedge2.h5")

# importing referenced files
#from project_modelCV import *
#from project_main import *
#from recognize_edge import * # importing modelCV file

CLASS_MAP =  {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
}

def mapper(val):
    return CLASS_MAP[val]

# creating game window
window = tk.Tk()
#window.geometry("400x400")
window.title("Rock Paper Scissors Game") 

# from test GUI
frame=np.random.randint(0,255,[100,100,3],dtype='uint8')
img = ImageTk.PhotoImage(Image.fromarray(frame))

panel_img = tk.Label(window) #,image=img)
panel_img.grid(row=0,column=0,columnspan=3,pady=1,padx=10)

message="Press Play to Begin!"
panel_text=tk.Label(window,text=message)
panel_text.grid(row=1,column=1,pady=1,padx=10)

# end from test GUI

global cam

def camera():
    global frame
    global cam
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()

        # rectangle for user to play
        cv2.rectangle(frame, (25, 25), (300, 300), (255, 255, 255), 2)
    
        # extract the region of image within the user rectangle
        player_move = frame[25:300, 25:300]
        panel_img = cv2.cvtColor(player_move, cv2.COLOR_BGR2GRAY)
        panel_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        panel_img = cv2.resize(img, (224, 224))
        img_blur = cv2.GaussianBlur(img, (3,3), 0)
        sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
        img_update = ImageTk.PhotoImage(Image.fromarray(panel_img))
        panel_img.configure(image=img_update)
        panel_img.image=img_update
        panel_img.update()

        # predict the move made
        pred = model.predict(np.array([sobelxy]))
        player_move_code = np.argmax(pred[0])
        player_move_name = mapper(player_move_code)
        #print(user_move_name)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "Your Move: " + player_move_name, (5, 25), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

        if not ret:
            print("failed to grab frame")
            break

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")

            cam.release()
            cv2.destroyAllWindows()
            break
        cv2.imshow("Rock Paper Scissors", frame)

def stop():
    global cam
    cam.release()
    cv2.destroyAllWindows()
    print("Stopped!")


# start button
handle_height=10
handle_1=tk.Button(window,text="Play",command=camera,height=5,width=20)
handle_1.grid(row=1,column=0,pady=10,padx=10)
handle_1.config(height=1*handle_height,width=20)

# stop button
handle_height=10
handle_1=tk.Button(window,text="Exit",command=stop,height=5,width=20)
handle_1.grid(row=1,column=2,pady=10,padx=10)
handle_1.config(height=1*handle_height,width=20)

window.mainloop()

# initializing global variables
USER_SCORE = 0      # keeps track of user's score for RPS game
COMP_SCORE = 0      # keeps track of computer's score for RPS game
USER_CHOICE = ""#player_move_name    # initialize user choice variable using variable from recognize_edge.py
COMP_CHOICE = ""    # initialize computer choice variable


def choice_to_number(choice):
    rps = {'rock':0,'paper':1,'scissors':2}
    return rps[choice]
def number_to_choice(number):
    rps={0:'rock',1:'paper',2:'scissors'}
    return rps[number]

def random_computer_choice():
    return random.choice(['rock','paper','scissors']) 

# random win statement
def random_win_statement():
    r = random.randint(1,5)
    match r:
        case 1:
            statement = 'That was all luck...'
        case 2:
            statement = 'You got lucky'
        case 3:
            statement = 'I let you win that one...'
        case 4:
            statement = 'Your awkward hands were distracting me...'
        case 5:
            statement = 'You cheated!'
    return statement

# random lose statement
def random_lose_statement():
    r = random.randint(1,5)
    match r:
        case 1:
            statement = 'Ha I dont even have hands and I won'
        case 2:
            statement = 'Like playing against a baby'
        case 3:
            statement = 'You kinda suck'
        case 4:
            statement = 'Do you even know how to play?'
        case 5:
            statement = 'How many times do I have to tell you? Paper beats Rock beats Scissors beats Paper!'
    return statement

# determine winner of game
def result(human_choice,comp_choice):
    # declare variables
    global USER_SCORE
    global COMP_SCORE
    user=choice_to_number(human_choice)
    comp=choice_to_number(comp_choice)
    
    if(user==comp):
        print("Tie")
    
    elif((user-comp)%3==1):
        print("You win")

        # getting random win statement
        s = random_win_statement()
        print(s)
        USER_SCORE+=1
    
    else:
        print("Comp wins")
        # getting random lose statement
        s = random_lose_statement()
        print(s)
        COMP_SCORE+=1

    # adjusting text on window    
    text_area = tk.Text(master=window,height=12,width=30,bg="#FFFF99")
    text_area.grid(column=0,row=4)
    answer = "Your Choice: {uc} \nComputer's Choice : {cc} \n Your Score : {u} \n Computer Score : {c} ".format(uc=USER_CHOICE,cc=COMP_CHOICE,u=USER_SCORE,c=COMP_SCORE)    
    text_area.insert(tk.END,answer)
    
def rock():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='rock'
    # modified code to cheat
    #COMP_CHOICE=random_computer_choice()
    COMP_CHOICE='paper'
    result(USER_CHOICE,COMP_CHOICE)
def paper():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='paper'
    # modified code to cheat
    #COMP_CHOICE=random_computer_choice()
    COMP_CHOICE='scissors'
    result(USER_CHOICE,COMP_CHOICE)
def scissor():
    global USER_CHOICE
    global COMP_CHOICE
    USER_CHOICE='scissors'
    # modified code to cheat
    #COMP_CHOICE=random_computer_choice() 
    COMP_CHOICE='rock'
    result(USER_CHOICE,COMP_CHOICE)
    
# commenting out button functions
#button1 = tk.Button(text="       Rock       ",bg="skyblue",command=rock)
#button1.grid(column=0,row=1)
#button2 = tk.Button(text="       Paper      ",bg="pink",command=paper)
#button2.grid(column=0,row=2)
#button3 = tk.Button(text="      Scissors     ",bg="lightgreen",command=scissors)
#button3.grid(column=0,row=3)

>>>>>>> 3ab2d71e8d837d9a0a620ad98009474f188b0392
#window.mainloop()