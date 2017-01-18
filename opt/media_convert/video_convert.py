#!/usr/bin/env python
import json
import os
from pprint import pprint


###############Functions############
def vid_check ( vid_str ):
   print "checking "+str(vid_str)+" to see if it needs converting"
   info = c.probe(str(data['media_convert']['search_folder']+"/"+str(vid_str)))
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

   conv = c.convert(str(data['media_convert']['search_folder']+"/"+file), str(data['media_convert']['convert_folder']+"/"+file), {
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

   print "~~~~~~~~~~~~~~~~~~~~~~Checking~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
   print "checking "+str(file)+" to see if it needs converting"
   cinfo = c.probe(str(data['media_convert']['convert_folder']+"/"+file))
   print "~~will check if both videos lenths match~~"

   if int(info.format.duration) == int(cinfo.format.duration):
    print "Why yes they do match"
    print "~~~~~~~~~~~~~~~~~~~~~~Removeing non converted file~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Deleteing: "+file+" from "+data['media_convert']['search_folder']
    os.remove(data['media_convert']['search_folder']+"/"+file)
    os.rename(str(data['media_convert']['convert_folder']+"/"+file), str(data['media_convert']['out_folder']+"/"+file))
   else:
    print "Error found"
    print "Deleteing: "+file+" from "+data['media_convert']['convert_folder']
    os.remove(data['media_convert']['convert_folder']+"/"+file)
    return "false" 


   return "true"



#####################################################
with open('data.json') as data_file:    
    data = json.load(data_file)

from converter import Converter
c = Converter()

for file in os.listdir(data['media_convert']['search_folder']):
    if file.endswith(".mp4"):
        if vid_check(str(file)) == "true":
            print str(file)+" Converter no issues" 
        else:
            print str(file)+" Converter failed"