import PyPDF2

# file = open('IBROHIM_ABDIVOKHIDOV_CV.pdf', 'rb')


def clear_text(text):
    text = text.replace('•', '')
    text = text.replace('_', '')
    text = text.replace('-', '')
    text = text.replace('—', '')
    text = text.replace('Proof:ZView', '')
    text = text.replace('Proof: ZView', '')
    text = text.replace('Proof:Z View', '')
    text = text.replace('Proof: Z View', '')

    return text


def read_pdf(file):
    pdfReader = PyPDF2.PdfReader(file)

    pages = len(pdfReader.pages)

    for i in range(pages):
        
        page = pdfReader.pages[i]
        print("Page\n", i)
        
        t = page.extract_text()
        c = clear_text(t)

        print('Content\n', c)

        return c


# read_pdf(file)