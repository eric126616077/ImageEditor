import tkinter as tk
from tkinter import Scale, HORIZONTAL, filedialog  
from PIL import Image, ImageEnhance, ImageTk

# Initializing variables
img = None
original_img = None
adjust_img = None
temp_img = None
start_image = None
image_height = 0
image_width = 0
control = None



# Functions fields====================================================

def complete_crop(): 
    """save image and close the control window"""
    global original_img, adjust_img, control, temp_img, img

    original_img = temp_img.copy()
    adjust_img = original_img.copy()

    img = ImageTk.PhotoImage(adjust_img)
    panel.img = img
    panel.config(image=img)
    
    if control is not None:
        control.destroy()

    brightness_slider.set(1)
    contrast_slider.set(1)
    color_slider.set(1)
    sharpness_slider.set(1)

# crop function------------------------------------------------

def crop_image(left, top, right, bottom):
    global adjust_img, img, temp_img

    temp_img = adjust_img.copy()
    """using crop to cut the image"""
    temp_img = temp_img.crop((left, top, image_width - right, image_height - bottom))

    img = ImageTk.PhotoImage(temp_img)

    panel.config(image=img)

def control_window(w, h):
    global control
    control = tk.Toplevel(root)
    control.geometry("400x400")

    left_lb = tk.Label(control, text="left")
    left_lb.pack(anchor=tk.W, pady=5)

    left_scale = tk.Scale(control, from_=0, to=w, orient=tk.HORIZONTAL,
                          command=lambda x: crop_image(left_scale.get(),
                                                       top_scale.get(),
                                                       right_scale.get(),
                                                       bottom_scale.get()))
    left_scale.pack(anchor=tk.W, fill=tk.X)

    right_lb = tk.Label(control, text="right")
    right_lb.pack(anchor=tk.W, pady=5)

    right_scale = tk.Scale(control, from_=0, to=w, orient=tk.HORIZONTAL,
                          command=lambda x: crop_image(left_scale.get(),
                                                       top_scale.get(),
                                                       right_scale.get(),
                                                       bottom_scale.get()))
    right_scale.pack(anchor=tk.W, fill=tk.X)

    top_lb = tk.Label(control, text="top")
    top_lb.pack(anchor=tk.W, pady=5)

    top_scale = tk.Scale(control, from_=0, to=h, orient=tk.HORIZONTAL,
                          command=lambda x: crop_image(left_scale.get(),
                                                       top_scale.get(),
                                                       right_scale.get(),
                                                       bottom_scale.get()))
    top_scale.pack(anchor=tk.W, fill=tk.X)

    bottom_lb = tk.Label(control, text="bottom")
    bottom_lb.pack(anchor=tk.W, pady=5)

    bottom_scale = tk.Scale(control, from_=0, to=h, orient=tk.HORIZONTAL,
                            command=lambda x: crop_image(left_scale.get(),
                                                        top_scale.get(),
                                                        right_scale.get(),
                                                        bottom_scale.get()))
    bottom_scale.pack(anchor=tk.W, fill=tk.X)

    complete_button = tk.Button(control, text="Complete", command=complete_crop)
    complete_button.pack(anchor=tk.W, fill=tk.X, pady=20, padx=10)

def open_image():
    global img, panel, original_img, adjust_img, image_height, image_width, file_path, start_image
    file_path = filedialog.askopenfilename()
    if file_path:
        original_img = Image.open(file_path)
        start_image = original_img.copy()
        adjust_img = original_img.copy()
        img = ImageTk.PhotoImage(original_img)
        panel.img = img
        panel.config(image=img)

        image_height = img.height()
        image_width = img.width()

def save_image():
    global adjust_img
    if adjust_img is None:
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                             filetypes=[("JPEG", "*.jpg"),("PNG", "*.png"),("BMP", "*.bmp"),("All files", "*.*")])
    if file_path:
        adjust_img.save(file_path)


def adjust_image(val):
    global img, panel, original_img, adjust_img

    if original_img is None:
        return
    adjust_img = original_img.copy()



    # Using PIL ImageEnhance adjust Brightness
    enhancer = ImageEnhance.Brightness(adjust_img)
    adjust_img = enhancer.enhance(float(brightness_slider.get()))

    # Using PIL ImageEnhance adjust Contrast
    enhancer = ImageEnhance.Contrast(adjust_img)
    adjust_img = enhancer.enhance(float(contrast_slider.get()))

    # Using PIL ImageEnhance adjust Color
    enhancer = ImageEnhance.Color(adjust_img)
    adjust_img = enhancer.enhance(float(color_slider.get()))

    # Using PIL ImageEnhance adjust Sharpness
    enhancer = ImageEnhance.Sharpness(adjust_img)
    adjust_img = enhancer.enhance(float(sharpness_slider.get()))

    # transfer PIL image to useable Tkinter format
    img = ImageTk.PhotoImage(adjust_img)

    # display image on the windows
    panel.img = img
    panel.config(image=img)

# rotate function
def rotate_image(angle):
    global adjust_img, img, panel

    if adjust_img is None:
        return

    adjust_img = adjust_img.rotate(int(angle), fillcolor="white", expand=True)

    # Convert the adjusted PIL picture object to a format that Tkinter can use and display it
    img = ImageTk.PhotoImage(adjust_img)

    # display image in the windows
    panel.img = img
    panel.config(image=img)

# reset function
def reset_image():
    global img, panel, original_img, adjust_img, brightness_slider, contrast_slider, color_slider, sharpness_slider
    if original_img is None:
        return
    original_img = start_image.copy()
    adjust_img = original_img.copy()
    img = ImageTk.PhotoImage(adjust_img)
    brightness_slider.set(1)
    contrast_slider.set(1)
    color_slider.set(1)
    sharpness_slider.set(1)
    panel.img = img
    panel.config(image=img)

# create windows
root = tk.Tk()
root.geometry("800x400")    
root.title("Image Edit Master")



# create label to display image
img_frame = tk.Frame(root)
panel = tk.Label(img_frame, image=img)
panel.pack()

# create control frame
control_frame = tk.Frame(root,bd=1,relief="solid",highlightbackground="blue", highlightthickness=1)
# open and save function
open_button = tk.Button(control_frame, text="Open Image", command=open_image)
open_button.grid(row=0,column=0,columnspan=1)

save_button = tk.Button(control_frame, text="Save Image", command=save_image)
save_button.grid(row=0,column=4,columnspan=1)
# Create a Scale component as a slider to adjust brightness
brightness_slider = Scale(control_frame, from_=0.1, to=2, length=400, resolution=0.1,
                          orient=HORIZONTAL, label="Brightness",
                          command=adjust_image)
brightness_slider.set(1)
brightness_slider.grid(row=1,column=0,columnspan=5)

# Create a Scale component as a slider for adjusting contrast
contrast_slider = Scale(control_frame, from_=0.1, to=2, length=400, resolution=0.1,
                        orient=HORIZONTAL, label="Contrast",
                        command=adjust_image)
contrast_slider.set(1)
contrast_slider.grid(row=2,column=0,columnspan=5)

# Create a Scale component as a slider for adjusting color balance
color_slider = Scale(control_frame, from_=0.1, to=2, length=400, resolution=0.1,
                     orient=HORIZONTAL, label="Color",
                     command=adjust_image)
color_slider.set(1)
color_slider.grid(row=3,column=0,columnspan=5)

# Create a Scale component as a slider to adjust sharpness
sharpness_slider = Scale(control_frame, from_=0.1, to=2, length=400, resolution=0.1,
                         orient=HORIZONTAL, label="Sharpness",
                         command=adjust_image)
sharpness_slider.set(1)
sharpness_slider.grid(row=4,column=0,columnspan=5)

# rotate function
rotate_180_left_button = tk.Button(control_frame, text="Rotate 180° ", command=lambda: rotate_image(180))
rotate_180_left_button.grid(row=5,column=1)

rotate_90_left_button = tk.Button(control_frame, text="<<Rotate 90°", command=lambda: rotate_image(90))
rotate_90_left_button.grid(row=5,column=0)

rotate_90_right_button = tk.Button(control_frame, text="Rotate 90°>>", command=lambda: rotate_image(-90))
rotate_90_right_button.grid(row=5,column=2)

# crop button
crop_button = tk.Button(control_frame, text="Crop", 
                        command=lambda: control_window(w=image_width, h=image_height))
crop_button.grid(row=5,column=4)

# reset function
reset_button = tk.Button(control_frame, text="Reset Image", command=reset_image)
reset_button.grid(row=0,column=1,columnspan=2)

# Place img_frame and control_frame in the window

img_frame.pack(side="left", fill="y", expand="yes")
control_frame.pack(side="right", fill="y")

# Run the main loop of the window
root.mainloop()
