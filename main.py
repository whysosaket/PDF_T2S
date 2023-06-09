import PyPDF2
import pyttsx3

with open('uhv.pdf', 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    engine = pyttsx3.init()

    speed = 250
    engine.setProperty('rate', speed)

    from_page = 5

    for page in range(num_pages):
        if page < from_page - 1:
            continue
        pdf_page = pdf_reader.pages[page]
        page_text = pdf_page.extract_text()
        engine.say(page_text)

    engine.runAndWait()
