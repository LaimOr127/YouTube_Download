## Код для скачивания видео с Ютуба

from pytube import YouTube


def download_video(url):
    yt = YouTube(url)
    print("Доступные разрешения:")
    for stream in yt.streams:
        print(stream.resolution)

    resolution = input("Введите желаемое разрешение: ")
    video = yt.streams.filter(res=resolution).first()
    if video:
        video.download()
        print("Видео успешно загружено!")
    else:
        print("Неверное разрешение или видео недоступно в указанном разрешении.")


video_url = input("Введите URL видео на YouTube: ")
download_video(video_url)


