import pyttsx3
import PyPDF2

# A simple program, that reads aloud pdf documents
# placed in the "Audiobook"-folder. The sound quality
# kinda sucks though, as does the intonation

engine = pyttsx3.init()
#engine.setProperty('rate', 150)

book = open('bookname.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(book)
pages = pdfReader.numPages
print(pages)
a = int(input("Aloitussivu"))
for i in range(pages-a+1):
    print(i+a)
    page = pdfReader.getPage(i+a-1)
    text = page.extractText()
    engine.say(text)
    engine.runAndWait()
