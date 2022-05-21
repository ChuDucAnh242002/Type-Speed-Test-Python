"""
    Author : Chu Duc Anh
    Github : https://github.com/ChuDucAnh242002
    Inspired by Speed Typing Test in Python of NeuralNine: https://www.youtube.com/watch?v=quBb--IJPPc&t=14s
    A program that show the your typing speed by type a test
"""

from tkinter import *
import time
import threading
import random

class TypeSpeedGUI:

    """ 
        Constructor
        The initial data of the main window
    """
    def __init__(self):
        # The main window
        self.root = Tk()
        self.root.title("10 Fast Finger by Duc Anh")
        self.root.geometry("1200x400")

        # Create random text
        self.text = open("text.txt", "r").read().split("\n")
        self.random_text = random.choice(self.text)
        self.text_list = self.random_text.split()

        # Frame
        self.frame = Frame(self.root)
        
        # To calculate the speed in word per minute and accuracy
        self.wpm = 0
        self.counter =0
        self.accuracy = 100
        self.char_count = 0
        self.red_char = 0
        
        
        # Track the current word and letter
        self.track = 0
        self.track_words = 0
        self.red = False
        self.cur_word = ""

        # Text labels
        self.text_label = Label(self.frame, text= self.random_text, font=("Helvetica", 18))
        self.text_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        # User input entry
        self.input_entry = Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start_word)
        
        # Label show the speed and accuracy
        self.speed_label = Label(self.frame, text= f"{self.wpm:.2f} WPM\n{self.accuracy:.2f}% accuracy", font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        # Reset button
        self.reset_button = Button(self.frame, text="Reset", command = self.reset, font=("Helvetica", 18))
        self.reset_button.grid(row=3, column=0, padx=5, pady=10)

        # Quit button
        self.quit_button = Button(self.frame, text= "Quit", command = self.quit, font=("Helvetica", 18))
        self.quit_button.grid(row=3, column=1, padx=5, pady=10)

        # Frame
        self.frame.pack( expand=True)
        self.frame.bind("<Leave>", self.quit)
    
        self.running = False

        self.root.mainloop()


    """
        When user start typing, it will start the time clock and calculate the speed
        @param: event, Key Press event from user key board
    """
    def start_word(self, event):

        # If Key Pressed is F5 then reset the text word
        if event.keycode == 116:
            self.reset()
            return

        # Start the timer
        if not self.running:
            if not event.keycode in [13, 16, 17, 18, 32]:
                self.running = True
                t = threading.Thread(target= self.time_thread)
                t.start()
        
        # Tracking letter
        if self.text_list[0].startswith(self.input_entry.get()) and event.keycode not in [13, 16, 17, 18, 32]:
            # If Back space the track letter also go back
            if event.keycode == 8 and self.input_entry.get() :
                if self.red == True:
                    self.red = False
                    return
                self.track -= 1
                self.track_words -= 1
            # If none Back space then the track moves forward
            elif event.keycode != 8 and self.input_entry.get() :
                self.track += 1
                self.track_words += 1
        
        # Count the characters
        self.char_count += 1

        # If the text is wrong, the entry will change to red
        if not self.text_list[0].startswith(self.input_entry.get()) and event.keycode != 32:
            self.red_char += 1
            self.red = True
            self.input_entry.config(fg="red")

        # If text is correct, the entry word will be black
        else:
            self.input_entry.config(fg="black")
           
        # Calculate accurracy
        self.accuracy = (1 - self.red_char/ self.char_count)*100

        # If Key press is space, delete the entry and start new word
        if event.keycode == 32:
            self.cur_word = self.text_list[0]
            count = 0

            # If the word typed is correct then move it out the text list
            if self.input_entry.get().startswith(self.cur_word) and self.track_words == len(self.cur_word):
                self.text_list.remove(self.cur_word)
                count = 0
            
            # If the word type is not correct, just delete the entry
            elif count == 0 :
                self.track -=  (self.track_words + 1)
                count = 1

            self.track += 1
            self.track_words = 0
            self.input_entry.delete(0, END)

        # Underline the tracking letter
        self.text_label.config(underline= self.track)

        # If the text list is empty, close the input entry
        if self.text_list == [] or self.text_list == None:
            self.running = False
            self.input_entry.config( state= 'disable')

    """
        The original tutorial walkthrough and more edited functions 
        Change by replace start_word with start in the input_entry binding in the constructor
        @param: event, Key Press event from user key board
    """
    def start(self, event):

        if event.keycode == 116:
            self.reset()
            return
        
        if not self.running:
            if not event.keycode in [13, 16, 17, 18, 32]:
                self.running = True
                t = threading.Thread(target= self.time_thread)
                t.start()

        self.char_count += 1

        if not self.text_label.cget('text').startswith(self.input_entry.get()) :
            self.red_char += 1
            self.input_entry.configure(fg="red")

        else:
            self.input_entry.configure(fg="black")

        self.accuracy = (1 - self.red_char/ self.char_count)*100

        if self.input_entry.get() == self.text_label.cget('text'):
            self.running = False
            self.input_entry.config(fg="green")
            self.input_entry.config(state= 'disable')

    """
        This function start the timer, calculate the speed and  accurracy
    """
    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            self.wpm = (self.char_count-self.red_char)* 60 /(self.counter * 5)
            self.speed_label.configure(text = f"{self.wpm:.2f} WPM\n{self.accuracy:.2f}% accuracy")

    """
        This function reset back to the initial data
        Press F5 or Reset button
    """
    def reset(self):

        # Reset running state
        self.running = False
        self.input_entry.config(state = 'normal')

        # Reset text
        self.random_text = random.choice(self.text)
        self.text_list = self.random_text.split()

        # Reset speed and accuracy
        self.char_count = 0
        self.red_char = 0
        self.red = False
        self.counter = 0
        self.wpm = 0
        
        # Reset tracking word and letter
        self.track = 0
        self.track_words = 0 
        self.cur_word = ""

        # Reset label and entry
        self.speed_label.config(text= f"{self.wpm:.2f} WPM\n{self.accuracy:.2f}% accuracy")
        self.text_label.config(text= self.random_text, underline= self.track)
        self.input_entry.delete(0, END)

    # Close main window by press X on the top right or Quit button
    def quit(self):
        self.root.destroy()

def main():
    type = TypeSpeedGUI()

if __name__ == "__main__":
    main()