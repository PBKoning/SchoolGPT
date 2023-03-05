import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import os
import openai


class Application(tk.Frame):

    # lees de chaptgpt init tekst in
    file_name = "chatgpt_init_tekst.txt"  
    t = ""
    with open(file_name, "r") as f:   
        for line in f: 
            t = t + line
    chatgpt_init_tekst = t    
    
    # lees de chatgpt tekst voor elke vraag in
    file_name = "chatgpt_tekst_voor_vraag.txt"  
    t = ""
    with open(file_name, "r") as f:   
        for line in f: 
            t = t + line    
    chatgpt_tekst_voor_vraag = t
    
  

    # Lees de apikey in
    file_name = "apikey.txt"  
    t = ""
    with open(file_name, "r") as f:   
        for line in f: 
            if t == "":
                t = line.rstrip()
    openai.api_key = t
    
    logfile = "gesprek.txt"

    fontgrootte = 18
    max_length_question = 100

    messages = []

    max_questions = 10
    count_questions = 0

    eerste_gesprek = True

    def __init__(self, master=None):

        global messages
        global start_messages
        
        super().__init__(master)
        self.master = master
        self.master.title("School GPT")
        self.master.geometry("800x550")  # stel de grootte van het venster in op 800x600
        self.master.resizable(False, False)  # zorg ervoor dat het venster niet kan worden vergroot of verkleind
        self.pack()
        self.create_widgets()

        self.init_chatgpt()

        self.textbox.insert(tk.END, "Stel je vraag en druk op <enter>."+ '\n\n')

        
        

    def add_text():
        st.insert(tk.END, input_box.get() + "\n")
        st.see(tk.END)

    def create_widgets(self):
        # label voor de titel
        self.title_label = tk.Label(self, text="School GPT", font=("Helvetica", self.fontgrootte))
        self.title_label.pack()

        # tekstvak
        
        self.textbox = ScrolledText(self, height=15, width=50, font=("Helvetica", self.fontgrootte), wrap=tk.WORD)
        self.textbox.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.textbox.bind("<Configure>", self.on_textbox_resize)

        # status label
        self.status_label = tk.Label(self, text="...", font=("Helvetica", self.fontgrootte))
        self.status_label.pack()

        # invoervak voor tekst
        self.input_var = tk.StringVar()  # maak een StringVar-object aan
        self.input_var.trace_add("write", self.limit_input)  # koppel de functie "limit_input" aan het StringVar-object
        self.input_box = tk.Entry(self, width=50, font=("Helvetica", 20), textvariable=self.input_var)
        self.input_box.pack(side=tk.BOTTOM)

        # focus op invoervak houden, zelfs nadat de tekst is gekopieerd
        self.input_box.bind('<Return>', self.add_text)
        self.input_box.focus_set()

        # stel de grootte van de scrollbar in op de grootte van het tekstvak
        self.textbox.update_idletasks()
       


    
    def on_textbox_resize(self, event):
        # pas de breedte van het tekstvak aan aan de breedte van het venster
        self.textbox.configure(width=event.width // self.fontgrootte)


    def limit_input(self, *args):
        # controleer of de invoer langer is dan maximaal aantal tekens
        if len(self.input_var.get()) > self.max_length_question:
            # inkorten tot 20 tekens
            self.input_var.set(self.input_var.get()[:self.max_length_question])

    def add_text(self, event):             
        
        vraag = self.input_box.get()
        if len(vraag) < 5: # er moet wel een vraag worden gesteld, dus niet een kort woordje
            return
        # kopieer de tekst naar het tekstvak
        self.output_text(self.input_box.get() + '\n\n')
            
        # maak het invoervak leeg
        self.input_box.delete(0, tk.END)
        # zet de focus terug op het invoervak
        self.input_box.focus_set()

        content = self.chatgpt_tekst_voor_vraag + vraag

        answer = self.ask_chatgpt(content)
        self.output_text(answer + '\n\n')        

        self.count_questions += 1
        t = "(" + str(self.count_questions) + "/" + str(self.max_questions) + ")"
        self.status_label.configure(text=t)        
        if self.count_questions >= self.max_questions:
            self.count_questions = 0
            self.init_chatgpt()
            
        
            
    def ask_chatgpt(self, content):
        try:
            self.messages.append({"role": "user", "content": content})
            
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
            )

            chat_response = completion.choices[0].message.content
            return(chat_response)
        except Exception as e:
            print(e)
            return("Er ging iets fout. Misschien is ChatGPT overbelast? Probeer het nog eens.")
            


    def init_chatgpt(self):     

        
        t = "(" + str(self.count_questions) + "/" + str(self.max_questions) + ")"
        self.status_label.configure(text=t)

        self.messages = []
        content = self.chatgpt_init_tekst 
        self.messages.append({"role": "user", "content": content})
        answer = self.ask_chatgpt(content)
        if self.eerste_gesprek == True:
            now = datetime.now() # Get current date and time
            date_time_string = now.strftime("%d/%m/%Y %H:%M:%S" + "\nLet op! dit gesprek wordt opgeslagen op de computer!") 
            self.output_text(date_time_string + '\n\n')
            self.output_text(answer + '\n\n')
            self.eerste_gesprek = False
        else: 
            self.output_text("--- nieuw gesprek ---"+ '\n\n')
        
        # maak het invoervak leeg
        self.input_box.delete(0, tk.END)
        # zet de focus terug op het invoervak
        self.input_box.focus_set()            
               


    def output_text(self, content):
        self.textbox["state"] = tk.NORMAL
        self.textbox.insert(tk.END, content)
        self.textbox.see(tk.END)
        self.textbox["state"] = tk.DISABLED

        file_name = self.logfile
        with open(file_name, "a", encoding='utf-8') as f: 
            f.write(content)  


root = tk.Tk()
app = Application(master=root)
app.mainloop()
