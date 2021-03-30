import random
import smtplib
import time
#This is in German lol
import speech_recognition as sr
import keyboard
import webbrowser
global bungee, wkey
bungee = str("on")
wkey = "API_KEY"
import requests, json
def get_contact(contact_id, to_get):
    with open("contact_" + contact_id + ".alexa", "r+") as file:
        d = file.read()
        data = json.loads(d)
        turner = data[to_get]
        return turner
print(get_contact("1", "email"))
def sendmail(subject, msg_, receiver):
    msg = str("From: Sendmail <" + "Sendmail@gmail.com" + ">") + "\n"
    msg = msg + time.strftime("%a, %d %b %Y %H:%M:%S +0200", time.gmtime()) + "\n"
    msg = msg + "Message-ID: <Sendmail" + str(random.uniform(1000000, 9999999)) + "@gmail.com>" + "\n"
    msg = msg + "Subject: " + subject + "\n"
    msg = msg + "To: " + receiver + "\n\n"
    msg = msg + msg_ + "\n"
    msg = msg + "   \n"
    print(msg)
    server = smtplib.SMTP_SSL(PROVIDER)
    server.login(DATA)
    server.sendmail(
        "Sendmail@gmail.com",
        receiver,
        msg)
    server.quit()
def say(text, rate, type, volume):
    import win32com.client as wcc
    class Sprecher(object):
        def __init__(self):
            self.speaker = wcc.Dispatch("SAPI.SpVoice")
            self.sprechen()
        def sprechen(self):
            self.speaker.Rate = rate
            self.speaker.Volume = volume
            text_ = """<pitch middle="{0}" > {1} </pitch> """.format(type, text)
            self.speaker.Speak(text_)
    a = Sprecher()
def weather(city, key):
    api_key = key
    uul = ("https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key)
    url = uul
    response = requests.get(url)
    data = json.loads(response.text)
    return data
def calc(calc):
    calc = str(calc)
    calc = calc.replace("x", "*")
    try:
        if "+" in calc:
            first, scnd = calc.split("+")
            end = str(int(first) + int(scnd))
            return end
        if "*" in calc:
            first, scnd = calc.split("*")
            end = str(int(first) + int(scnd))
            return end
        if "/" in calc:
            first, scnd = calc.split("/")
            end = str(int(first) + int(scnd))
            return end
        if "-" in calc:
            first, scnd = calc.split("-")
            end = str(int(first) + int(scnd))
            return end
    except:
        print("Error")
def get_settings():
    directory = "settings.alexa"
    file = open(directory, "r")
    file = str(file.read())
    print(file)
    file = str(file).replace(":::;", "")
    file = str(file).replace(";:::", "")
    file = str(file).replace("\n", "")
    if "rate:" and "volume:" and "type:" and "language:" and "seconds:" and "key:" and "user_email:" in file:
        return True
    else:
        print("File incorrect!")
def respond(text):
    text = text.replace("x", "*")
    text = text.replace("/", "geteilt durch ")
    if alter == "on":
        say("Es wurden keine erlaubten Einstellungen gefunden!", 0, 0, 100)
    else:
        say(text, rate, type, volume)
def getweather(city):
    try:
        rets = weather(city, wkey)
        main = (rets["main"])
        temp_min = int(main["temp_min"])
        temp_max = int(main["temp_max"])
        temp = int(main["temp"])
        rets = ("die mindest temperatur in " + city + " betraegt " + str(
            (temp_min - 273.15).__round__()) + "°C, die höchsttemperatur beträgt " + str(
            (temp_max - 273.15).__round__()) + "°C und die aktuelle temperatur beträgt " + str(
            (temp - 273.15).__round__()) + "°C")
        return rets
    except:
        respond("Es wurde keine Stadt mit diesem Namen gefunden")
def refine(text):
    cmd = str(text).lower()
    print("user command: " +  cmd)
    if cmd.startswith("was ist "):
        cmd = cmd.replace("was ist ", "")
        erg = calc(cmd)
        end = (cmd + " ergibt " + erg)
        respond(end)
        mainloop(key)
    elif "mail" in cmd:
        record("sm_receiver")
    elif cmd.startswith("was ergibt "):
        cmd = cmd.replace("was ergibt ", "")
        erg = calc(cmd)
        end = (cmd + " ergibt " + erg)
        respond(end)
        mainloop(key)
    elif cmd.startswith("rechne "):
        cmd = cmd.replace("rechne ", "")
        erg = calc(cmd)
        end = (cmd + " ergibt " + erg)
        respond(end)
        mainloop(key)
    elif cmd.startswith('wetter '):
        cmd = cmd.replace("Wetter ", "")
        cmd = cmd.replace("wetter ", "")
        ort = (cmd)
        weather = getweather(ort)
        respond(weather)
        mainloop(key)
    elif cmd.startswith("suche "):
        cmd = cmd.replace("suche ", "")
        cmd = cmd.replace(" ", "+")
        url = ("https://www.google.com/search?q=" + cmd)
        webbrowser.open_new_tab(url)
        respond("Ich habe das mal gegooglet!")
        mainloop(key)
    elif cmd.startswith("google "):
        cmd = cmd.replace("google ", "")
        cmd = cmd.replace(" ", "+")
        url = ("https://www.google.com/search?q=" + cmd)
        webbrowser.open_new_tab(url)
        respond("Ich habe das mal gegooglet!")
        mainloop(key)
    else:
        respond("Ich habe nichts zu " + cmd + " gefunden!")
        mainloop(key)
def get_stats():
    try:
        global rate, type, volume, language, seconds, alter, key, user_email
        if get_settings() == True:
            alter = "off"
            file = open("settings.alexa")
            file = str(file.read())
            file = str(file).replace(":::;", "")
            file = str(file).replace(";:::", "")
            file = str(file).replace("\n", "")
            print(file)
            rate, volume, type, language, seconds, key, user_email = file.split(";")
            rate = int(str(rate).replace("rate:", ""))
            volume = int(str(volume).replace("volume:", ""))
            type = int(str(type).replace("type:", ""))
            seconds = int(str(seconds).replace("seconds:", ""))
            key = str(str(key).replace("key:", ""))
            user_email = str(str(user_email).replace("user_email:", ""))
            language = str(str(language).replace("language:", ""))
            if rate >= 10:
                rate = 10
            if type >= 10:
                type = 10
            if type <= -10:
                type = -10
            if rate <= -10:
                rate = -10
            if seconds <= 5:
                seconds = 5
            if seconds >= 10:
                seconds = 10
            if volume <= 1:
                seconds = 1
            if volume >= 100:
                volume = 100
            mainloop(key)
        else:
            alter = str("on")
            respond("off")
    except FileNotFoundError:
        alter = str("on")
        respond("off")
def record(usage):
    global sm_subject, sm_msg, sm_receiver
    if bungee == "on":
        if usage == "null":
            try:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    recorded_audio = recognizer.listen(source, timeout=seconds)
                print("Recognizing the text")
                text = recognizer.recognize_google(
                    recorded_audio,
                    language=language
                )
                text = ("{}".format(text))
                print(text)
                refine(text)
            except Exception as ex:
                print("Es gab einen Fehler: " + str(ex))
                mainloop(key)
        elif usage == "sm_receiver":
            try:
                respond("Bitte gebe an wer die Email erhalten soll")
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    recorded_audio = recognizer.listen(source, timeout=seconds)
                print("Recognizing the text")
                text = recognizer.recognize_google(
                    recorded_audio,
                    language=language
                )
                text = ("{}".format(text)).lower()
                print(text)
                if text.startswith("kontakt"):
                    contact_id = text.replace("kontakt", "")
                    contact_id = contact_id.replace(" ", "")
                    sm_receiver = get_contact(contact_id, "email")
                else:
                    text = text.replace(" ", "")
                    sm_receiver = text.replace("at", "@")
                respond("Bitte geben sie jetzt den Betreff an!")
                record("sm_subject")
            except Exception as ex:
                print("Es gab einen Fehler: " + str(ex))
                record("sm_receiver")
        elif usage == "sm_subject":
            try:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    recorded_audio = recognizer.listen(source, timeout=seconds)
                print("Recognizing the text")
                text = recognizer.recognize_google(
                    recorded_audio,
                    language=language
                )
                text = ("{}".format(text))
                print(text)
                sm_subject = text
                respond("Bitte geben sie jetzt die Nachricht an!")
                record("sm_msg")
            except Exception as ex:
                print("Es gab einen Fehler: " + str(ex))
                record("sm_subject")
        elif usage == "sm_msg":
            try:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    recorded_audio = recognizer.listen(source, timeout=seconds)
                print("Recognizing the text")
                text = recognizer.recognize_google(
                    recorded_audio,
                    language=language
                )
                text = ("{}".format(text))
                print(text)
                sm_msg = text
                sendmail(sm_subject, sm_msg, sm_receiver)
                respond("Deine Nachricht wurde gesendet!")
                mainloop(key)
            except Exception as ex:
                print("Es gab einen Fehler: " + str(ex))
                record("sm_msg")
    else:
        refine("Wetter Kamp-Lintfort")
def mainloop(key):
    while True:
        if keyboard.is_pressed(key):
            record("null")
            break
get_stats()
