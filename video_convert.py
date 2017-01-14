#!/usr/bin/env python
import json
import os
from pprint import pprint

with open('data.json') as data_file:    
    data = json.load(data_file)

print "Searching in:"+data['media_convert']['search_folder']
print "Send to:"+data['media_convert']['out_folder']
print "Convert audio to:"+data['media_convert']['audio_convert']
print "Convert video to:"+data['media_convert']['video_convert']


from converter import Converter
c = Converter()

for file in os.listdir(data['media_convert']['search_folder']):
    if file.endswith(".mp4"):
        print("found: "+file)


print "checking "+file+" to see if it needs converting"
info = c.probe(data['media_convert']['search_folder']+"/"+file)

video = info.video
audio = info.audio
print "~~~~~~~~~~~~~~~~~~~~~~Checking Video~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "video codec: "+str(video.codec)
print "video width: "+str(video.video_width)
print "video height: "+str(video.video_height)
print "video frames per second: "+str(video.video_fps)

print "~~~~~~~~~~~~~~~~~~~~~~Checking Audio~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print "audio codec: "+str(audio.codec)
print "bitrate: "+str(audio.bitrate)
print "Number of Channels: "+str(audio.audio_channels)


print ""
print "~~~~~~~~~~~~~~~~~~~~~~Checking what needs to be converted~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

print ""
print "~~~~~~~~~~~~~~~~~~~~~~Video~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

print "Video codec is "+str(video.codec)+" and is it the same as "+data['media_convert']['video_convert']

if str(video.codec) == data['media_convert']['video_convert']:
		print "Yes will set encode to copy"
		conv_video_codec='copy'
else:
	print "Nope setting it to "+data['media_convert']['video_convert']
	conv_video_codec = data['media_convert']['video_convert']

print ""
print "~~~~~~~~~~~~~~~~~~~~~~Audio~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

print "audio codec is "+str(audio.codec)+" and is it the same as "+data['media_convert']['audio_convert']

if str(audio.codec) == data['media_convert']['audio_convert']:
		print "Yes will set encode to copy"
		conv_audio_codec='copy'
else:
	print "Nope setting it to "+data['media_convert']['audio_convert']
	conv_audio_codec = data['media_convert']['audio_convert']


print ""
print "~~~~~~~~~~~~~~~~~~~~~~Starting the convert~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


conv = c.convert(data['media_convert']['search_folder']+"/"+file, data['media_convert']['out_folder']+"/"+file, {
    'format': 'mkv',
    'audio': {
        'codec': conv_audio_codec,
        'samplerate': audio.bitrate,
        'channels': audio.audio_channels
    },
    'video': {
        'codec': conv_video_codec,
        'width': video.video_width,
        'height': video.video_height,
        'fps': video.video_fps
    }})


for timecode in conv:
    print "Converting (%f) ...\r" % timecode

print "~~~~~~~~~~~~~~~~~~~~~~Removeing old file~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
os.remove(data['media_convert']['search_folder']+"/"+file)
