import json
import socket
import requests
def get_result(auth):
    dest = str("server_gb/" + auth + ".gb")
    gat = open(dest, 'r')
    result = gat.read()
    return result
def give_back(bungee, auth):
    dest = str("server_gb/" + auth + ".gb")
    gat = open(dest, 'w')
    gat.write(bungee)
def get_weather(ort, auth):
    api_key = "KEY"
    uul = ("https://api.openweathermap.org/data/2.5/weather?q=" + ort + "&appid=" + api_key)
    url = uul
    response = requests.get(url)
    data = json.loads(response.text)
    main = (data["main"])
    sys = (data["sys"])
    timezone = int(data["timezone"])
    timezone = str(timezone)
    temp_min = int(main["temp_min"])
    sunrise = int(sys["sunrise"])
    temp_max = int(main["temp_max"])
    temp = int(main["temp"])
    temp = str(temp - 273.15)
    temp_max = str(temp_max - 273.15)
    temp_min = str(temp_min - 273.15)
    sunrise = str(sunrise.__round__())
    print("...")
    print(str("Zeitzone: " + timezone))
    print(str("Sonnenaufgang: " + sunrise))
    print(str("Min Temp: " + temp_min + " °C"))
    print(str("Max Temp: " + temp_max + " °C"))
    print(str("Temp: " + temp + " °C"))
    print("...")
    bungee_str = str("weather_gb:"+ timezone + ";" + sunrise + ";" + temp_min + ";" + temp_max + ";" + temp)
    give_back(bungee_str, auth)
def get_cmd(cmd, auth_code):
    cmd = str(cmd)
    if cmd.startswith('Wetter') or ('wetter'):
        print("got command 'weather'")
        cmd = cmd.replace("Weather", "")
        cmd = cmd.replace("weather", "")
        ort = (cmd)
        get_weather(ort, auth_code)
    else:
        bungee = "--0;end"
        give_back()
def ref_audio(auth, name):
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.AudioFile(name) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language="en-EN")
            print('Converting audio transcripts into text ...')
            print(text)
            get_cmd(text, auth)
        except:
            give_back( )
            print('ERROR')
serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.2.120"
print(host)
port = 54833
serversocket.bind((host, port))
serversocket.listen(50000000)
while True:
    clientsocket, addr = serversocket.accept()
    auth = clientsocket.recv(9999999)
    auth = str(auth.decode('ascii'))
    if auth.startswith('GET_RESULT:'):
        auth = auth.replace("GET_RESULT:", "")
        auth_code = (auth)
        raw_result = get_result(auth)
        clientsocket.send(raw_result.encode('ascii'))
    if auth.startswith("AUDIO_AUTH_CODE_"):
        auth = auth.replace("ADUIO_AUTH_CODE_", "")
        name = ("server_storage/" +auth + ".wav")
        with open(name, 'wb') as f:
            print("Opened File")
            while True:
                print('receiving data...')
                data = clientsocket.recv(9999999)
                if not data:
                    ref_audio(auth, name)
                    break
                f.write(data)
