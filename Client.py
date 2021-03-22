import pyaudio, wave, socket, random, string
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 6
filename = "DO_NOT_DELETE_ME.sound_file"

def getback():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "192.168.2.120"
    port = 5483
    s.connect((host, port))
    cca = ("WRAC_" + rstr)
    ccs = cca.encode("ascii")
    s.send(ccs)
    s.close()
    f.close()

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

# Store data in chunks for 3 seconds

for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    frames.append(data)
# Stop and close the stream
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
print('Finished recording')

def get_res(auth):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "IP"
    port = 54833
    s.connect((host, port))
    get_random_str(5)
    cca = ("GET_RESULT:" + auth)
    ccs = cca.encode("ascii")
    s.send(ccs)
    raw_result = s.recv(999999)
    raw_result = raw_result.decode('ascii')
    if raw_result.startswith('weather_gb:'):
        raw_result = raw_result.replace("weather_gb:")
        timezone, sunrise, temp_min, temp_max, temp = raw_result.split(";")
        print("...")
        print(str("Zeitzone: " + timezone))
        print(str("Sonnenaufgang: " + sunrise))
        print(str("Min Temp: " + temp_min + " °C"))
        print(str("Max Temp: " + temp_max + " °C"))
        print(str("Temp: " + temp + " °C"))
        print("...")
    else:
        print("ERROR")
    s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "IP"
port = 54833
s.connect((host, port))
def get_random_str(length):
    global rstr
    letters = string.ascii_lowercase
    rstr = ''.join(random.choice(letters) for i in range(length))
get_random_str(5)
cca = ("ADUIO_AUTH_CODE_" + rstr)
ccs = cca.encode("ascii")
s.send(ccs)
uag = ("DO_NOT_DELETE_ME.sound_file")
f = open(uag, 'rb')
l = f.read(9999999)
s.send(l)
print('Sent Data to Receiver-Server')
s.close()
f.close()
get_res(rstr)
