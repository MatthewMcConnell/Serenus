import pyaudio

class MicStream(object):
	""" Returns an pyaudio audiostream, which should be opened 
		with a with-statement. Closes properly.
	"""
	def __init__(self):
		self._audio = pyaudio.PyAudio()

	def __enter__(self):
		self.stream = self._audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
		return self.stream

	def __exit__(self, type, value, traceback):
		self.stream.stop_stream()
		self.stream.close()
		self._audio.terminate()

