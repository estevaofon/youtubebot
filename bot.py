from __future__ import unicode_literals
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import os
import traceback
import youtube_dl

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

TOKEN = os.environ.get('TOKEN')
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    name = update.message.chat.first_name
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Olá {0}! Sou o baixador de youtube! \o/".format(name))
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

chat_inf = {}

def echo(bot, update):
    name = update.message.chat.first_name
    update.message.chat_id
    text = str(update.message.text)
    if "youtu" in text:
        youtube_link = update.message.text
        chat_inf[update.message.chat_id] = youtube_link
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Baixar música ou vídeo?")
    elif ("musica" in text.lower()) or ("música" in text.lower()) \
            or ("music" in text.lower()):
        music(bot, update, chat_inf[update.message.chat_id])
    elif ("video" in text.lower()) or ("vídeo" in text.lower()):
        video(bot, update, chat_inf[update.message.chat_id])
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Oi {0}!".format(name))
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Cole o seu link do youtube aqui.")
echo_handler = MessageHandler([Filters.text], echo)
dispatcher.add_handler(echo_handler)


@run_async
def music(bot, update, link):
    try:
        ydl_opts = {
            'outtmpl': '%(title)s.(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        title = ""
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Baixando...")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #ydl.download([link])
            info = ydl.extract_info(link, download=True)
            print('Title of the extracted video/playlist: %s' % info['title'])
            title = info['title']
            title = formating(title)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Enviando a você...")
        bot.sendAudio(chat_id=update.message.chat_id,
                      audio=open(title+'.mp3', 'rb'), title=title)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Concluído!")
        name = update.message.chat.first_name
        print(name+" downloaded "+title)
    except:
        traceback.print_exc()
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Desculpe, algo deu errado.")
    finally:
        if os.path.exists(title+'.mp3'):
            os.remove(title+'.mp3')


@run_async
def video(bot, update, link):
    try:
        ydl_opts = {
            'format': '18',
            'ext':'mp4',
            'outtmpl': '%(title)s.mp4'
        }
        title = ""
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Baixando...")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            #ydl.download([link])
            info = ydl.extract_info(link, download=True)
            print('Title of the extracted video/playlist: %s' % info['title'])
            title = info['title']
            title = formating(title)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Enviando a você...")
        bot.sendVideo(chat_id=update.message.chat_id,
                      video=open(title + '.mp4', 'rb'), title=title)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Concluído!")
        name = update.message.chat.first_name
        print(name+" downloaded "+title)
    except:
        traceback.print_exc()
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Desculpe, algo deu errado.")
    finally:
        if os.path.exists(title+'.mp4'):
            os.remove(title+'.mp4')


def formating(title):
    if ":" in title:
        title = title.replace(":", " -")
    if "?" in title:
        title = title.replace("?", "")
    if "/" in title:
        title = title.replace("/", "_")
    if "|" in title:
        title = title.replace("|", "_")
    if '"' in title:
        title = title.replace('"', "'")
    return title



def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Desculpe, não entendi esse comando.")
unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()
