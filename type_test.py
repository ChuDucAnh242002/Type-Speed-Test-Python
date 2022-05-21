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
        self.sample_label = Label(self.frame, text= self.random_text, font=("Helvetica", 18))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start_word)
        # self.input_entry.bind("<KeyRelease>", self.track_word)
        
        self.speed_label = Label(self.frame, text= f"{self.wpm:.2f} WPM\n{self.accuracy:.2f}% accuracy", font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = Button(self.frame, text="Reset", command = self.reset, font=("Helvetica", 18))
        self.reset_button.grid(row=3, column=0, padx=5, pady=10)

        # self.input_entry.bind()

        self.quit_button = Button(self.frame, text= "Quit", command = self.quit, font=("Helvetica", 18))
        self.quit_button.grid(row=3, column=1, padx=5, pady=10)

        self.frame.pack( expand=True)
        self.frame.bind("<Leave>", self.close)
    
        self.running = False

        self.root.mainloop()

    def start_word(self, event):

        if event.keycode == 116:
            self.reset()
            return

        if not self.running:
            if not event.keycode in [13, 16, 17, 18, 32]:
                self.running = True
                t = threading.Thread(target= self.time_thread)
                t.start()
        
        if self.text_list[0].startswith(self.input_entry.get()) and event.keycode not in [13, 16, 17, 18, 32]:
            if event.keycode == 8 and self.input_entry.get() :
                # print("this1")
                if self.red == True:
                    self.red = False
                    return
                self.track -= 1
                self.track_words -= 1
                # print(self.track_words)
            elif event.keycode != 8 and self.input_entry.get() :
                # print("this2")
                self.track += 1
                self.track_words += 1
                # print(self.track_words)
            
        self.char_count += 1

        if not self.text_list[0].startswith(self.input_entry.get()) and event.keycode != 32:
            self.red_char += 1
            self.red = True
            self.input_entry.config(fg="red")

        else:
            self.input_entry.config(fg="black")
           
        self.accuracy = (1 - self.red_char/ self.char_count)*100
        if event.keycode == 32:
            self.cur_word = self.text_list[0]
            count = 0
            if self.input_entry.get().startswith(self.cur_word) and self.track_words == len(self.cur_word):
                self.text_list.remove(self.cur_word)
                count = 0
            elif count == 0 :
                # print("this3")
                self.track -=  (self.track_words + 1)
                count = 1
            # print("this4")
            self.track += 1
            self.track_words = 0
            # print(self.track_words)
            self.input_entry.delete(0, END)

        self.sample_label.config(underline= self.track)

        if self.text_list == [] or self.text_list == None:
            self.running = False
            self.input_entry.config(state= 'disable')
        
    def track_word(self, event):
        self.sample_label.config(underline= self.track)
        
        if self.cur_word.startswith(self.input_entry.get()) and not event.keycode in [8, 13, 16, 17, 18, 32]:
            if event.keycode == 8:
                self.track -= 1
                return
            if event.keycode == 32:
                self.count = 0
                self.track += 1
            self.track += 1
            return

        elif not self.input_entry.get().startswith(self.cur_word) :
            self.cur_word = self.text_list[0]
            if event.keycode == 32 and self.count == 0:
                self.track -= len(self.cur_word)
                self.count = 1
            return

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

        if not self.sample_label.cget('text').startswith(self.input_entry.get()) :
            self.red_char += 1
            self.input_entry.configure(fg="red")

        else:
            self.input_entry.configure(fg="black")

        self.accuracy = (1 - self.red_char/ self.char_count)*100

        if self.input_entry.get() == self.sample_label.cget('text'):
            self.running = False
            self.input_entry.config(fg="green")
            self.input_entry.config(state= 'disable')

    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            self.wpm = (self.char_count-self.red_char)* 60 /(self.counter * 5)
            self.speed_label.configure(text = f"{self.wpm:.2f} WPM\n{self.accuracy:.2f}% accuracy")

    def reset(self):

        self.running = False
        self.input_entry.config(state = 'normal')
        self.char_count = 0
        self.red_char = 0
        self.red = False
        self.counter = 0
        self.wpm = 0
        self.random_text = random.choice(self.text)
        self.text_list = self.random_text.split()
        self.track = 0
        self.track_words = 0 
        self.cur_word = ""
        self.speed_label.config(text= f"{self.wpm:.2f} WPM\n{self.accuracy:.2f}% accuracy")
        self.sample_label.config(text= self.random_text, underline= self.track)
        self.input_entry.delete(0, END)

    def close(self):
        self.root.destroy()

    def quit(self):
        self.root.destroy()

def main():
    type = TypeSpeedGUI()

if __name__ == "__main__":
    main()