import numpy as np
import math
import pyaudio
from subprocess import call

#ask for a string
#convert string to binary
#

def char_2_bits(character):

	#bin returns a binary string where the first two digits label it as binary
	bits = bin(ord(character))[2:]

	#0s must be added to the start of bits if it is less than 8 characters (a byte)
	bits = '00000000'[len(bits):] + bits

	return map(int, bits)

def str_2_bits(string):
	bits = []
	for c in string:
		byte = char_2_bits(c)
		bits.extend(byte)
	return bits

def bits_2_wave(bits, fs, duration):

	wave = []

	for bit in bits:
		if bit == 0:
			wave.append(sine(440,.1,fs))
		elif bit == 1:
			wave.append(sine(640,.1,fs))

	wave = np.concatenate(wave)*0.25

	return wave

def sine(frequency, length, rate):
    length = int(length * rate)
    factor = float(frequency) * (math.pi * 2) / rate
    return np.sin(np.arange(length) * factor)

def play_wave(samples, fs, volume = 1):
	p = pyaudio.PyAudio()

	stream = p.open(format=pyaudio.paFloat32,
	                channels=1,
	                rate=fs,
	                output=True)
	stream.write(samples.astype(np.float32).tostring())

	# play. May repeat with different volume values (if done interactively) 
	#stream.write(volume*samples)

	#stream.stop_stream()
	stream.close()

	p.terminate()

def run_transmitter(): 	

	#start on JACK
	call(["sudo", "jack_control", "start"])
	bobby = str_2_bits("jeremy ur a cutie")
	print len(bobby)
	bob = bits_2_wave(bobby,44100,1.0)

	play_wave(bob,44100,0.5)
	#test = np.array([])
	#bits_2_wave()
run_transmitter()
