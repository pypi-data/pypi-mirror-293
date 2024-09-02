from .deckwriter import DeckWriter
from .filehandler import FileHandler
from .jsonhandler import JsonHandler

class DeckCreator():
    def __init__(self, path):
        self.path = path
        self.DeckWriterObject = DeckWriter(path=path)
        self.FileHandlerObject = FileHandler(path=path)
        self.JsonHandlerObject = JsonHandler(path=path)
    # derivs = parse_derivatives()
    # print(get_derivative(derivs,"ager"))
    # print(derivs)    

    def create_deck_internal(self,words,delay=0.1):
        return self.DeckWriterObject.return_deck(words)

    def create_deck_textfile(self, input="input.txt", output="output.txt", delay=0.1, append=False):
        lines = self.FileHandlerObject.read_text_lines(input)
        deck = self.create_deck_internal(lines, delay)[0] 
        self.FileHandlerObject.write_text_lines(deck,output,append,delay)


    


    