#!/usr/bin/python3
import sys
import os
import json
import subprocess
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QLineEdit, QLabel, QPushButton
from PyQt5.QtCore import QSize
from PyDictionary import PyDictionary
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class ClipBoardWindow(QMainWindow):
    dictionary = PyDictionary()

    def __init__(self, selected_text):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(440, 240))    
        self.setWindowTitle("Vocab Builder") 
        self.word_label = QLabel(self)
        self.word_label.setText('Word : ')
        self.word_label.move(20, 20)
        # Add word_text field
        self.word_box = QLineEdit(self)
        self.word_box.move(100,20)
        self.word_box.resize(280, 40)
        #definition_label
        self.def_label = QLabel(self)
        self.def_label.setText('Definition : ')
        self.def_label.move(20, 100)
        #definition_text
        self.def_box = QPlainTextEdit(self)
        self.def_box.move(100,100)
        self.def_box.resize(280, 80)
        #submit_button
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.move(50, 200)  
        self.submit_button.clicked.connect(self.on_click_submit)

        #open pdf button
        self.pdf_button = QPushButton('Open vocab list', self)
        self.pdf_button.move(220, 200)  
        self.pdf_button.resize(150, 30)
        self.pdf_button.clicked.connect(self.on_click_pdf)

        #get selected text and meaning
        self.selected_text = selected_text.lower()
        self.word_box.setText(self.selected_text)
        meaning = self.getMeaning(self.selected_text)
        self.def_box.clear()
        self.def_box.insertPlainText(meaning)
        #QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

    def getNoun(self, text):
        noun_array = []
        if "Noun" in ClipBoardWindow.dictionary.meaning(text):
            noun_array = ClipBoardWindow.dictionary.meaning(text)["Noun"]
            noun_string = ""
            for noun in noun_array:
                noun_string += noun + '; '
            return noun_string[0: len(noun_string) - 2]
        else:
            return None
        

    def getVerb(self, text):
        verb_array = []
        if "Verb" in ClipBoardWindow.dictionary.meaning(text):
            verb_array = ClipBoardWindow.dictionary.meaning(text)["Verb"]
            verb_string = ""
            for verb in verb_array:
                verb_string += verb + '; '
            return verb_string[0: len(verb_string) - 2]        
        else:
            return None
        

    def getAdj(self, text):
        adj_array = []
        if "Adjective" in ClipBoardWindow.dictionary.meaning(text):
            adj_array = ClipBoardWindow.dictionary.meaning(text)["Adjective"]
            adj_string = ""
            for adj in adj_array:
                adj_string += adj + '; '
            return adj_string[0: len(adj_string) - 2]
        else:
            return None
        

    # return the meaning of the word

    def getMeaning(self, text):
        noun = self.getNoun(text)
        verb = self.getVerb(text)
        adj = self.getAdj(text)
        if noun != None:
            return noun
        elif verb != None:
            return verb
        elif adj != None:
            return adj
        else:
            return "Definition not found"
    


    
    # Get the system clipboard contents
    # alternate way to populate the fields with the content copied to the clipboard
    def clipboardChanged(self):
        text = QApplication.clipboard().text().lower()
        self.word_box.setText(text)
        meaning = self.getMeaning(text)
        self.def_box.clear()
        self.def_box.insertPlainText(meaning)

    def on_click_submit(self):
        with open('/home/harshil/Harshil/projects/personal_projects/vocab_builder/dictionary.json', 'r+') as file:
            data = json.load(file)
            new_data = {
                self.word_box.text(): self.def_box.toPlainText()
            }
            data.update(new_data)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            PDFgenerator.generatePDF()
            print("Successfully added the word and its definition")
            sys.exit()
    def on_click_pdf(self):
        pdf_path = "/home/harshil/Harshil/projects/personal_projects/vocab_builder/vocab_list.pdf"
        doc_viewer = '/usr/bin/evince'
        os.system("%s %s" % (doc_viewer, pdf_path))


class PDFgenerator():
    @staticmethod
    def generatePDF():
        with open('/home/harshil/Harshil/projects/personal_projects/vocab_builder/dictionary.json', 'r') as file:
            data = json.load(file)
        doc = SimpleDocTemplate("/home/harshil/Harshil/projects/personal_projects/vocab_builder/vocab_list.pdf",pagesize=letter,
                        rightMargin=18,leftMargin=18,
                        topMargin=18,bottomMargin=18)
        Story=[]
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='custom_title', alignment=TA_CENTER, fontName = "Times-Roman"))
        styles.add(ParagraphStyle(name='custom_content', alignment=TA_JUSTIFY, fontName = "Times-Roman"))
        ptext = '<font size = 20 color = "green"> Vocab list </font>'
        Story.append(Paragraph(ptext, styles["custom_title"]))
        Story.append(Spacer(1, 10))
        for word in data:
            definition = data[word]
            ptext = '<font size=8 color = "red">%s </font>: <font size = 8> %s </font>' % (word, definition)
            Story.append(Paragraph(ptext, styles["custom_content"]))
            Story.append(Spacer(1, 4))
        doc.build(Story)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    selected_text = os.popen('xsel').read()
    mainWin = ClipBoardWindow(selected_text)
    mainWin.show()
    sys.exit(app.exec())



