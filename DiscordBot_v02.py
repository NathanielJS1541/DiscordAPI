#####################################################
#                                                                                                                                     #
#                                             __PREREQUISUTES__                                                 #
#                                                                                                                                     #
# - You must use pip3 to install discord.py                                                          #
# - You must have installed espeak on the computer                                        #
#   and have added espeak to your PATH, to allow it                                          #
#   to be run from command prompt.                                                                    #
# - You must have created a Giphy API at                                                              #
#   https://developers.giphy.com/                                                                          #
#   and then add the URL to this where relevant.                                                #
# - You must have made a Discord API at                                                              #
#   https://discordapp.com/developers/                                                               #
#   and then add the token to this where relevant.                                             #
# - To use admin commands you must find all                                                     #
#   instances where the ID is checked and replace                                              #
#   it with your user ID.                                                                                              #
# - Change all directories within the code to                                                      #
#   actual directories on your machine.                                                                 #
#                                                                                                                                     #
#####################################################

import discord
import random
import time
import subprocess
import threading
import os
import urllib.request
import json
from pathlib import Path
from datetime import datetime
from datetime import datetime,timedelta
import os

global player
global voice_client
global voice_channel
global old_voice_members
global volume
volume  = 60/100 #Use this to change the bot's voice volume
global adminID
adminID = "" #Change this to your ID if you are going to admin this Bot.
global filePath
filePath = "" #This is the file path to your "Voice Files" folder, within the DiscordBot folder.
global apiToken
apiToken = "" #Your Discord Bot's API
global apiID
apiID = "" #Your Discord Bot's ID
global gifyApi
difyApi = "" #URL for your Gify API
client = discord.Client()

def member_change():
  global old_voice_members
  global player
  if not (len(old_voice_members) == len(voice_channel.voice_members)):
    if(len(old_voice_members) > len(voice_channel.voice_members)):
      for i in range(0, len(old_voice_members)):
        if old_voice_members[i] not in voice_channel.voice_members:
          name = old_voice_members[i].display_name
          old_voice_members = []
          for k in range(0, len(voice_channel.voice_members)):
            old_voice_members.append(voice_channel.voice_members[k])
          if(name.startswith("(")):
            parindex = name.find(")")
            name = name[parindex+1:]
          file_name = filePath+name+".wav"
          print(name + "left the channel.")
          if Path(file_name).is_file():
            player = voice_client.create_ffmpeg_player(file_name)
            player.volume= volume #Change the left number to adjust over all volume
            player.start()
            while(not player.is_done()):
              count = 0
            player = voice_client.create_ffmpeg_player(filePath + "left.wav")
            player.volume= volume
            player.start()
            while(not player.is_done()):
              waitCount = 0
          else:
            textToWav(name,file_name)
            player = voice_client.create_ffmpeg_player(filePath+"name"+".wav")
            player.volume= volume
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player(filePath + "left.wav")
            player.volume= volume
            player.start()
            while(not player.is_done()):
              waitCount = 0
          break
    elif(len(voice_channel.voice_members) > len(old_voice_members)):
      for i in range(0, len(voice_channel.voice_members)):
        if voice_channel.voice_members[i] not in old_voice_members:
          name = voice_channel.voice_members[i].display_name
          old_voice_members = []
          for k in range(0, len(voice_channel.voice_members)):
            old_voice_members.append(voice_channel.voice_members[k])
          if(name.startswith("(")):
            parindex = name.find(")")
            name = name[parindex+1:]
          file_name = filePath+name+".wav"
          print(name + " joined the channel.")
          if Path(file_name).is_file():
            player = voice_client.create_ffmpeg_player(file_name)
            player.volume= volume
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player(filePath + "joined.wav")
            player.volume= volume
            player.start()
            while(not player.is_done()):
              waitCount = 0
          else:
            textToWav(name,file_name)
            player = voice_client.create_ffmpeg_player(filePath+name+".wav")
            player.volume= volume
            player.start()
            while(not player.is_done()):
              waitCount = 0
            player = voice_client.create_ffmpeg_player(filePath + "left.wav")
            player.volume= volume
            player.start()
            while(not player.is_done()):
              waitCount = 0
          break
  threading.Timer(.5, member_change).start()


def textToWav(text, file_name):
  try:
    subprocess.call(["espeak", "-vf2", "-w", file_name, text]) #Change "f2" to a voice file in ~/espeak/espeak-data/voice to change the voice
    print(" [ OK ] File written")
  except:
    print(" [ ERR ] File writing failed.")

async def giphy_command(message):
  forbidden_gifs = ["/gamerescape", "/xivdb", "/giphy", "/tts", "/tenor", "/me", "/tableflip", "/unflip", "/shrug", "/nick"]
  spaceIndex = message.content.find(" ")
  if message.content[:spaceIndex] in forbidden_gifs:
    return
  search_params = message.content[1:]
  search_params_sb = ""
  first = True
  for i in range(0,len(search_params)):
    if search_params[i] == " ":
      search_params_sb = search_params_sb + search_params[len(search_params_sb):i] + "+"
  search_params_sb = search_params_sb + search_params[len(search_params_sb):]
  #Change these to your own Giphy API URLs. but make sure shearch_params_sb is in the correct place.
  data = json.loads(urllib.request.urlopen(difyApi+search_params_sb+"&limit=10&offset=0&rating=R&lang=en").read().decode("utf-8")) #Add your own giphy API here key
  try:
    url = json.dumps(data["data"][random.randint(0,4)]["url"], sort_keys = True, indent = 4)
    await client.send_message(message.channel, url[1:len(url)-1])
  except:
    try:
      data = json.loads(urllib.request.urlopen(difyApi+search_params_sb+"&rating=R"))
      url = json.dumps(data["data"][0]["url"], sort_keys = True, incident = 4)
      await client.send_message(message.channel, url[1:len(url)-1])
    except:
      await client.send_message(message.channel, "No Gif found.")

async def join_voice(channel_id):
  global player
  global voice_client
  global voice_channel
  global old_voice_members
  print(" [ OK ] Attempting to join voice channel with ID: " + channel_id)
  try:
    voice_channel = client.get_channel(channel_id)
    voice = await client.join_voice_channel(voice_channel)
    player = voice.create_ffmpeg_player(filePath + "init.wav")
    voice_client = voice
    old_voice_members = []
    for i in range(0, len(voice_channel.voice_members)):
      old_voice_members.append(voice_channel.voice_members[i])
    member_change()
  except:
    print(" [ ERR ] Failed to join voice channel with ID: " + channel_id)

async def ping_command(message):
  d = message.timestamp - datetime.utcnow()
  s = d.seconds*1000 + d.microseconds/1000
  await client.send_message(message.channel, "Ping: {}ms".format(s))

async def help_command(message):
  channel = message.channel
  help_message = """Here are list of available commands:
< !help >:                              *Displays a list of available commands*
< !status >:                           *Replies indicating I am online*
< !voice [channel_id] >: ~ *Joins voice channel with specified Id*
< !ping >:                              *Responds with your ping*
< !stopvoice >:                 ~ *Disconnects the bot from the current voice channel*
< !clean [amount] >:       ~ *Removes all messages from this channel sent or intended for me*
< /[emote] >:                       *Search and post a gif.*
< !shutdown >:                 ~ *Logs the bot off.*

~ = special premissions required.

Last updated 25/05/2018"""
  await client.send_message(channel, help_message)

async def stop_voice(message):
  global voice_client
  await voice_client.disconnect()

async def reddit_link(message):
  await client.send_message(message.channel, "http://www.reddit.com"+message.content)

async def clean_command(message):
  channel = message.channel
  options = [channel, 50000, delete_message, message, None, None]
  #This should contain the author ID of your bot.
  await client.purge_from(channel, limit = 100, check=lambda m: m.author.id == apiID or m.content.startswith("!") or m.content.startswith("/"))

def delete_message(message):
  return False
  #if(message.author.id == "" or message.content.startswith("!")):
   # return True

@client.event
async def on_ready():
    print(" [ OK ] Login Successful.")
    print(" [ OK ] Name: " + client.user.name)
    print(" [ OK ] ID: " + client.user.id)
    print()
    if not os.path.exists("VoiceFiles"):
      os.makedirs("VoiceFiles")
    if( not (Path(filePath + "joined.wav").is_file())):
      textToWav("Has joined the channel", filePath + "joined.wav")
    if( not (Path(filePath + "left.wav").is_file())):
      textToWav("Has left the channel", filePath + "left.wav")
    if( not (Path(filePath + "init.wav").is_file())):
      textToWav("init", filePath + "init.wav")

@client.event
async def on_message(message):
  if(message.author != client.user):
    print(message.author.name + " said: \"" + message.content + "\" in #" + message.channel.name + " @ " + time.ctime())
  if(message.content.startswith("!voice")):
    if(message.author.id == adminID):
      if(len(message.content) < len("!voice ")):
        await client.send_message(message.channel, "Please provide a voice channel id")
        print(" [ ERR ] No channel ID specified.")
        return
      channelId = message.content[len("!voice "):]
      await client.send_message(message.channel, "Joining voice channel with\nID: " + channelId +"\nName: " + client.get_channel(channelId).name)
      await join_voice(channelId)
      print(" [ OK ] Successfully joined channel with ID: " + channelID)
    else:
      count = 0
      await client.send_message(message.channel, "Sorry, you do not have permission to use this command.")
  elif(message.content.startswith("!status")):
    await client.send_message(message.channel, "[ OK ] Client service running.\n[ OK ] Client logged in as: " + client.user.name + "\n[ OK ] Network Active.")
  elif(message.content.startswith("!help")):
    await help_command(message)
  elif(message.content.startswith("!ping")):
    await ping_command(message)
  elif(message.content.startswith("!stopvoice")):
    if(message.author.id == adminID):
      await stop_voice(message)
  elif(message.content.startswith("/r/")):
    await reddit_link(message)
  elif(message.content.startswith("!clean")):
    if(message.author.id == adminID):
      await clean_command(message)
    else:
      await client.send_message(message.channel, "Sorry, you do not have permission to use this command.")
  elif(message.content.startswith("/")):
    await giphy_command(message)
  elif(message.content.startswith("!shutdown")):
    if(message.author.id == adminID):
      await client.send_message(message.channel, "Logging out...")
      print(" [ OK ] Shutdown initiated")
      try:
        await stop_voice("stopvoice")
      except:
        print(" [ ERR ] Voice service not running.")
      client.logout()
      print(" [ OK ] Shutdown successful. Service gracefully terminated.")
      os._exit(0)
    else:
      await client.send_message(message.channel, "Sorry, you do not have permission to use this command.")

client.run(apiToken) #Add your own bot's token here
