M E 369P - Team 4 - Short n' Clean 
Allen Hewson, Brenda Miltos, Marcie Legarde, Pranay Srivastava

This repository includes all of the files needed to produce a dataset to train a model to allow a user to play a game of rock paper scissors with a computer. The game includes an easy and a hard mode, where easy bases the computer hand off of random choice, and hard gets the computer to cheat.

Files
1) gather_data.py
    This file captures image data for use in training a model to recognize a hand playing rock paper scissors
2) edge_detection.py
    This file uses the images collected from gather_data.py and prepares new images to train the model using edge detection 
3) EdgeDetectionModelTraining.ipynb
    This file trains a model based on the images produced from edge_detection.py
4) dream_code.py
    This file creates the GUI for the game of rock paper scissors