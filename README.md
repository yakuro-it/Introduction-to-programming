# Secret Message Hider (Steganography Tool)
This is a light weight, graphical python application which is used to hide text messages inside Images (PNG) using Least Significant Bit (LSB) steganography.This project demonstrates basic data techniques where we can hide the messages in the images without alter or making visible changes to the images of the owner or the host of the image.

# How it works
The tool we used is Least Significant Bit(LSB) insertion method. In which every pixel in a digital image is made up of three color channel which is red,green and Blue (RGB).
Every color is represnted by 8 bits. The LSB technique replaces the last bits of the images of each color with your single bit of secret message that you want to hide.
Because the changes is done in bit this makes it hard for the human eye to notice it  annd also it mantains the image quality.

# Requirements
You will need to install pillow library
[ pip install Pillow]

# Features
## Simple Gui
### Encrypted Data Hiding
#### Automated Markers

# Appendix Images:
<img width="810" height="591" alt="image" src="https://github.com/user-attachments/assets/799e7a78-185c-47ce-8b72-1b56a19f5c9e" />
<img width="805" height="587" alt="image" src="https://github.com/user-attachments/assets/ab1eb4f8-6e48-4df7-820a-36339a1bdac5" />
<img width="365" height="176" alt="image" src="https://github.com/user-attachments/assets/21d63e8c-e6a3-4cfe-96b2-5bec6fca218f" />
<img width="806" height="592" alt="image" src="https://github.com/user-attachments/assets/dd7326b0-e79d-4876-bc3f-704259b282ad" />

