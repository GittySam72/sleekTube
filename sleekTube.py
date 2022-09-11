#!/usr/bin/env python
# importing packages
from email.policy import default
from tkinter import CENTER
import flet
import pytube
import os
import sys
from termcolor import colored
from pytube import YouTube
import os
from flet import (
    Theme,
    FilePicker,
    Divider,
    VerticalDivider,
    FilePickerResultEvent,
    Checkbox,
    Column,
    FloatingActionButton,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Tab,
    Tabs,
    Text,
    TextField,
    UserControl,
    colors,
    icons,
    ElevatedButton,
    Radio,
    RadioGroup,
    Stack,
    ListTile,
    ListView,
    Card,
    TextButton,
    Image, Page, Row, Stack, Text,
    Icon,
    alignment,
    colors,
    Container
)

base_dir = '/home/greytesla/Desktop/Sam/Testing/'


def crtFolder(fldname):
    if (os.path.exists(os.path.join(base_dir, fldname))):
        pass
    else:
        path = os.path.join(base_dir, fldname)
        os.mkdir(path)


def main(page: Page):
    page.title = "YT-Downloader App"
    page.fonts = {
        "B6": "https://github.com/google/fonts/blob/main/ofl/b612mono/B612Mono-Bold.ttf",
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf"
    }
    page.theme = Theme(font_family="B6")
    page.horizontal_alignment = "center"
    artist_name = TextField(hint_text="Artist name? eg: - Justin Bieber")
    url_id = TextField(
        hint_text="URL? eg:- https://www.youtube.com/c/justinbieber/videos", disabled=True, width=600)

    def radiogroup_changed(e):
        url_id.disabled = False
        page.update()

    frmt = RadioGroup(content=Row([
        Radio(value="mp3", label="MP3"),
        Radio(value="mp4", label="MP4")]))

    st = Row(
        controls=[
            Image(
                src=f"https://www.pngitem.com/pimgs/m/302-3024199_instagram-verified-symbol-png-instagram-verified-logo-png.png",
                width=24,
                height=24,
                fit="contain",
            )
        ]
    )

    url_type = RadioGroup(content=Column([
        Radio(value="channel", label="Channel"),
        Radio(value="playlist", label="Playlist")], spacing=5), on_change=radiogroup_changed)

    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()
        global base_dir
        base_dir = e.path + '/'

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()
    page.overlay.extend([get_directory_dialog])

    def add_clicked(e):
        view.update()
        crtFolder(artist_name.value)
        if (frmt.value == 'mp3'):
            MP3_downloader()
        else:
            MP4_downloader()
        status_view.controls.append(
            Row([Text(value="All Songs Downloaded Successfully", weight="bold")]))
        view.update()

    def MP4_downloader():
        if (url_type.value == 'channel'):
            c = pytube.Channel(url_id.value)
            status_view.controls.append(
                Text('<<<< Status >>>>', color=colors.BLUE))
            status_view.controls.append(
                Text(f'Downloading videos from: {c.channel_name}' + ' channel'))
            status_view.controls.append(Text(
                'Channel Contains:' + str(len(c.videos)) + ' videos', color=colors.BLUE))
            view.update()
            tasks_view.controls.append(
                Text('<<<< Download Details >>>>', color=colors.BLUE))
            print(f'Downloading videos from Channel: {c.channel_name}')
            for cnt, video in zip(range(0, len(c.videos)), c.videos):
                try:
                    destination = base_dir + artist_name.value
                    video.streams.get_highest_resolution().download(output_path=destination)
                    tasks_view.controls.append(Row(
                        controls=[st, Text(
                            str(cnt+1) + ' -->> ' + video.title + ' has been successfully downloaded.', font_family=default)]
                    ))
                    view.update()
                    print(colored(video.title, 'cyan') +
                          " has been successfully downloaded.")
                except:
                    pass
        else:
            p = pytube.Playlist(id)
            status_view.controls.append(
                Text('<<<< Status >>>>', color=colors.BLUE))
            status_view.controls.append(
                Text(f'Downloading videos from: {p.title}' + ' channel'))
            status_view.controls.append(Text(
                'Channel Contains:' + str(len(p.videos)) + ' videos', color=colors.BLUE))
            view.update()
            tasks_view.controls.append(
                Text('<<<< Download Details >>>>', color=colors.BLUE))
            print(f'Downloading videos from Channel: {c.channel_name}')
            for cnt, video in zip(range(0, len(p.videos)), p.videos):
                try:
                    destination = base_dir + artist_name.value
                    video.streams.get_highest_resolution().download(output_path=destination)
                    tasks_view.controls.append(Row(
                        controls=[st, Text(
                            str(cnt+1) + ' -->> ' + video.title + ' has been successfully downloaded.', font_family=default)]
                    ))
                    view.update()
                    print(colored(video.title, 'cyan') +
                          " has been successfully downloaded.")
                except:
                    pass

    def MP3_downloader():
        if (url_type.value == 'channel'):
            c = pytube.Channel(url_id.value)
            status_view.controls.append(
                Text('<<<< Status >>>>', color=colors.BLUE))
            status_view.controls.append(
                Text(f'Downloading videos from: {c.channel_name}' + ' channel'))
            status_view.controls.append(Text(
                'Channel Contains:' + str(len(c.videos)) + ' videos', color=colors.BLUE))
            view.update()
            tasks_view.controls.append(
                Text('<<<< Download Details >>>>', color=colors.BLUE))
            print(f'Downloading videos from Channel: {c.channel_name}')
            for cnt, video in zip(range(0, len(c.videos)), c.videos):
                try:
                    destination = base_dir + artist_name.value
                    out_file = video.streams.filter(
                        only_audio=True).first().download(output_path=destination)
                    # save the file
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    tasks_view.controls.append(Row(
                        controls=[st, Text(
                            str(cnt+1) + ' -->> ' + video.title + ' has been successfully downloaded.', font_family=default)]
                    ))
                    view.update()
                    print(colored(video.title, 'cyan') +
                          " has been successfully downloaded.")
                except:
                    pass
        else:
            p = pytube.Playlist(url_id.value)
            status_view.controls.append(
                Text('<<<< Status >>>>', color=colors.BLUE))
            status_view.controls.append(
                Text(f'Downloading videos by: {p.title}' + ' playlist'))
            status_view.controls.append(Text(
                'Playlist Contains:' + str(len(p.videos)) + ' videos', color=colors.BLUE))
            view.update()
            print(f'Downloading videos by: {p.title}' + ' playlist')
            tasks_view.controls.append(
                Text('<<<< Download Details >>>>', color=colors.BLUE))
            for cnt, video in zip(range(0, len(p.videos)), p.videos):
                try:
                    destination = base_dir + artist_name.value
                    out_file = video.streams.filter(
                        only_audio=True).first().download(output_path=destination)
                    # save the file
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    # result of success
                    # result of success
                    tasks_view.controls.append(Row(
                        controls=[st, Text(
                            str(cnt+1) + ' -->> ' + video.title + ' has been successfully downloaded.', font_family=default)]
                    ))
                    view.update()
                    # print(str(cnt) +'-->>' + colored(video.title,'cyan') + " has been successfully downloaded.")
                except:
                    print('cant download')
                    pass

    status_view = Column()
    tasks_view = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
    view = Column(
        spacing=5,
        expand=True,
        controls=[
            Row([Text(value="YT-Downloader", style="headlineMedium")],
                alignment="center"),

            Row([Text(value="Download Location"), ElevatedButton(
                "Open directory",
                icon=icons.FOLDER_OPEN,
                on_click=lambda _: get_directory_dialog.get_directory_path(),
                disabled=page.web,
            ),
                directory_path], alignment="center"),
            Divider(),
            Row(
                controls=[
                    Text(value="Artist or Folder Name"),
                    artist_name,
                    Text(value="Choose a Format :- "),
                    frmt
                ],
                spacing=15,
                alignment=CENTER
            ),

            Row(
                controls=[
                    url_type,
                    url_id,
                ],
                spacing=15,
                alignment=CENTER,

            ),


            Row([ElevatedButton(text="Download", on_click=add_clicked,
                icon="download")], alignment="center"),
            Divider(),
            Row(
                [
                    Container(
                        content=status_view,
                        alignment=alignment.center,
                    ),
                    VerticalDivider(),
                    Row([tasks_view], spacing=0),
                ],
                spacing=0,
                expand=True,
            ),
            Row(

                controls=[Text('made with \u2764\ufe0f by SAM'),
                          ],
            ),

        ],
    )

    page.horizontal_alignment = "center"
    page.scroll = 'none'
    page.add(view)
    page.update()


flet.app(target=main)
