import tkinter as tk
from tkinter import filedialog, messagebox
import os
import email
import pickle

from numpy import float32

from util import extract_email_content
from util import predict_url
from util import predict_email

file_path = None


def set_file_path(file):
    file_path = file


def is_eml_file(file):
    # Check if the file extension is ".eml"
    return file.lower().endswith(".eml")


def browse_file():
    # Asks for file input from user
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        if is_eml_file(file_path):
            # Validate file for email content
            fileName = file_path.split("/")
            label.config(text="Selected File: " + fileName.pop(), fg="green")
            set_file_path(file_path)
        else:
            # Return error if file is not an .eml file
            label.config(text="Selected File is not a .eml file, please try again", fg="red")


def utility():
    with open(file_path, 'rb') as file:
        eml_content = file.read()
    message = email.message_from_bytes(eml_content)

    text, urls = extract_email_content(message)
    # Checks if there are any urls, otherwise check only email text
    if urls:
        uFile = open('phishing_url_detection_random_forest.pkl', 'rb')
        url_model = pickle.load(uFile)

        sFile = open('url_scaler.pkl', 'rb')
        scaler = pickle.load(sFile)

        eFile = open('email_detection_logistic_regression.pkl', 'rb')
        email_model = pickle.load(eFile)

        vFile = open('email_vectorizer.pkl', 'rb')
        vectorizer = pickle.load(vFile)

        url_pred = predict_url(urls, url_model, scaler)
        email_pred = predict_email(text, email_model, vectorizer)

        counter = 0
        if 1 in url_pred:
            counter += 1
        pct_url = 100 * counter / len(url_pred)
        url_message = "URLs" + str(pct_url) + "%: Unlikely Phishing"
       
        if pct_url > 50:
            url_message = "URLs" + str(pct_url) + "%: Likely Phishing"
        email_message = "Text: Unlikely Phishing"
        
        if email_pred[0] == 1:
            email_message = "Text: Likely Phishing"
        show_message(url_message, email_message)
        # label.config(url_pred)
        # label.config(email_pred)

    else:
        eFile = open('email_detection_logistic_regression.pkl', 'rb')
        email_model = pickle.load(eFile)

        vFile = open('email_vectorizer.pkl', 'rb')
        vectorizer = pickle.load(vFile)

        email_pred = predict_email(text, email_model, vectorizer)

        email_message = "Text: Unlikely Phishing"
        if email_pred[0] == 1:
            email_message = "Text: Likely Phishing"
        show_message_email_only(email_message)
        # label.config(email_pred)

def show_message(url_message, email_message):
    messagebox.showinfo("Results", url_message + "\n" + email_message)

def show_message_email_only(email_message):
    messagebox.showinfo("Results", email_message)
    
# Create the main window
root = tk.Tk()
root.title("Phishing File Checker")
root.tk_setPalette(background='#2E2E2E', foreground='#FFFFFF', selectBackground='#4A90E2', selectForeground='#FFFFFF')
root.geometry('1200x800')

if root.winfo_width() > 1200:
    root.geometry('1200x800')

# Create a label to display the selected file path
label = tk.Label(root, text="Selected File: None")
label.pack(pady=100)

# Create a button to browse for a file
browse_button = tk.Button(root, text="Browse", command=browse_file, width=15, height=5)
browse_button.pack(pady=20)

# Check a button to check phishing
check_button = tk.Button(root, text="Phish Check", command=utility, width=15, height=5)
check_button.pack(pady=20)

# Run the main loop
root.mainloop()
