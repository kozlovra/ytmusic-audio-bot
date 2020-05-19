import io, os, time
from pytube import YouTube
from bot.bot import Bot
from bot.handler import MessageHandler

bot = Bot(token=os.environ['TOKEN'])

def message_cb(bot, event):
    link = event.text

    YouTube(link).streams.get_highest_resolution().download()
    yt = YouTube(link)
    filetitle = yt.title.replace('.','')
    filename = filetitle.replace(',','')

    yt.streams.filter(only_audio=True, mime_type='audio/mp4').order_by('abr')[-0].download()

    os.rename(f'{filename}.mp4', f'{filename}.m4a')

    ytsound = open(f'{filename}.m4a', 'rb')

    bot.send_file(chat_id=event.from_chat, file=ytsound)

    ytsound.close()
    os.remove(f'{filename}.m4a')

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()