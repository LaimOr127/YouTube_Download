#Телеграмм бот для скачивания видео с Ютуба


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pytube import YouTube

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Отправь мне ссылку на видео на YouTube.")

def download_video(update, context):
    url = update.message.text
    yt = YouTube(url)
    resolutions = [stream.resolution for stream in yt.streams]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Доступные разрешения: {}".format(", ".join(resolutions)))
    context.user_data["url"] = url
    context.user_data["state"] = "resolution"

def select_resolution(update, context):
    resolution = update.message.text
    url = context.user_data["url"]
    yt = YouTube(url)
    video = yt.streams.filter(res=resolution).first()
    if video:
        video.download()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Видео успешно загружено!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверное разрешение или видео недоступно в указанном разрешении.")
    context.user_data.clear()

def cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Операция отменена.")
    context.user_data.clear()

def main():
    updater = Updater(token="YOUR_TOKEN", use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    download_handler = MessageHandler(Filters.regex(r"(https?://)?(www\.)?youtube\.com/watch\?v=\S+"), download_video)
    resolution_handler = MessageHandler(Filters.regex(r"\d+x\d+"), select_resolution)
    cancel_handler = CommandHandler("cancel", cancel)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(download_handler)
    dispatcher.add_handler(resolution_handler)
    dispatcher.add_handler(cancel_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()