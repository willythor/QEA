import pyaudio 
import wave
import numpy as np
from subprocess import call
import matplotlib.pyplot as plt
from scipy.fftpack import fft, rfft
from scipy.io import wavfile # get the api

def get_audio():
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100
	RECORD_SECONDS = 5
	WAVE_OUTPUT_FILENAME = "output.wav"

	p = pyaudio.PyAudio()


	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	print("* recording")

	frames = []

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)

	stream.stop_stream()
	stream.close()
	p.terminate()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()




def freq_listener(chunk=4410):

	
	fs, data = wavfile.read('output.wav') # load the data
	a = data.T[0] # this is a two channel soundtrack, I get the first track
	b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
	c = fft(b) # calculate fourier transform (complex numbers list)
	d = len(c)/2  # you only need half of the fft list (real signal symmetry)
	print np.argmax(abs(c.imag))
	print np.real(c[153])
	plt.plot(abs(c[:1000]),'r') 
	plt.show()

get_audio()
freq_listener()