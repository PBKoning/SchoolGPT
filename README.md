# SchoolGPT
Dit is een schil om ChatGPT heen, gemaakt met Python en Tkinter om ChatGPT geschikt te maken voor het basisonderwijs.

Om dit programma te gebruiken heb je nodig:
- Python

  Er zijn genoeg handleidingen te vinden hoe je dit kan installeren, bv. https://realpython.com/installing-python/ 

- Een apikey van OpenAI

  Die kan je hier aanmaken: https://platform.openai.com/account/api-keys
  Sla deze key op in een textbestand met de naam apikey.txt in dezelfde map als het Python programma. Het tekstbestand moet geen opmaak hebben. Gebruik dus bijvoorbeeld in Windows Kladblok/Notepad.

  **LET OP!!! Een apikey opslaan in een tekstbestand is uiteraard zeer onveilig. Gebruik dit Python programma dus alleen zelf, of onder toezicht.**

- De pythonmodule openai

  Installeer deze met het commando "pip install openai"

Het programma kent 2 tekstbestanden waarmee de werking wordt beïnvloed:
- chatgpt_init_tekst.txt

  Dit is de tekst die chatgpt "opstart" en aangeeft hoe het moet werken.

- chatgpt_tekst_voor_vraag.txt

  Deze tekst wordt voor elke ingevoerde vraag gezet, zodat het antwoord wordt beïnvloed.


5-3-2023: Eerste werkende versie geüploaded

7-3-2023: Programma heeft nu multithreading, waardoor het nie meer lijkt te bevriezen. Veel commentaar toegevoegd en fouten worden nu opgeslagen in een error logfile.
