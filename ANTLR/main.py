import json
from antlr4 import *
from parser.JSONLexer import JSONLexer
from parser.JSONParser import JSONParser
from parser.JSONVisitor import JSONVisitor  # Importáljuk a JSONVisitor-t

class JSONPrettyPrinter(JSONVisitor):
    def visitJson(self, ctx):
        # Az egész JSON fához hozzáférünk
        return self.visit(ctx.value())

    def visitObj(self, ctx):
        # JSON objektumot kezelünk
        obj = {}
        for pair in ctx.pair():
            key = pair.STRING().getText()[1:-1]  # Az idézőjelek eltávolítása
            value = self.visit(pair.value())  # Érték lekérdezése
            obj[key] = value
        return obj

    def visitArr(self, ctx):
        # JSON tömböt kezelünk
        return [self.visit(value) for value in ctx.value()]

    def visitValue(self, ctx):
        if ctx.STRING():
            return ctx.STRING().getText()[1:-1]  # Tömörített stringet adunk vissza
        if ctx.NUMBER():
            return float(ctx.NUMBER().getText())  # Szám értéke
        if ctx.obj():
            return self.visit(ctx.obj())  # Rekurzívan hívunk objektumot
        if ctx.arr():
            return self.visit(ctx.arr())  # Rekurzívan hívunk tömböt
        if ctx.getText() == "true":
            return True
        if ctx.getText() == "false":
            return False
        if ctx.getText() == "null":
            return None
        return None

def print_pretty_json(tree):
    # A parse-olt fát JSON formátumban kiíratjuk
    print(json.dumps(tree, indent=4, ensure_ascii=False))

def main(input_file):
    # Fájl megnyitása
    input_stream = FileStream(input_file)
    
    # Lexer létrehozása
    lexer = JSONLexer(input_stream)
    
    # Token stream létrehozása
    token_stream = CommonTokenStream(lexer)
    
    # Parser létrehozása
    parser = JSONParser(token_stream)
    
    # Elemzés indítása
    tree = parser.json()  # Az elemzés kezdő szabálya (pl. 'json')

    print("JSON Parsed Successfully")

    # Látogató létrehozása
    pretty_printer = JSONPrettyPrinter()
    
    # A parse tree-t átadjuk a JSONPrettyPrinter-nek
    parsed_data = pretty_printer.visit(tree)

    # Kiíratjuk a szép formázott JSON-t
    print("Parsed Tree:")
    print_pretty_json(parsed_data)

if __name__ == "__main__":
    main("test_files/tests.json")
