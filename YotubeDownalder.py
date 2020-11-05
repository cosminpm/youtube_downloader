#This Script was developed by Cosmin Marian Paduraru at 4/1/2020

import pytube
import os
import time
import subprocess
import sys

# Para solucionar errores al convertirlo al .exe
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

nombreFichero = ''

def audioFun(audio):
		global nombreFichero
		titulo = audio.download()
		clip = VideoFileClip(titulo)
		nombre_audio = titulo.rsplit(".",1)[0]+".mp3"
		clip.audio.write_audiofile(nombre_audio,verbose=False, logger = None)
		clip.close()
		os.remove(titulo)
		nombreFichero = nombre_audio
		nombreFichero = nombreFichero.rsplit('\\')[-1].rsplit('.',1)[0]
		nombreFichero = nombreFichero.replace(' ','_')
		return nombre_audio

def videoFun(audioFich,videoFich):
	global nombreFichero
	os.rename(audioFich,os.getcwd()+"/audio.mp3")
	os.rename(videoFich,os.getcwd()+"/video.mp4")
	cmd = 'ffmpeg -hide_banner -loglevel panic -y -i audio.mp3 -r 30 -i video.mp4  -filter:a aresample=async=1 -c:a flac -c:v copy '+nombreFichero+'.mkv'     #YouTubeVideo.mkv
	subprocess.call(cmd, shell=True)
	os.remove("audio.mp3")
	os.remove("video.mp4")

def main(url, numero):
	video_url = ''
	tipo = 0
	if url != None:
		video_url = url
	else:
		print("Intoduce the link of the video:")
		video_url = input()
	youtube = pytube.YouTube(video_url)

	print ("Type:")
	audio = youtube.streams.first()
	if audio:
		print("0. Only Audio")

	video360 = youtube.streams.filter(res="360p")
	if video360:
		print ("1. 360p")

	video480 = youtube.streams.filter(res="480p")
	if video480:
		print("2. 480p")

	video720 = youtube.streams.filter(res="720p")
	if video720:
		print("3. 720p")

	video1080 = youtube.streams.filter(res="1080p")
	if video1080:
		print("4. 1080p")

	if numero != None:
		tipo = int(numero)
	else:
		print("Intoduce number acording of which type you want: ")
		tipo = int(input())

	print("Downoalding...")
	if tipo == 0:
		audioFun(audio)
	elif tipo == 1:
		audioFich = audioFun(audio)
		videoFich = video360[0].download()
		videoFun(audioFich,videoFich)
	elif tipo == 2:
		audioFich = audioFun(audio)
		videoFich = video480[0].download()
		videoFun(audioFich,videoFich)
	elif tipo == 3:
		audioFich = audioFun(audio)
		videoFich = video720[0].download()
		videoFun(audioFich,videoFich)
	elif tipo == 4:
		audioFich = audioFun(audio)
		videoFich = video1080[0].download()
		videoFun(audioFich,videoFich)
	else:
		print("Wrong number")

if __name__ == "__main__":
	if len(sys.argv) > 1 and sys.argv[1] == '-help':
		print(

''' 
There are 3 main forms of using this script. 
Maybe you have to swicht between python/python3 depending of your SO.

First of all you can use just:
*** "python3 YouTubeDownalder.py" And you will have to paste the URL of the song and choose if you want video or music and its quality.
*** "python3 [url_of_youtube_video]" You just have to choose sound/video and quality
*** "python3 [url_of_youtube_video] [number]" It will alredy downald it 0 corresponding with only music and 1,2,3 corresponding to 360,480... 
It depends on the video, if it doesnt have that quality it will stop with an Error Message.
*** "python3 [file.txt] you may want to download a list of youtube videos. You just have to write the text file in this format:
	
	urlA numberYouWant
	urlB numberYouWant
	...

Enjoy the script.

''')
	
	elif len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
		i = 0
		fichero = open(sys.argv[1],'r')
		for linea in fichero:
			i += 1
			print("Descargando archivo:", i)
			parametros = linea.split(" ")
			main(parametros[0],parametros[1])
		fichero.close()
	elif len(sys.argv) == 1:
		print("Introduce el numero segun lo que quieras:\n1. Descargar una cancion/video\n2. Descargar varias canciones.")
		x = int(input())
		if x == 1:
			main(None,None)
		elif x == 2:
			print("Introduce el nombre del .txt")
			f = input()
			i = 0
			fichero = open(f,'r')
			for linea in fichero:
				i += 1
				print("Descargando cancion:", i)
				parametros = linea.split(" ")
				main(parametros[0],parametros[1])
			fichero.close()
	elif len(sys.argv) == 2:
		main(sys.argv[1],None)
	elif len(sys.argv) == 3:
		main(sys.argv[1],sys.argv[2])
