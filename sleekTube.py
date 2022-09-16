#!/usr/bin/env python
# importing packages
from email.policy import default
from tkinter import CENTER
import flet
import pytube
import os
import sys
from time import sleep
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
    ProgressBar,
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
        pathText.value = e.path if e.path else "Cancelled!"
        pathText.update()
        global base_dir
        base_dir = e.path + '/'

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    pathText = Text()
    page.overlay.extend([get_directory_dialog])

    def downloadAction(e):
        view.update()
        crtFolder(artist_name.value)
        if (frmt.value == 'mp3'):
            MP3_downloader()
        else:
            MP4_downloader()
        

    
        
    def MP4_downloader():
        if (url_type.value == 'channel'):
            c = pytube.Channel(url_id.value)
            status_view.controls.append(Text(f'Downloading videos from: {c.channel_name}' + ' channel'))
            status_view.controls.append(Text('Channel Contains:' + str(len(c.videos)) + ' videos', color=colors.BLUE))
            view.update()
            for cnt, video in zip(range(0, len(c.videos)), c.videos):
                video = video.streams.get_highest_resolution()
                destination = base_dir + artist_name.value
                fileSizeInBytes = video.filesize
                MaxFileSize = fileSizeInBytes/1024000
                MB = str(int(round(MaxFileSize))) + " MB"
                try:
                    pb = ProgressBar(width=400,color="blue")
                    tasks_view.controls.append(
                        Column(
                        controls=[
                            Text( str(cnt+1) + ' -->> ' + ' Downloading  ' + video.title, font_family=default),
                            Row([Text(value="↳"),pb,Text("File Size = " + MB, font_family=default)])]
                            )
                        )
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sf = int(round(MaxFileSize)) / 3
                        sleep(sf * 0.1)
                        view.update()

                    view.update()
                    video.download(output_path=destination)
                    tasks_view.controls.pop()
                    tasks_view.controls.append(Row(
                        controls=[st, Text(
                            str(cnt+1) + ' -->> ' + video.title + ' has been successfully downloaded.', font_family=default),
                            Text("File Size = " + MB, font_family=default)]
                    ))
                    view.update()
                    print(colored(video.title, 'cyan') + " has been successfully downloaded.")
                except:
                    pass
            status_view.controls.append(Row([Text(value="All Videos Downloaded Successfully", weight="bold")]))
            view.update()
        else:
            p = pytube.Playlist(url_id.value)
            status_view.controls.append(Text(f'Downloading videos from: {p.title}' + ' channel'))
            status_view.controls.append(Text('Playlis Contains:' + str(len(p.videos)) + ' videos', color=colors.BLUE))
            view.update()
            for cnt, video in zip(range(0, len(p.videos)), p.videos):
                video = video.streams.get_highest_resolution()
                destination = base_dir + artist_name.value
                fileSizeInBytes = video.filesize
                MaxFileSize = fileSizeInBytes/1024000
                MB = str(int(round(MaxFileSize))) + " MB"
                print("File Size = {:00.00f} MB".format(MaxFileSize))
                try:
                    pb = ProgressBar(width=400,color="blue")
                    tasks_view.controls.append(
                        Column(
                        controls=[
                            Text( str(cnt+1) + ' -->> ' + ' Downloading  ' + video.title, font_family=default),
                            Row([Text(value="↳"),pb,Text("File Size = " + MB, font_family=default)])]
                            )
                        )
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sf = int(round(MaxFileSize)) / 3
                        sleep(sf * 0.1)
                        view.update()

                    view.update()
                    video.download(output_path=destination)
                    tasks_view.controls.pop()
                    tasks_view.controls.append(Row(
                        controls=[st, Text(
                            str(cnt+1) + ' -->> ' + video.title + ' has been successfully downloaded.', font_family=default),
                            Text("File Size = " + MB, font_family=default)]
                    ))
                    view.update()
                    print(colored(video.title, 'cyan') + " has been successfully downloaded.")
                except:
                    pass
            status_view.controls.append(Row([Text(value="All Videos Downloaded Successfully", weight="bold")]))
            view.update()


    def MP3_downloader():
        if (url_type.value == 'channel'):
            c = pytube.Channel(url_id.value)
            status_view.controls.append(Text(f'Downloading videos from: {c.channel_name}' + ' channel'))
            status_view.controls.append(Text('Channel Contains:' + str(len(c.videos)) + ' videos', color=colors.BLUE))
            view.update()
            for cnt, video in zip(range(0, len(c.videos)), c.videos):
                try:
                    video1 = video.streams.get_highest_resolution()
                    destination = base_dir + artist_name.value
                    fileSizeInBytes = video1.filesize
                    MaxFileSize = fileSizeInBytes/1024000
                    MB = str(int(round(MaxFileSize))) + " MB"
                    pb = ProgressBar(width=400,color="blue")
                    tasks_view.controls.append(
                        Column(
                        controls=[
                            Text( str(cnt+1) + ' -->> ' + ' Downloading  ' + video.title, font_family=default),
                            Row([Text(value="↳"),pb,Text("File Size = " + MB, font_family=default)])]
                            )
                        )
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sleep(0.1)
                        view.update()

                    view.update()
                    destination = base_dir + artist_name.value
                    out_file = video.streams.filter(
                        only_audio=True).first().download(output_path=destination)
                    # save the file
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    tasks_view.controls.pop()
                    tasks_view.controls.append(Row(
                        controls=[st, Text(
                            str(cnt+1) + ' -->> ' + video.title + ' has been successfully downloaded.', font_family=default),
                            Text("File Size = " + MB, font_family=default)]
                    ))
                    view.update()
                    print(colored(video.title, 'cyan') + " has been successfully downloaded.")
                except:
                    pass
            status_view.controls.append(Row([Text(value="All Songs Downloaded Successfully", weight="bold")]))
            view.update()
        else:
            p = pytube.Playlist(url_id.value)
            status_view.controls.append(Text('<<<< Status >>>>', color=colors.BLUE))
            status_view.controls.append(Text(f'Downloading videos by: {p.title}' + ' playlist'))
            status_view.controls.append(Text('Playlist Contains:' + str(len(p.videos)) + ' videos', color=colors.BLUE))
            view.update()
            print(f'Downloading videos by: {p.title}' + ' playlist')
    
            for cnt, video in zip(range(0, len(p.videos)), p.videos):
                video1 = video.streams.get_highest_resolution()
                destination = base_dir + artist_name.value
                fileSizeInBytes = video1.filesize
                MaxFileSize = fileSizeInBytes/1024000
                MB = str(int(round(MaxFileSize))) + " MB"
                try:
                    pb = ProgressBar(width=400,color="blue")
                    tasks_view.controls.append(
                        Column(
                        controls=[
                            Text( str(cnt+1) + ' -->> ' + ' Downloading  ' + video.title, font_family=default),
                            Row([Text(value="↳"),pb,Text("File Size = " + MB, font_family=default)])]
                            )
                        )
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sleep(0.1)
                        view.update()

                    view.update()
                    destination = base_dir + artist_name.value
                    out_file = video.streams.filter(only_audio=True).first().download(output_path=destination)
                    # save the file
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    # result of success
                    tasks_view.controls.pop()
                    tasks_view.controls.append(
                        Row(
                        controls=[
                            st,
                            Text(str(cnt+1) + ' -->> ' + video.title + ' has been successfully downloaded.', font_family=default),
                            Text("File Size = " + MB, font_family=default)]
                            )
                        )
                    view.update()
                    print(str(cnt) +'-->>' + colored(video.title,'cyan') + " has been successfully downloaded.")
                except:
                    print('cant download')
                    pass
            status_view.controls.append(Row([Text(value="All Songs Downloaded Successfully", weight="bold")]))
            view.update()

    status_view = Column()
    tasks_view = ListView(expand=1, spacing=10, padding=1, auto_scroll=True)
    view = Column(
        spacing=5,
        expand=True,
        controls=[
            #1
                Row([Text(value="YT-Downloader", style="headlineMedium")],alignment="center"),
                
                #2
                Divider(),

                #3
                Row([Text(value="Download Location"), ElevatedButton("Open directory",icon=icons.FOLDER_OPEN,on_click=lambda _: get_directory_dialog.get_directory_path(),),pathText],alignment="center"),

                #4
                Divider(),

                #5
                Row(
                [
                Text(value="Artist or Folder Name"),
                artist_name,
                Text(value="Choose a Format :- "),
                frmt
                ],alignment="center"),

                #5
                Row(
                [
                url_type,
                url_id,
                ],alignment="center"),

                #7
                Row([ElevatedButton(text="Download", on_click=downloadAction,icon="download")], alignment="center"),

                #8
                Divider(),

                #9
                Container(
                    content = 
                    Row(
                        [
                            Column([Row([Text(value="Status")],alignment="center"),Divider(),status_view],width=230),
                            VerticalDivider(),
                            Column([Row([Text(value="Download Details")],alignment="center"),Divider(),tasks_view],spacing=0,expand=True)
                        ],
                            spacing=4
                        ),

                    bgcolor=colors.WHITE,
                    width=1360,
                    height=350,
                )

        ],
    )

    page.horizontal_alignment = "center"
    page.scroll = 'none'
    page.add(view)
    page.update()


flet.app(target=main)
