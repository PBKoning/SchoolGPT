import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime
import os, time, openai, sys
import threading as thr


class Application(tk.Frame):

    # Variabelen
    content = "" # Dit is de vraag die wordt gesteld aan chatgpt

    logfile = "data/gesprek.txt" # Bestand waar het gesprek in wordt opgeslagen
    errorfile = "data/errors.txt" # Bestand waarin de errors worden opgeslagen
    fontgrootte = 18
    
    messages = [] # Slaat het gesprek op voor follow up questions

    max_length_question = 100 # Maximaal aantal tekens voor een vraag
    max_questions = 10 # Aantal vragen waarna een nieuw gesprek begint
    count_questions = 0 # Telt het aantal vragen in het gesprek

    eerste_gesprek = True # Wordt het eerste gesprek gevoerd? Bij een nieuw gesprek een ander vervolg
    ready_for_next_question = False # Kan de volgende vraag worden gesteld?
    init_chatgpt_flag = False # Wordt ChatGPT (opnieuw) geïnitialiseerd

    # Bestanden inlezen en opslaan in variabelen

    try:
        # Lees de chaptgpt init tekst in
        file_name = "data/chatgpt_init_tekst.txt"  
        t = ""
        with open(file_name, "r") as f:   
            for line in f: 
                t = t + line
        chatgpt_init_tekst = t    
        #print(t)    
    except Exception as e:
        # Sla de fout op in een logbestand
        print(f"\nError: kon {file_name} niet laden.\n")
        file_name = errorfile
        with open(file_name, "a", encoding='utf-8') as f: 
            f.write(str(e)+ "\n\n")  
        sys.exit()    

    
    try:
        # lees de chatgpt tekst voor elke vraag in
        file_name = "data/chatgpt_tekst_voor_vraag.txt"  
        t = ""
        with open(file_name, "r") as f:   
            for line in f: 
                t = t + line    
        chatgpt_tekst_voor_vraag = t
        #print(t)
    except Exception as e:
        # Sla de fout op in een logbestand
        print(f"\nError: kon {file_name} niet laden.\n")
        file_name = errorfile
        with open(file_name, "a", encoding='utf-8') as f: 
            f.write(str(e)+ "\n\n")  
        sys.exit()      

    try:
        # Lees de apikey in
        file_name = "data/apikey.txt"  
        t = ""
        with open(file_name, "r") as f:   
            for line in f: 
                if t == "":
                    t = line.rstrip()
        openai.api_key = t
        #print(t)
    except Exception as e:
        # Sla de fout op in een logbestand
        print(f"\nError: kon {file_name} niet laden.\n")
        file_name = errorfile
        with open(file_name, "a", encoding='utf-8') as f: 
            f.write(str(e)+ "\n\n")  
        sys.exit()         
    
    def __init__(self, master=None):
        """
        Initialiseert de class. 
        
        TKinter wordt geïnitialiseerd.
        ChatGPT wordt geïnitialiseerd. 
        """  
        super().__init__(master)
        self.master = master
        self.master.title("School GPT")
        self.master.geometry("800x550")  # stel de grootte van het venster in op 800x600
        self.master.resizable(False, False)  # zorg ervoor dat het venster niet kan worden vergroot of verkleind
        self.pack()
        self.create_widgets()

        # Tekst in het tekstvak om aan te geven dat ChatGPT wordt gestart en de thread voor de wachtpuntjes starten.        
        self.textbox.insert(tk.END, "ChatGPT wordt gestart, Even geduld..."+ '\n\n')
        wacht_thread=thr.Thread(target=self.wacht_puntjes, daemon=True) # deamon=True zorgt ervoor dat er geen foutmeling komt bij afsluiten als de thread nog loopt
        wacht_thread.start()


        self.init_chatgpt() # ChatGPT initialiseren


    # def add_text():
    #     """
    #     Voeg tekst toe aan het tekstvak.
    #     """
    #     st.insert(tk.END, input_box.get() + "\n")
    #     st.see(tk.END)

    def create_widgets(self):
        """
        Functie om de widgets voor TKinter te maken.
        """
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

        # Stel de vraag samen met de standaardtekst ervoor, zodat de gewenste antwoorden komen.
        self.content = self.chatgpt_tekst_voor_vraag + vraag

        self.input_box["state"] = tk.DISABLED # Schakel het invoervak tijdelijk uit.
        # Stel nu de vraag in een aparte thread, zodat TKinter niet vastloopt.
        t1=thr.Thread(target=self.ask_chatgpt, daemon=True) # deamon=True zorgt ervoor dat er geen foutmeling komt bij afsluiten als de thread nog loopt
        t1.start()
        self.ready_for_next_question = False
        
    
        
            
        
            
    def ask_chatgpt(self):
        chat_response = "" # Variabele voor de response van ChatGPT
        try:
            self.messages.append({"role": "user", "content": self.content}) # Voeg de vraag toe aan het gesprek
            
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
            )

            chat_response = completion.choices[0].message.content # Stel de vraag aan ChatGPT
            #print(chat_response)
            
    	# Handel fouten af als er geen response komt. bv. omdat de API-key niet klopt, het te druk is of omdat er teveel vragen zijn gesteld.    
        except Exception as e:
            # Sla de fout op in een logbestand
            file_name = self.errorfile
            with open(file_name, "a", encoding='utf-8') as f: 
                f.write(str(e)+ "\n\n")  
            if "Incorrect API key"in str(e) :
                chat_response = "Er ging iets fout. Klopt de API-key?"
            else:  
                chat_response = "Er ging iets fout. Misschien is ChatGPT overbelast? Probeer het nog eens."

        # Tekstuitvoer naar het scherm: bij initialisatie van ChatGPT
        if self.init_chatgpt_flag == True:
            # Uitvoer bij een eerste gesprek
            if self.eerste_gesprek == True:
                self.textbox.delete("1.0", tk.END) # Maak het tekstvak leeg voor het eerste gesprek
                now = datetime.now() # Get current date and time
                date_time_string = now.strftime("%d/%m/%Y %H:%M:%S" + "\nLet op! dit gesprek wordt opgeslagen op de computer!") 
                self.output_text(date_time_string + '\n\n')
                self.output_text(chat_response + '\n\n')
                self.textbox.insert(tk.END, "Stel je vraag en druk op <enter>."+ '\n\n')
                self.eerste_gesprek = False # Het eerste gesprek is nu geweest
            else: 
                pass # Bij latere initialisaties niets op het scherm: bij de vragen komt al in beeld dat het een nieuw gesprek is.
                
            
            # Maak het invoervak leeg
            self.input_box.delete(0, tk.END)
            # Zet de focus terug op het invoervak
            self.input_box.focus_set() 

            self.init_chatgpt_flag = False  # Initialisatie is klaar en er worden weer vragen beantwoord
            self.input_box["state"] = tk.NORMAL # Schakel het invoervak weer in.
            self.ready_for_next_question = True # Klaar voor de volgende vraag   
            self.title_label.configure(text="SchoolGPT") # Boven in het scherm weer de titel van het programma
        
        # Tekstuitvoer bij alle andere vragen.
        else:
            
            self.output_text(chat_response + '\n\n') # Antwoord in het uitvoervak       

            self.count_questions += 1 # Tel de vragen
            t = "(" + str(self.count_questions) + "/" + str(self.max_questions) + ")"
            self.status_label.configure(text=t) # En zet dat in het label
            # Bij maximaal aantal vragen gesprek wissen en opnieuw initialiseren       
            if self.count_questions >= self.max_questions:
                self.output_text("(Er start nu een nieuw gesprek. Het geheugen wordt gewist.)"+ '\n\n')
                self.count_questions = 0
                self.init_chatgpt()
            else:
                self.input_box["state"] = tk.NORMAL # Schakel het invoervak weer in.        
                self.ready_for_next_question = True # Klaar voor de volgende vraag   
                self.title_label.configure(text="SchoolGPT") # Titel weer bovenin beeld


    def init_chatgpt(self):     
        """
        Functie om ChatGPT te initialiseren met de init tekst, zodat ChatGPT weet waar het voor bedoeld is.
        """
        self.init_chatgpt_flag = True # flag om aan te geven dat ChatGPT wordt geïnitiaiseerd, nodig als respons terug komt via thread

        # Zet het aantal vragen en het maximaal aantal vragen in het label op het scherm
        t = "(" + str(self.count_questions) + "/" + str(self.max_questions) + ")"
        self.status_label.configure(text=t)


        self.messages = [] # Maak het gesprek met ChatGPT leeg
        self.content = self.chatgpt_init_tekst # De chat wordt met de init tekst opgestart
        self.messages.append({"role": "user", "content": self.content}) # Voeg de vraag toe aan het gesprek
                
        self.input_box["state"] = tk.DISABLED # Schakel het invoervak tijdelijk uit.
        # Stel nu de vraag in een aparte thread, zodat TKinter niet vastloopt.
        t1=thr.Thread(target=self.ask_chatgpt, daemon=True) # deamon=True zorgt ervoor dat er geen foutmeling komt bij afsluiten als de thread nog loopt
        t1.start()
        self.ready_for_next_question = False # Er kunnen even geen vragen worden gesteld, wachtpuntjes gaan lopen
        

    def output_text(self, content):
        """
        Functie om tekst in het tekstvak te zetten en ook op te slaan in een tekstbestand, zodat het gesprek wordt opgeslagen.
        """
        self.textbox["state"] = tk.NORMAL
        self.textbox.insert(tk.END, content)
        self.textbox.see(tk.END)
        self.textbox["state"] = tk.DISABLED

        file_name = self.logfile
        with open(file_name, "a", encoding='utf-8') as f: 
            f.write(content)  


    def wacht_puntjes(self):
        """
        Constant lopende thread die de wachtpuntjes in de titellabel zet als er geen vraag kan worden gesteld.
        """
        tekst = ""
        while True:
            if self.ready_for_next_question == False:
                tekst += "░ "
                if len(tekst) > 12:
                    tekst = ""
                self.title_label.configure(text=tekst)
                time.sleep(0.2)                
            else:
                tekst = ""        


root = tk.Tk()
app = Application(master=root)
app.mainloop()
