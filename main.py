# Ein Discord Bot, bei dem jeder aus dem Info LK etwas hinzufügen kann

# momentan einfache Textcommands und ein Voice Channel Command

import discord  # installiere mit "python3 -m pip install -U discord.py" (MacOs/Linux) oder "py -3 -m pip install -U discord.py" (Windows)
import random
import asyncio
import math
from numpy import diff
from discord import FFmpegPCMAudio  # nur für voice chat benötigt, muss vielleicht unabhängig installiert werden
from os import listdir
from os.path import isfile, join
import os
from matheAufgaben import createTask    # erstellt Aufgaben für das Kopfrechenspiel
from commands import rnd_list, commandDescriptions

intents = discord.Intents.default()     
intents.message_content = True
client = discord.Client(intents=intents)    # standardmäßige Berechtigungen, um Nachrichten zu senden

with open("token.txt", "r", encoding="utf-8") as hfile:
    token=hfile.read()
    if token.startswith("Hier deinen Token reinpacken!"):
        token = input("Kopiere hier deinen Discord Bot Token hin und drücke Enter oder noch besser, schreibe ihn in 'token.txt', um ihn beim nächsten Mal automatisch zu laden! (Wenn du noch keinen Discord Bot Token hast, solltest du im Discord Developer Portal eine neue Bot-Applikation erstellen.) Dein Token hier: ")


list_keys = rnd_list.keys()     # Liste der obrigen Befehle

games = {}  # für das Kopfrechenspiel

countingChannels = [int(f) for f in listdir("binarycount/") if isfile(join("binarycount/", f))]     # channels, in denen binär gezählt wird.

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('f!help'))   # im Profil wird "playing f!help" angezeigt
    print("ready")


@client.event
async def on_message(message):
    msg = message.content.lower()

    # nicht auf eigene Nachrichten reagieren
    if message.author == client.user:
        return
    

    if msg == "f!ranton":
        if (message.author.voice):
            channel = message.author.voice.channel  # Sprachkanal des Nutzers
            voice = await channel.connect()         # mit Sprachkanal verbinden
            source = FFmpegPCMAudio('rrranton.mp3') # FFmpeg Kodierung, damit Discord den Sound abspielen kann
            await asyncio.sleep(1)      # verhindert eine unregelmäßige Geschwindigkeit beim Abspielen
            player = voice.play(source)
            await asyncio.sleep(2)
            await channel.guild.voice_client.disconnect() # leaved nach weiteren 2 Sekunden
        else:
               await message.channel.send("Du solltest in einem Channel sein, um diesen Befehl zu benutzen")


    # erstellt eine Datei mit der Channel ID als Name. Die erste Zahl darin ist der Zahlenwert, der momentan erreicht ist. Der Zweite Wert ist die ID vom Nutzer, die als letztes gezählt hat.
    if msg.startswith("f!binary counting channel"):
        with open("binarycount/"+str(message.channel.id), "w", encoding="utf-8") as hfile:
            hfile.write("0,0")
        await message.channel.send("Du kannst anfangen, hier in Binär zu zählen! `f!remove counting channel` beendet den Zählchannel. Die Nächste Zahl ist: 0")
        countingChannels.append(message.channel.id)
    
    # löscht diese Datei für einen Channel, falls vorhanden
    if msg.startswith("f!remove counting channel"):
        try:
            os.remove("binarycount/"+str(message.channel.id))
            await message.channel.send("Das hier ist kein Zählkanal mehr.")
        except FileNotFoundError:
            await message.channel.send("Was ist deine Mission? das hier ist gar kein Zählchannel???")

    
    if message.channel.id in countingChannels:
        try:
            answer = int(msg.replace(" ", ""))  # erlaubt es, in Bytes oder anders für Lesbarkeit zu gliedern
        except ValueError:
            return  # keine Zahl -> keine Reaktion

        with open("binarycount/"+str(message.channel.id), "r", encoding="utf-8") as hfile:
            content = hfile.read()
        solutionBin = int(str(bin(int(content.split(",")[0]))).split("0b")[1])  # unnötig komplizierter Code, der den Text in der Datei zu einem Integer umwandelt, der die binäre Ziffernfolge in Dezimal hat
        prev = int(content.split(",")[1])
        if answer == solutionBin and message.author.id != prev:  # wenn nicht zweimal der gleiche Nutzer gezählt hat
            with open("binarycount/"+str(message.channel.id), "w", encoding="utf-8") as hfile:
                hfile.write(str(int(str(solutionBin), 2)+1) + "," + str(message.author.id))  # Fortschritt und letzten Nutzer speichern
            await message.add_reaction("✅")
        else:
            with open("binarycount/"+str(message.channel.id), "w", encoding="utf-8") as hfile:
                hfile.write("0,0")
            await message.channel.send("Haha, <@" + str(message.author.id) + "> ruined the streak of " + str(solutionBin) + ". The next number is 0.")
        
        

    


    if msg.startswith("f!calc"):
        if msg == "f!calc stop":
            if (message.channel.id in list(games.keys())):    # sucht nach existierenden Spielen im Dictionary games für diesen channel
                if (games[message.channel.id]["state"] != "calc"):
                    await message.channel.send("In diesem Channel läuft gerade ein Spiel, das kein Rechenspiel ist!")
                    return
                games.pop(message.channel.id)           # entfernt das Spiel aus dem Dictionary und beendet es damit
                await message.channel.send("Dein Spiel wurde beendet.")
                return
            else:
                await message.channel.send("Hier ist gerade kein Spiel, schreibe `f!calc`, um eins zu beginnen!")
                return
        elif msg == "f!calc skip":
            if not message.channel.id in list(games.keys()):    # sucht nach existierenden Spielen im Dictionary games für diesen channel
                await message.channel.send("Hier ist gerade kein Spiel. Schreibe `f!calc`, um eins zu beginnen")
                return
            if games[message.channel.id]["state"] != "calc":
                await message.channel.send("In diesem Channel läuft gerade ein Spiel, das kein Rechenspiel ist!")
                return
            skipped = games[message.channel.id]["current task"][1]      # merkt sich das Ergebnis, der übersprungenen Aufgabe
            games[message.channel.id]["current task"] = createTask(
                games[message.channel.id]["type"], games[message.channel.id]["difficulty"]) # erneuert die Aufgabe
            await message.channel.send("Die richtige Antowrt wäre gewesen: " + str(skipped) + " Die neue Aufgabe: " + games[message.channel.id]["current task"][0]) # gibt vorheriges Ergebnis und neue Aufgabe aus
            return
        # wird ausgeführt, wenn f!calc ohne skip oder stop aufgerufen wird
        msg = msg.split("f!calc", 1)[1] # reduziert auf die Parameter nach dem Befehl
        msg = msg.split(" ")            # trennt die Parameter an den Leerzeichen (msg ist jetzt eine Liste)
        if len(msg) > 4:
            await message.channel.send("Falscher Syntax. `f!calc [type: +,-,*,:] [difficulty: 1-6; 0 for random] [number of rounds]`")
            return
        # im Nachfolgenden werden die Parameter in die dazugehörigen Variablen eingeordnet
        elif len(msg) == 1:
            tType = "random"
            tDifficulty = "1-3"
            tRounds = 9
        else:
            tType = msg[1]
            if len(msg) > 2:
                tDifficulty = msg[2]
            else:
                tDifficulty = "1-3"
            if len(msg) > 3:
                try:
                    tRounds = int(msg[3])
                except ValueError:
                    await message.channel.send("Die Rundenanzahl sollte eine Zahl sein. Der Syntax ist: `f!calc [type: +,-,*,:] [difficulty: 1-6; 0 for random] [number of rounds]`")
            else:
                tRounds = 9
        games[message.channel.id] = {"participants": {message.author.id: 0},
                                     "round": tRounds,
                                     "type": tType,
                                     "difficulty": tDifficulty,
                                     "state": "calc"} # erstellt den Dictionary Eintrag mit den Parametern und dem Ersteller als ersten Spieler
        games[message.channel.id]["current task"] = createTask(games[message.channel.id]["type"], games[message.channel.id]["difficulty"])     # erste Aufgabe
        
        # Fehler beim Generieren der Aufgabe:
        if games[message.channel.id]["current task"][0].startswith("ERROR1"):
            await message.channel.send("Versteh ich nicht. Der Syntax ist: `f!calc [type: +,-,*,:] [difficulty: 1-6; 0 for random] [number of rounds]`")
            games.pop(message.channel.id)
            return
        if games[message.channel.id]["current task"][0].startswith("ERROR2"):
            await message.channel.send("Invalide Operation. (erstes Parameter nach `f!calc`) is invalid. Es sollte +, -, *, : oder random (oder mehrere mit Komma getrennt (+,-,:)")
            games.pop(message.channel.id)
            return
        if games[message.channel.id]["current task"][0].startswith("ERROR3"):
            await message.channel.send("Invalider Schwierigkeitsgrad. Es sollte eine Zahl oder Reichweite sein (z.B. 2-5) und nicht mehr als 6.")
            games.pop(message.channel.id)
            return
        
        # beginnt Spiel!
        await message.channel.send("Spiel begonnen! `f!calc stop` Schreibe, um es frühzeitig zu beenden. Antworte schneller, als deine Freunde! `f!calc skip`, um eine zu schwere Aufgabe zu überspringen.")
        await message.channel.send(games[message.channel.id]["current task"][0])
        return

    # wenn im Channel ein Rechenspiel läuft:
    if message.channel.id in list(games.keys()) and games[message.channel.id]["state"] == "calc":
        msg = msg.replace(",", ".")     # für Kommazahlen mit "." statt ","
        game = message.channel.id       # kürzer als message.channel.id
        try:
            float(msg)
        except ValueError:
            await message.add_reaction("❓")    # keine Zahl, sondern Text
            return
        
        if abs(float(msg) - float(games[game]["current task"][1])) < 0.00000001:  # nicht ==, weil Floatkalkulation minimale Abweichungen aufweisen kann.
            if message.author.id in list(games[game]["participants"].keys()):     # falls bereits Teilnehmer
                games[game]["participants"][message.author.id] += 1
            else:
                games[game]["participants"][message.author.id] = 1                # wenn kein Teilnehmer, wird Teilnehmer und erhält einen Punkt.
            games[game]["current task"] = createTask(games[game]["type"], games[game]["difficulty"]) # neue Aufgabe
            games[game]["round"] -= 1
            await message.add_reaction('✅')

            # Auswertung am Ende des Spiels:
            if games[game]["round"] == 0:
                ranking = sorted(games[game]["participants"].items(), key=lambda x: x[1], reverse=True)
                titles = [":first_place: ", "\n:second_place: ", "\n:third_place:",
                          "\n4. ", "\n5. ", "\n6. ", "\n7. ", "\n8. ", "\n9. ", "\n10. "]
                reply = ""
                if len(ranking) > 10:
                    cparticipants = 10
                else:
                    cparticipants = len(ranking)
                for i in range(cparticipants):
                    reply = reply + \
                        titles[i] + "<@" + str(ranking[i][0]) + \
                        "> (score: " + str(ranking[i][1]) + ")"
                games.pop(game)
                await message.channel.send(reply)
                return
            await message.channel.send(games[game]["current task"][0])
        
        # bei falscher Antwort:
        else:
            if not message.author.id in list(games[game]["participants"].keys()):
                games[game]["participants"][message.author.id] = 0      # fügt bei Bedarf neuen Spieler hinzu
            await message.add_reaction("❌")


    if msg == "f!help":
        embed = discord.Embed(title="ÜBERSICHT", description="Die meisten Commands:", color=0xc853e6)  # erstellt so einen hübschen Kasten
        for i in list(commandDescriptions.keys()):
            embed.add_field(name=i, value=commandDescriptions[i][0], inline=True)
        await message.channel.send(embed=embed)
    
    if msg.startswith("f!help "):
        command = msg.split("f!help ", 1)[1]
        if command in list(commandDescriptions.keys()):
            embed = discord.Embed(title=command, description=commandDescriptions[command][1], color=0xc853e6)
            await message.channel.send(embed=embed)
        return

    # iteriert durch alle rnd_list commands und sendet eine zufällige Antwort bei Bedarf:
    for command in list_keys:
        if msg == command:
            reply = random.choice(rnd_list[command])
            await message.channel.send(reply)

    if any(word in msg.lower() for word in ["pneumonoultramicroscopicsilicovolcanoconiosis"]):    # kleines Easteregg oder so
        await message.add_reaction("🫶")

    if msg == "simp" or msg.startswith("simp "):    # auch ein kleines lustiges feature
        simp = discord.Embed(title="Simp alert!", url = "https://www.youtube.com/watch?v=79HvepInByU", description="This alert was activated because someone was simping", color= 0xff0000)
        simp.set_author(name="*alarm sounds*", url = "https://puginarug.com/", icon_url = "https://banner2.cleanpng.com/20171127/20a/red-police-siren-png-clip-art-image-5a1bc3ca664f24.1812680215117690344191.jpg")
        simp.set_thumbnail(url="https://preview.redd.it/m9y7v0alndl51.png?width=750&format=png&auto=webp&s=1814437460b51654bfb4b9feb622f43ffe338f89")
        simp.add_field(name="no panic ma guys n girls", value = "There is no need to panic, if you punish the simp hard enough there is a chance they can change and become a good person again.")
        simp.set_image(url="https://c.tenor.com/dAjBzKj9H3AAAAAC/danger-alert.gif")
        simp.set_footer(text="sincerely, your simp bot and true simp hater")
        await message.channel.send(embed = simp)


# schickt einen Hinweis, wenn in einem Binary Counting Channel eine Nachricht gelöscht wird:
@client.event
async def on_message_delete(message):
    if message.channel.id in countingChannels:
        with open("binarycount"+str(message.channel.id), "r", encoding="utf-8") as hfile:
            content = hfile.read()
        next = str(bin(int(content.split(",")[0]) - 1)).split("0b")[1]
        await message.channel.send(f"<@{message.author.id}> hat hier eine Nachricht gelöscht. Die nächste Nachricht ist: {next}")


client.run(token)   # wenn hier ein Fehler auftritt, solltest du darauf achten, 
