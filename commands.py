# In dieser Datei sind findest du ein paar einfache Befehle, die das Schema  Frage - zufällige Antwort befolgen.
# Vielleicht wichtiger findest du auch hier die Beschreibungen der verschiedenen Befehle für den f!help Befehl.
# Stelle sicher, dass du die Beschreibungen hinzufügst, wenn du einen neuen Befehl hinzugefügt hast!



# zugehörige Beschreibungen der Befehle. Die erste ist für den normalen f!help Befehl,
# die zweite für einen noch nicht eingeführten, ausführlicheren Hilfebefehl.
commandDescriptions = {
    "f!hallo":["Simpler Testcommand", "Ein einfacher Command, auf den der Bot einen zufälligen Gruß antowrtet."],
    "f!orakel":["Fiiliiuus Profet", "Beantwortet jegliche Ja/Nein Fragen, die du hast."],
    "f!calc":["Kopfrechenspiel", "Lege dich mit deinen freunden in einem spannenden Kopfrechenduell an!"],
    "f!binary counting channel":["In einem Channel binär zählen", "In einem Channel binär zählen"],
    "f!ranton":["...finde es raus", "Spielt die legendäre Audio in einem VC ab."]
}

# einfache Befehle, die alle auf die gleiche Weise funktionieren:
# Nach einer bestimmten Nachricht wird eine zufällige Nachricht aus einer Liste versendet.
# Um einen neuen Befehlt hinzuzufügen einfach den Befehlsnamen mit Prefix als Schlüssel und als value
# eine Liste von möglichen Antworten zum Dictionary hinzufügen. also z.B.
# "f!command":["antwort1", "antwort2", "antwort3"],
rnd_list = {
    "f!hallo":[     # einfacher Testcommand
               "Sei gegrüßt!",
               "Guten Tag!",
               "Hallo, du!"],
    "f!orakel":[    #einfacher Testcommand 2
                "Ja",
                "Nein",
                "Wahrscheinlich",
                "Vielleicht",
                "Wahrscheinlich nicht",
                "Definitiv",
                "absolut nicht"]
}
