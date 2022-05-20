from tkinter import *
import time
import threading
import random

class TypeSpeedGUI:

    def __init__(self):
        self.root = Tk()
        self.root.title("10 Fast Finger")
        self.root.geometry("1200x400")

        self.text = open("text.txt", "r").read().split("\n")
        self.random_text = random.choice(self.text)

        self.frame = Frame(self.root)
        self.wpm = 0
        self.counter =0
        self.accuracy = 100
        self.red_char = 0
        self.char_count = 0
        self.text_list = self.random_text.split()

        self.sample_label = Label(self.frame, text= self.random_text, font=("Helvetica", 18))
        self.sample_label.grid(row=0, column=0, columnspan=2, padx=5, pady=10)

        self.input_entry = Entry(self.frame, width=40, font=("Helvetica", 24))
        self.input_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)
        self.input_entry.bind("<KeyRelease>", self.start)
        # self.input_entry.bind("<KeyRelease>", self.key_reset)
        
        self.speed_label = Label(self.frame, text= f"{self.wpm:.2f} WPM\n{self.accuracy:.2f}% accuracy", font=("Helvetica", 18))
        self.speed_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

        self.reset_button = Button(self.frame, text="Reset", command = self.reset, font=("Helvetica", 18))
        self.reset_button.grid(row=3, column=0, padx=5, pady=10)

        # self.input_entry.bind()

        self.quit_button = Button(self.frame, text= "Quit", command = self.quit, font=("Helvetica", 18))
        self.quit_button.grid(row=3, column=1, padx=5, pady=10)

        self.frame.pack( expand=True)
        self.frame.bind("<Leave>", self.quit)
    
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

        self.char_count += 1

        if not self.text_list[0].startswith(self.input_entry.get()):
            self.red_char += 1
            self.input_entry.config(fg="red")

        else:
            self.input_entry.config(fg="black")

        self.accuracy = (1 - self.red_char/ self.char_count)*100
        if event.keycode == 32:
            if self.input_entry.get().startswith(self.text_list[0]):
                cur_word = self.text_list[0]
                self.text_list.remove(cur_word)
            self.input_entry.delete(0, END)

        if self.text_list == [] or self.text_list == None:
            self.running = False
            self.input_entry.config(state= 'disable')
        

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
        self.red_char =0
        self.counter = 0
        self.wpm = 0
        self.random_text = random.choice(self.text)
        self.text_list = self.random_text.split()
        self.speed_label.config(text= f"{self.wpm:.2f} WPM\n{self.accuracy:.2f}% accuracy")
        self.sample_label.config(text= self.random_text)
        self.input_entry.delete(0, END)

    def quit(self):
        self.root.destroy()

def main():
    type = TypeSpeedGUI()

if __name__ == "__main__":
    main()