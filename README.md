# Vocabulary Builder
This utility assists in compiling a list of useful vocabulary in an efficient and simple manner. For example, if you are reading something on internet and you come across a useful vocabulary term, then you can press the assigned keyboard shortcut and add the term and its meaning automatically to your vocabulary list in a matter of seconds. This vocabulary list can be useful in preparing for standardized tests, improving communication and written skills, and for building your own personal dictionary. 

### Files included:

dictionary.json : This file contains the words that have been compiled together overtime by the user in a JSON format.
vocab_list.pdf : This file uses dicitionary.json to create a readable PDF file.
vocab_builder.py: This file contains the logic that gets the word and its definition and puts it into the dictionary.json file.

### API's used:

PyDictionary: for getting the definition of the word
PyQt: for designing the GUI for the application

### How to use this utility:
1. First, open up vocab_builder.py and change the paths of the file to suit your needs.

2. Move the python executable file to usr/local/bin

3. Using the linux terminal, copy over the generated executable to usr/local/bin.

4. Open linux settings->devices->keyboard --> add new shortcut

5. Name field is arbitrary. For the command field, insert "vocab_builder" (without the quotes. Note: This name must be same as the name of the executable in usr/local/bin)

6. Assign any shortcut key combination.

### Code in action:

Select the word that you want to add to your list of words.
Press the shortcut key.
This should open up a dialog box populated with your selected word and its definition.
You can view your own list of words and its definitions by opening the vocab_list.pdf file.


### Extra Notes:
A sample of words list is provided along with other files. Delete all the words keeping just the {}. This is required otherwise the program will throw an error.
