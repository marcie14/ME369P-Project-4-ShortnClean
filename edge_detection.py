from asyncore import write
import cv2
import os
folders = ["rock", "paper", "scissors", "none"]
for folder in folders:
  dir = f"C:/Users/daich/OneDrive/Documents/ME 369P RPS Project/{folder}"
  new_dir = f"C:/Users/daich/OneDrive/Documents/ME 369P RPS Project/{folder}edge"
  for item in os.listdir(dir):
      if item.endswith("jpg"):
        img = cv2.imread(os.path.join(dir, item))
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # The image needs to be blurred to improve edge detection
        img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)
        # Get Sobel X and Y edge detection
        sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X
        cv2.imwrite(os.path.join(dir, item), sobelxy)