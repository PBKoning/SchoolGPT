# SchoolGPT
Dit is een schil om ChatGPT heen, gemaakt met Python en Tkinter om ChatGPT geschikt te maken voor het basisonderwijs.

## Python-versie
Dit is de originele versie die je eventueel ook zelf kan aanpassen. Je hebt daarvoor nodig:
- Python

  Er zijn genoeg handleidingen te vinden hoe je dit kan installeren, bv. https://realpython.com/installing-python/ 

- Een API-key van OpenAI

  Die kan je hier aanmaken: https://platform.openai.com/account/api-keys
  Sla deze key op in een textbestand met de naam apikey.txt in dezelfde map als het Python programma. Het tekstbestand moet geen opmaak hebben. Gebruik dus bijvoorbeeld in Windows Kladblok/Notepad.

  **LET OP!!! Een API-key opslaan in een tekstbestand is uiteraard zeer onveilig. Gebruik dit Python programma dus alleen zelf, of onder toezicht.**

- De pythonmodule **openai**

  Installeer deze met het commando "pip install openai"

Het programma kent 2 tekstbestanden waarmee de werking wordt beïnvloed:
- chatgpt_init_tekst.txt

  Dit is de tekst die chatgpt "opstart" en aangeeft hoe het moet werken.

- chatgpt_tekst_voor_vraag.txt

  Deze tekst wordt voor elke ingevoerde vraag gezet, zodat het antwoord wordt beïnvloed.

## De Windows-versie
Dit is het Pythonprogramma, maar dan omgezet naar een Windows executable gemaakt met https://pypi.org/project/auto-py-to-exe/.
Je hebt hier dus ook een API-key voor nodig, zoals bij de Python versie. 
Hoe het programma kan worden gedownload en er mee kan worden gewerkt wordt in deze video uitgelegd: https://www.youtube.com/watch?v=C-8xEsL5r1U

### De HTML-versie
Deze versie heeft wat code betreft niets met de Python-versie te maken. De werking ervan is wel min of meer gelijk aan de Python-versie. 
Er wordt bij de HTML-versie van een ander taalmodel van OpenAI gebruik gemaakt: *text-davinci-003* in plaats van *gpt-3.5-turbo*. 
De HTML-versie kan worden gedownload *(samen met 1 afbeelding)* en dan direct vanaf de computer in de browser worden geopend.
Ook hier is weer een API-key nodig om het te laten werken. 

Een versie online is hier te vinden: https://leerhetsnel.nl/demo/SchoolGPT/

### **Disclaimer: gebruik van SchoolGPT, zowel de Python-versie, de Windows executable als de HTML-versie is op eigen risico.**

# Updates

5-3-2023: Eerste werkende versie geüploaded

7-3-2023: Programma heeft nu multithreading, waardoor het niet meer lijkt te bevriezen. Veel commentaar toegevoegd en fouten worden nu opgeslagen in een error logfile.

9-3-2023: Data staat nu in een aparte directory. Foutafhandeling wanneer de API-key niet klopt of bestanden niet kunnen worden geladen. Windows executable toegevoegd (gemaakt met https://pypi.org/project/auto-py-to-exe/)

11-3-2023: HTML-versie toegevoegd die een compleet andere code heeft maar qua werking vergelijkbaar is met de Python-versie. Online versie staat op: https://leerhetsnel.nl/demo/SchoolGPT/