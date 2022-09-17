#!/usr/bin/env python
# importing packages
from email.policy import default
from operator import index
from tkinter import CENTER, N
from turtle import bgcolor
import flet
import pytube
import threading
import os
import sys
from PIL import Image as mage
import requests
from io import BytesIO
from time import sleep
from termcolor import colored
from pytube import YouTube
import os
from flet import (
    Theme,
    margin,
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
    AlertDialog,
    Radio,
    RadioGroup,
    ListTile,
    ListView,
    Card,
    TextButton,
    Image,
    Stack,
    alignment,
    colors,
    ProgressBar,
    Container,
    Column,
    FloatingActionButton,
    Icon,
    NavigationRail,
    NavigationRailDestination,
    ProgressRing
)

base_dir = '/home/greytesla/Desktop/Sam/Testing/'


def crtFolder(fldname):
    if (os.path.exists(os.path.join(base_dir, fldname))):
        pass
    else:
        path = os.path.join(base_dir, fldname)
        os.mkdir(path)


def main(page: Page):
    page.title = "SleekTube - YT-Downloader App"
    page.fonts = {
        "B6": "https://github.com/google/fonts/blob/main/ofl/b612mono/B612Mono-Bold.ttf",
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf"
    }
    page.theme = Theme(font_family="B6")
    page.horizontal_alignment = "center"
    bulk_artist_name = TextField(hint_text="Artist name? eg: - Justin Bieber")
    bulk_url_id = TextField(
        hint_text="URL? eg:- https://www.youtube.com/c/justinbieber/videos", disabled=True, width=600)
    single_url_id = TextField(
        hint_text="URL? eg:- https://www.youtube.com/watch?v=shSUDi4b2y8", width=600)

    def viewDecider(n):
        viewList = [single_mainView_1, bulk_mainView_2, settings_mainView_3]
        rails = [single_view_rail, bulk_view_rail, settings_view_rail]
        rails[n].selected_index = n
        for v in viewList:
            if v != viewList[n]:
                v.visible = False
                page.update()
            else:
                v.visible = True
                page.update()

    single_view_rail = NavigationRail(
        selected_index=0,
        label_type="all",
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=FloatingActionButton(icon=icons.DOWNLOADING, text="sleekTube"),
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=icons.DONE_OUTLINED, selected_icon=icons.DONE, label="SoloMode"
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.DONE_ALL_ROUNDED),
                selected_icon_content=Icon(icons.DONE_ALL),
                label="BulkMode",
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED,
                selected_icon_content=Icon(icons.SETTINGS),
                label_content=Text("Settings"),
            ),
        ],
        on_change=lambda e: viewDecider(e.control.selected_index),
    )

    bulk_view_rail = NavigationRail(
        selected_index=1,
        label_type="all",
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=FloatingActionButton(icon=icons.DOWNLOADING, text="sleekTube"),
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=icons.DONE_OUTLINED, selected_icon=icons.DONE, label="SoloMode"
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.DONE_ALL_ROUNDED),
                selected_icon_content=Icon(icons.DONE_ALL),
                label="BulkMode",
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED,
                selected_icon_content=Icon(icons.SETTINGS),
                label_content=Text("Settings"),
            ),
        ],
        on_change=lambda e: viewDecider(e.control.selected_index),
    )

    settings_view_rail = NavigationRail(
        selected_index=2,
        label_type="all",
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=FloatingActionButton(icon=icons.DOWNLOADING, text="sleekTube"),
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=icons.DONE_OUTLINED, selected_icon=icons.DONE, label="SoloMode"
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.DONE_ALL_ROUNDED),
                selected_icon_content=Icon(icons.DONE_ALL),
                label="BulkMode",
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED,
                selected_icon_content=Icon(icons.SETTINGS),
                label_content=Text("Settings"),
            ),
        ],
        on_change=lambda e: viewDecider(e.control.selected_index),
    )

    def bulk_url_state_changer(e):
        bulk_url_id.disabled = False
        page.update()

    downloadFormat = RadioGroup(content=Row([
        Radio(value="mp3", label="MP3"),
        Radio(value="mp4", label="MP4")]))

    bulk_status_verified_logo = Row(
        controls=[
            Image(
                src=f"https://www.pngitem.com/pimgs/m/302-3024199_instagram-verified-symbol-png-instagram-verified-logo-png.png",
                width=24,
                height=24,
                fit="contain",
            )
        ]
    )

    bulk_url_type = RadioGroup(content=Column([
        Radio(value="channel", label="Channel"),
        Radio(value="playlist", label="Playlist")], spacing=5), on_change=bulk_url_state_changer)

    def get_directory_result(e: FilePickerResultEvent):
        pathText.value = e.path if e.path else "Cancelled!"
        pathText.update()
        global base_dir
        base_dir = e.path + '/'

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    pathText = Text()
    page.overlay.extend([get_directory_dialog])

    def downloadActionForSingle(e):
        # single_status_thumbnail.controls.pop()
        # single_download_status.controls.pop()
        # page.update()
        onSingleDownloadThread()

    def downloadActionForBulk(e):
        bulkViewMode.update()
        crtFolder(bulk_artist_name.value)
        if (downloadFormat.value == 'mp3'):
            bulk_MP3_downloader()
        else:
            bulk_MP4_downloader()

    pr = ProgressRing(stroke_width=2)

    dlg = AlertDialog(
        title=Text("Parsing Data", text_align='center'), on_dismiss=lambda e: print("Dialog dismissed!"),
        content=pr
    )

    def viewDlg():
        page.dialog = dlg
        dlg.open = True
        page.update()
        sleep(3)
        dlg.open = False
        single_status.visible = True
        page.update()

    def onSingleDownloadThread():
        threading.Thread(target=viewDlg).start()
        threading.Thread(target=singleDownloader).start()

    def singleDownloader():
        if (downloadFormat.value == 'mp3'):
            try:
                yt = YouTube(single_url_id.value)
                video = yt.streams.filter(only_audio=True).first()
                single_video_name.value = video.title
                single_video_length.value = str(
                    int(yt.length / 60)) + " Minute"
                fileSizeInBytes = video.filesize
                MaxFileSize = fileSizeInBytes/1024000
                single_video_size.value = str(int(round(MaxFileSize))) + " MB"
                single_video_quality.value = "128Hz"
                single_video_format.value = "MP3"
                single_video_link.value = single_url_id.value
                single_video_folder.value = base_dir
                single_status.update()
                pb = ProgressBar(width=400, color='blue',
                                 bgcolor=colors.BLACK87)
                video = yt.streams.filter(only_audio=True).first()
                destination = base_dir + bulk_artist_name.value
                MB = str(int(round(MaxFileSize))) + " MB"
                cnt = 1
                url = yt.thumbnail_url
                tImage = Image(
                    src=url,
                    width=500,
                    height=300,
                    fit="fill"
                )
                single_status_thumbnail.controls.append(tImage)
                single_status_thumbnail.controls.append(
                    Row(

                        controls=[
                            Column([Text(str(cnt) + '  ' + u"\u27F6" + '   Downloading  ' + yt.title, font_family=default),
                                    Row([Text(value="↳"), pb, Text(
                                        "| File Size = " + MB, font_family=default)])
                                    ])],
                        spacing=0
                    )
                )
                singleModeView.update()
                destination = base_dir

                def downMp3():
                    out_file = yt.streams.filter(
                        only_audio=True).first().download(output_path=destination)
                    # save the file
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)

                def updatePB():
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sf = int(round(MaxFileSize)) / 2
                        sleep(sf * 0.1)
                        singleModeView.update()
                threading.Thread(target=downMp3).start()
                threading.Thread(target=updatePB).start()

            except:
                pass
        else:
            try:
                yt = YouTube(single_url_id.value)
                video = yt.streams.get_highest_resolution()
                single_video_name.value = video.title
                single_video_length.value = str(
                    int(yt.length / 60)) + " Minute"
                fileSizeInBytes = video.filesize
                MaxFileSize = fileSizeInBytes/1024000
                single_video_size.value = str(int(round(MaxFileSize))) + " MB"
                single_video_quality.value = "1080P"
                single_video_format.value = "MP4"
                single_video_link.value = single_url_id.value
                single_video_folder.value = base_dir
                single_status.update()
                pb = ProgressBar(width=400, color='blue',
                                 bgcolor=colors.BLACK87)
                video = yt.streams.get_highest_resolution()
                destination = base_dir + bulk_artist_name.value
                fileSizeInBytes = video.filesize
                MaxFileSize = fileSizeInBytes/1024000
                MB = str(int(round(MaxFileSize))) + " MB"
                cnt = 1
                url = yt.thumbnail_url
                tImage = Image(
                    src=url,
                    width=500,
                    height=300,
                    fit="fill"
                )
                single_status_thumbnail.controls.append(tImage)
                single_status_thumbnail.controls.append(
                    Row(
                        controls=[
                            Column([Text(str(cnt) + '  ' + u"\u27F6" + '   Downloading  ' + yt.title, font_family=default),
                                    Row([Text(value="↳"), pb, Text(
                                        "| File Size = " + MB, font_family=default)])
                                    ])],
                        spacing=0
                    )
                )
                singleModeView.update()
                destination = base_dir

                def downMp4():
                    yt.streams.get_highest_resolution().download(destination)

                def updatePB():
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sf = int(round(MaxFileSize)) / 12
                        sleep(sf * 0.1)
                        singleModeView.update()
                threading.Thread(target=downMp4).start()
                threading.Thread(target=updatePB).start()

            except:
                pass

    def bulk_MP4_downloader():
        if (bulk_url_type.value == 'channel'):
            c = pytube.Channel(bulk_url_id.value)
            bulk_status_view.controls.append(
                Text(f'Downloading videos from: {c.channel_name}' + ' channel'))
            bulk_status_view.controls.append(
                Text('Channel Contains:' + str(len(c.videos)) + ' videos', color=colors.BLUE))
            bulkViewMode.update()
            for cnt, video in zip(range(0, len(c.videos)), c.videos):
                url = video.thumbnail_url
                tImage = Image(
                    src=url,
                    width=220,
                    height=120,
                    fit="fill",
                )
                video = video.streams.get_highest_resolution()
                destination = base_dir + bulk_artist_name.value
                fileSizeInBytes = video.filesize
                MaxFileSize = fileSizeInBytes/1024000
                MB = str(int(round(MaxFileSize))) + " MB"
                try:
                    pb = ProgressBar(width=400, color="blue",
                                     bgcolor=colors.BLACK87)
                    bulk_status_view.controls.append(tImage)
                    bulk_tasks_view.controls.append(
                        Row(
                            controls=[
                                Column([Text(str(cnt+1) + '  ' + u"\u27F6" + '   Downloading  ' + video.title, font_family=default),
                                        Row([Text(value="↳"), pb, Text(
                                            "File Size = " + MB, font_family=default)])
                                        ])],
                            spacing=0
                        )
                    )
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sf = int(round(MaxFileSize)) / 2
                        sleep(sf * 0.1)
                        bulkViewMode.update()

                    bulkViewMode.update()
                    video.download(output_path=destination)
                    bulk_tasks_view.controls.pop()
                    bulk_tasks_view.controls.append(Row(
                        controls=[bulk_status_verified_logo, Text(
                            str(cnt+1) + '  ' + u"\u27F6" + '  ' + video.title + ' has been successfully downloaded.', font_family=default),
                            Text("File Size = " + MB, font_family=default)]
                    ))
                    bulk_status_view.controls.remove(tImage)
                    bulkViewMode.update()
                    print(colored(video.title, 'cyan') +
                          " has been successfully downloaded.")
                except:
                    pass
            bulk_status_view.controls.append(
                Row([Text(value="All Videos Downloaded Successfully", weight="bold")]))
            bulkViewMode.update()
        else:
            p = pytube.Playlist(bulk_url_id.value)
            bulk_status_view.controls.append(
                Text(f'Downloading videos from: {p.title}' + ' channel'))
            bulk_status_view.controls.append(
                Text('Playlis Contains:' + str(len(p.videos)) + ' videos', color=colors.BLUE))
            bulkViewMode.update()
            for cnt, video in zip(range(0, len(p.videos)), p.videos):
                video = video.streams.get_highest_resolution()
                destination = base_dir + bulk_artist_name.value
                fileSizeInBytes = video.filesize
                MaxFileSize = fileSizeInBytes/1024000
                MB = str(int(round(MaxFileSize))) + " MB"
                print("File Size = {:00.00f} MB".format(MaxFileSize))
                try:
                    pb = ProgressBar(width=400, color="blue",
                                     bgcolor=colors.BLACK87)
                    bulk_tasks_view.controls.append(
                        Column(
                            controls=[
                                Text(str(cnt+1) + '  ' + u"\u27F6" +
                                     '   Downloading  ' + video.title, font_family=default),
                                Row([Text(value="↳"), pb, Text("File Size = " + MB, font_family=default)])]
                        )
                    )
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sf = int(round(MaxFileSize)) / 2
                        sleep(sf * 0.1)
                        bulkViewMode.update()

                    bulkViewMode.update()
                    video.download(output_path=destination)
                    bulk_tasks_view.controls.pop()
                    bulk_tasks_view.controls.append(Row(
                        controls=[bulk_status_verified_logo, Text(
                            str(cnt+1) + '  ' + u"\u27F6" + '  ' + video.title + ' has been successfully downloaded.', font_family=default),
                            Text("File Size = " + MB, font_family=default)]
                    ))
                    bulkViewMode.update()
                    print(colored(video.title, 'cyan') +
                          " has been successfully downloaded.")
                except:
                    pass
            bulk_status_view.controls.append(
                Row([Text(value="All Videos Downloaded Successfully", weight="bold")]))
            bulkViewMode.update()

    def bulk_MP3_downloader():
        if (bulk_url_type.value == 'channel'):
            c = pytube.Channel(bulk_url_id.value)
            bulk_status_view.controls.append(
                Text(f'Downloading videos from: {c.channel_name}' + ' channel'))
            bulk_status_view.controls.append(
                Text('Channel Contains:' + str(len(c.videos)) + ' videos', color=colors.BLUE))
            bulkViewMode.update()
            for cnt, video in zip(range(0, len(c.videos)), c.videos):
                try:
                    video1 = video.streams.filter(only_audio=True).first()
                    destination = base_dir + bulk_artist_name.value
                    fileSizeInBytes = video1.filesize
                    MaxFileSize = fileSizeInBytes/1024000
                    MB = str(int(round(MaxFileSize))) + " MB"
                    pb = ProgressBar(width=400, color="blue",
                                     bgcolor=colors.BLACK87)
                    bulk_tasks_view.controls.append(
                        Column(
                            controls=[
                                Text(str(cnt+1) + '  ' + u"\u27F6" +
                                     '   Downloading  ' + video.title, font_family=default),
                                Row([Text(value="↳"), pb, Text("File Size = " + MB, font_family=default)])]
                        )
                    )
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sf = int(round(MaxFileSize)) / 3
                        sleep(sf * 0.1)
                        bulkViewMode.update()

                    bulkViewMode.update()
                    destination = base_dir + bulk_artist_name.value
                    out_file = video.streams.filter(
                        only_audio=True).first().download(output_path=destination)
                    # save the file
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    bulk_tasks_view.controls.pop()
                    bulk_tasks_view.controls.append(Row(
                        controls=[bulk_status_verified_logo, Text(
                            str(cnt+1) + '  ' + u"\u27F6" + '  ' + video.title + ' has been successfully downloaded.', font_family=default),
                            Text("File Size = " + MB, font_family=default)]
                    ))
                    bulkViewMode.update()
                    print(colored(video.title, 'cyan') +
                          " has been successfully downloaded.")
                except:
                    pass
            bulk_status_view.controls.append(
                Row([Text(value="All Songs Downloaded Successfully", weight="bold")]))
            bulkViewMode.update()
        else:
            p = pytube.Playlist(bulk_url_id.value)
            bulk_status_view.controls.append(
                Text('<<<< Status >>>>', color=colors.BLACK87))
            bulk_status_view.controls.append(
                Text(f'Downloading videos by: {p.title}' + ' playlist'))
            bulk_status_view.controls.append(
                Text('Playlist Contains:' + str(len(p.videos)) + ' videos', color=colors.BLUE))
            bulkViewMode.update()
            print(f'Downloading videos by: {p.title}' + ' playlist')

            for cnt, video in zip(range(0, len(p.videos)), p.videos):
                try:
                    video1 = video.streams.filter(only_audio=True).first()
                    destination = base_dir + bulk_artist_name.value
                    fileSizeInBytes = video1.filesize
                    MaxFileSize = fileSizeInBytes/1024000
                    MB = str(int(round(MaxFileSize))) + " MB"
                    pb = ProgressBar(width=400, color="blue",
                                     bgcolor=colors.BLACK87)
                    bulk_tasks_view.controls.append(
                        Column(
                            controls=[
                                Text(str(cnt+1) + '  ' + u"\u27F6" +
                                     '   Downloading  ' + video.title, font_family=default),
                                Row([Text(value="↳"), pb, Text("File Size = " + MB, font_family=default)])]
                        )
                    )
                    for i in range(0, 101):
                        pb.value = i * 0.01
                        sf = int(round(MaxFileSize)) / 3
                        sleep(sf * 0.1)
                        bulkViewMode.update()

                    bulkViewMode.update()
                    destination = base_dir + bulk_artist_name.value
                    out_file = video.streams.filter(
                        only_audio=True).first().download(output_path=destination)
                    # save the file
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    # result of success
                    bulk_tasks_view.controls.pop()
                    bulk_tasks_view.controls.append(
                        Row(
                            controls=[
                                bulk_status_verified_logo,
                                Text(str(cnt+1) + '  ' + u"\u27F6" + '  ' + video.title +
                                     ' has been successfully downloaded.', font_family=default),
                                Text("File Size = " + MB, font_family=default)]
                        )
                    )
                    bulkViewMode.update()
                    print(str(cnt) + '-->>' + colored(video.title,
                          'cyan') + " has been successfully downloaded.")
                except:
                    print('cant download')
                    pass
            bulk_status_view.controls.append(
                Row([Text(value="All Songs Downloaded Successfully", weight="bold")]))
            bulkViewMode.update()

    bulk_status_view = Column()
    bulk_tasks_view = ListView(
        expand=1, spacing=10, padding=1, auto_scroll=True)
    single_status_thumbnail = Column(width=540, height=400)
    single_download_status = Column(expand=540)
    single_video_name = Text()
    single_video_size = Text()
    single_video_quality = Text()
    single_video_format = Text()
    single_video_link = Text(color=colors.BLUE)
    single_video_folder = Text(no_wrap=True)
    single_video_length = Text(no_wrap=True)
    single_status = Row(
        visible=False, expand=True,
        controls=[
            Column([
                single_status_thumbnail,
                single_download_status
            ]),

            VerticalDivider(),
            Card(
                expand=True,
                margin=margin.all(2),
                elevation=4,
                content=Column(
                    [
                        Column(

                            controls=[
                                Container(
                                    content=Row([Container(
                                        content=Text(
                                            value="Video Details"),
                                        alignment=alignment.center,
                                        width=200,
                                        height=40,

                                    )], alignment="center"),

                                ), ]),

                        Column([
                            Container(
                                content=Row([Container(
                                    content=Text(
                                        value="Video Name"),
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                ),
                                    Container(
                                    expand=True,
                                    content=single_video_name,
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                )], spacing=1, alignment="start"),
                                bgcolor=colors.AMBER_100,
                            ),
                        ]),

                        Column([
                            Container(
                                content=Row([Container(
                                    content=Text(
                                        value="Video Length"),
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                ),
                                    Container(
                                    expand=True,
                                    content=single_video_length,
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                )], spacing=1, alignment="start"),
                                bgcolor=colors.AMBER_100,
                            ),
                        ]),

                        Column([
                            Container(
                                content=Row([Container(
                                    content=Text(
                                        value="Video Size"),
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                ),
                                    Container(
                                    expand=True,
                                    content=single_video_size,
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                )], spacing=1, alignment="start"),
                                bgcolor=colors.AMBER_100,
                            ),
                        ]),

                        Column([
                            Container(
                                content=Row([Container(
                                    content=Text(
                                        value="Video Quality"),
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                ),
                                    Container(
                                    expand=True,
                                    content=single_video_quality,
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                )], spacing=1, alignment="start"),
                                bgcolor=colors.AMBER_100,
                            ),
                        ]),

                        Column([
                            Container(
                                content=Row([Container(
                                    content=Text(
                                        value="Video Format"),
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                ),
                                    Container(
                                    expand=True,
                                    content=single_video_format,
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                )], spacing=1, alignment="start"),
                                bgcolor=colors.AMBER_100,
                            ),
                        ]),

                        Column([
                            Container(
                                content=Row([Container(
                                    content=Text(
                                        value="Video Link"),
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                ),
                                    Container(
                                    expand=True,
                                    content=single_video_link,
                                    alignment=alignment.center,
                                    width=200,
                                    height=40,
                                    bgcolor=colors.WHITE,
                                )], spacing=1, alignment="start"),
                                bgcolor=colors.AMBER_100,
                            ),
                        ]),

                        Column(
                            expand=True,
                            controls=[
                                Container(
                                    content=Row([Container(
                                        content=Text(
                                            value="Output Folder"),
                                        alignment=alignment.center,
                                        width=200,
                                        height=40,
                                        bgcolor=colors.WHITE,
                                    ),
                                        Container(
                                        expand=True,
                                        content=single_video_folder,
                                        alignment=alignment.center,
                                        width=200,
                                        height=40,
                                        bgcolor=colors.WHITE,
                                    )], spacing=1, alignment="start"),
                                    bgcolor=colors.AMBER_100,
                                ),
                            ]),


                    ], spacing=1, width=400, height=500),


            ),
        ],
        spacing=15
    )

    singleModeView = Column(
        spacing=5,
        expand=True,
        controls=[

            #1
            Row([Text(value="Single Mode - Download one Youtube Video",
                style="headlineSmall")], alignment="center"),

            #2
            Divider(),

            #3
            Row([Text(value="Download Location"), ElevatedButton("Open directory", icon=icons.FOLDER_OPEN,
                on_click=lambda _: get_directory_dialog.get_directory_path(),), pathText], alignment="center"),

            #4
            Divider(),

            #5
            Row(
                [
                    downloadFormat,
                    single_url_id,
                ], alignment="center"),

            #6
            Row([ElevatedButton(text="Download", on_click=downloadActionForSingle,
                icon="download")], alignment="center"),

            #7
            Divider(),

            #8
            Container(
                content=single_status,
                bgcolor=colors.WHITE,
                width=1360,
                height=390,
            ),
            Row(

                controls=[Text('made with \u2764\ufe0f by SAM'),
                          ],
            ),

        ],
    )

    bulkViewMode = Column(
        spacing=5,
        expand=True,
        controls=[
            #1
            Row([Text(value="Bulk Mode - Download whole channel or Playlist Video",
                style="headlineSmall")], alignment="center"),

            #2
            Divider(),

            #3
            Row([Text(value="Download Location"), ElevatedButton("Open directory", icon=icons.FOLDER_OPEN,
                on_click=lambda _: get_directory_dialog.get_directory_path(),), pathText], alignment="center"),

            #4
            Divider(),

            #5
            Row(
                [
                    Text(value="Artist or Folder Name"),
                    bulk_artist_name,
                    Text(value="Choose a Format :- "),
                    downloadFormat
                ], alignment="center"),

            #5
            Row(
                [
                    bulk_url_type,
                    bulk_url_id,
                ], alignment="center"),

            #7
            Row([ElevatedButton(text="Download", on_click=downloadActionForBulk,
                icon="download")], alignment="center"),

            #8
            Divider(),

            #9
            Container(
                content=Row(
                    [
                        Column([Row([Text(value="Status")], alignment="center"), Divider(
                        ), bulk_status_view], width=230),
                        VerticalDivider(),
                        Column([Row([Text(value="Download Details")], alignment="center"), Divider(
                        ), bulk_tasks_view], spacing=0, expand=True)
                    ],
                    spacing=4
                ),

                bgcolor=colors.WHITE,
                width=1360,
                height=300,
            ),
            Row(

                controls=[Text('made with \u2764\ufe0f by SAM'),
                          ],
            ),

        ],
    )

    single_mainView_1 = Row(
        [
            single_view_rail,
            VerticalDivider(width=1),
            singleModeView
        ],
        expand=True,
    )

    bulk_mainView_2 = Row(
        [

            bulk_view_rail,
            VerticalDivider(width=1),
            bulkViewMode
        ],
        expand=True,
        visible=False
    )

    settings_mainView_3 = Row(
        [
            settings_view_rail,
            VerticalDivider(width=1),
            Column([Text("thirdPage!")], alignment="start", expand=True),
        ],
        expand=True,
        visible=False
    )

    page.horizontal_alignment = "center"
    page.scroll = 'none'
    page.add(single_mainView_1, bulk_mainView_2, settings_mainView_3)
    page.update()


flet.app(target=main)
