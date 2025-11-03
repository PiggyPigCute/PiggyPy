
import json

PART_OF_SPEECH_COLORS = {
    "Adjective": 92,
    "Noun": 34,
    "Verb": 91,
    "FunctionParticule": 93,
    "TransformationParticule": 93,
    "Conjonction": 31,
    "Adverb": 33,
    "Pronoun": 96,
    "SpiritWord": 32,
    "Interjection": 95,
    "Particule": 93
}

def open_dico(path):
    file = open(path, encoding="utf-8")
    dico = json.loads(file.read())
    file.close()
    return dico

def str_word(w:dict, english=True, description=True, author=True, date=True):
    return "│ dibi: \033[1m\033[" + str(PART_OF_SPEECH_COLORS[w["partOfSpeech"]]) + "m" + w["dibi"] + "\n\033[0m│ français: \033[1m\033[97m" + w["french"] + "\033[0m" + ("\n│ anglais: " + w["english"] if english and len(w["english"])>0 else "") + ("\n│ description: " + str(w["description"]) if description and "description" in w and w["description"] != None and len(w["description"])>0 else "") + ("\n│ créateur·ice: " + str(w["author"]) if author and "author" in w else "") + ("\n│ date: " + (w["date"].split("T"))[0] if date else "")

def str_dico(dico:list[dict], english=True, description=True, author=True, date=True):
    return "┌────\n" + "\n├────\n".join([str_word(w, english, description, author, date) for w in dico]) + "\n└────"

def search(dico, key, english=False, description=True, author=False, date=False):
    print("┌" + "─"*(len(key)+13) + "┐\n│ Recherche: " + key + " │\n└" + "─"*(len(key)+13) + "┘")
    result = [w for w in dico if key.lower() in w["dibi"].lower() or key.lower() in w["french"].lower() or (english and key.lower() in w["english"])]
    if len(result)==0:
        print("┌────\n│ \033[1mAucun résultat\033[0m\n└────")
    else:
        print(str_dico(result, english, description, author, date))

def search_cond(dico, cond, english=False, description=True, author=False, date=False):
    print("┌" + "─"*26 + "┐\n│ Recherche conditionnelle │\n└" + "─"*26 + "┘")
    result = [w for w in dico if cond(w)]
    if len(result)==0:
        print("┌────\n│ \033[1mAucun résultat\033[0m\n└────")
    else:
        print(str_dico(result, english, description, author, date))
