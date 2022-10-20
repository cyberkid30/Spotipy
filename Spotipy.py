# Inbuilt Modules
import os
import glob
import time
import urllib.parse
import requests
import webbrowser
import urllib.request
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog as fd

# Installed Modules
import pathlib
import mysql.connector
from pygame import mixer
from mutagen.mp3 import MP3
from bs4 import BeautifulSoup
from pydub import AudioSegment
from PIL import Image, ImageTk
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch
from pythumb import Thumbnail
from win10toast import ToastNotifier

# Path of current directory
file_path = pathlib.Path(__file__).parent.resolve()

# PyGame Mixer Initiation
mixer.init()
toaster = ToastNotifier()

paused, song_end, play = False, False, False

volume_set, est_time, est_length = 1, 0, 0

topic, name_save, category1 = "", "", ""
current_path, current_name = "", ""

song_list, name_list, thumbnail_list, thumbnailplay_list, category_list = [], [], [], [], []
all_list, all_name_list, all_thumbnail_list, all_thumbnailplay_list, all_category_list = [], [], [], [], []

sql = open("sqlpass.txt", "r+")
sql_pass_temp = sql.readline()
sql_pass = sql_pass_temp.replace("\n", "")

if os.environ['COMPUTERNAME'] == sql.readline():
    pass
else:
    sql_password = input("\nEnter password for SQL:")
    computername = os.environ['COMPUTERNAME']
    temp = open("sqlpass.txt", "w")
    temp.write(sql_password)
    temp.write("\n"+computername)
    temp.close()
    sql_pass = sql_password

# Database Initiation
try:
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password=sql_pass,
        database="MusicPlayer"
    )

except:
    mydatabase = mysql.connector.connect(
        host="localhost",
        user="root",
        password=sql_pass
    )

# Cursor Initiation
mycursor = mydatabase.cursor()

# Database Creation
mycursor.execute("CREATE DATABASE IF NOT EXISTS MusicPlayer")
mycursor.execute("USE MusicPlayer")

# Table Creation
mycursor.execute("CREATE TABLE IF NOT EXISTS All_Songs(SONG_NAME VARCHAR(255),CATEGORY VARCHAR(8),SONG_PATH VARCHAR(255) ,THUMBNAIL VARCHAR(255),THUMBNAIL_PLAY VARCHAR(255))")

# Folder Setup
list_of_files = os.listdir("./Dependencies//")
list_of_folder = ["DownloadedSongs", "Thumbnails", "ThumbnailsPlay"]

if "Dependencies" in os.listdir():
    for folder in list_of_folder:
        if folder not in list_of_files:
            os.makedirs("./Dependencies//" + folder)
        else:
            pass
else:
    os.makedirs('Dependencies')
    for folder in list_of_folder:
        os.makedirs("./Dependencies//" + folder)

main_window = Tk()
main_window.title("SoulSync")
main_window.geometry('1200x700')
main_window.maxsize(1200, 690)
main_window.minsize(1200, 690)


# MainScreen ImagePaths
folder_location_main = str(file_path) + "\\Dependencies\\images\\MainScreen\\"

# MainScreen ImageLoading
BG = PhotoImage(file=folder_location_main + "BG.png")
Add_Song = PhotoImage(file=folder_location_main + "Add_Song.png")
Add_from_Folder = PhotoImage(file=folder_location_main + "Add_Folder.png")
Go_Online = PhotoImage(file=folder_location_main + "GoOnline.png")
ML = PhotoImage(file=folder_location_main + "SongDisplay_BG.png")
All_Songs = PhotoImage(file=folder_location_main + "AllSongs.png")
Sleep = PhotoImage(file=folder_location_main + "Sleep.png")
Workout = PhotoImage(file=folder_location_main + "Workout.png")
Love = PhotoImage(file=folder_location_main + "Love.png")
Party = PhotoImage(file=folder_location_main + "Party.png")
Delete = PhotoImage(file=folder_location_main + "Delete.png")


# HUD ImagePaths
folder_location_HUD = str(file_path) + "\\Dependencies\\images\\HUD\\"

# HUD ImageLoading
Play = PhotoImage(file=folder_location_HUD + "Play_Button.png")
Pause = PhotoImage(file=folder_location_HUD + "Pause_Button.png")
Stop = PhotoImage(file=folder_location_HUD + "Stop_Button.png")
Next = PhotoImage(file=folder_location_HUD + "Next_Button.png")
Previous = PhotoImage(file=folder_location_HUD + "Previous_Button.png")
HighVol = PhotoImage(file=folder_location_HUD + "Full_Volume.png")
MediumVol = PhotoImage(file=folder_location_HUD + "Medium_Volume.png")
LowVol = PhotoImage(file=folder_location_HUD + "Low_Volume.png")
Mute = PhotoImage(file=folder_location_HUD + "Muted_Volume.png")

# AddSongs ImagePaths
folder_location_add = str(file_path) + "\\Dependencies\\images\\AddSong\\"

# AddSongs ImageLoading
BG2 = PhotoImage(file=folder_location_add + "Add_BG.png")
EL = PhotoImage(file=folder_location_add + "EntryBox_BG.png")
SSAName = PhotoImage(file=folder_location_add + "SaveAs_Text.png")
Category = PhotoImage(file=folder_location_add + "Category_Text.png")
Submit_button = PhotoImage(file=folder_location_add + "Submit_Button.png")
Cancel_button = PhotoImage(file=folder_location_add + "Cancel_Button.png")


# GoOnline ImagePaths
folder_location_online = str(file_path) + "\\Dependencies\\images\\GoOnline\\"

# GoOnline ImageLoading
Open_button = PhotoImage(file=folder_location_online + "OpenSong_Button.png")
SearchL = PhotoImage(file=folder_location_online + "Search_Text.png")
SAName = PhotoImage(file=folder_location_online + "SaveAs_Text.png")
Go_To_Site_button = PhotoImage(file=folder_location_online + "Go_to_Site_Button.png")
Download_button = PhotoImage(file=folder_location_online + "Download_Button.png")
LinkL = PhotoImage(file=folder_location_online + "Link_Text.png")
Provide_Link_button = PhotoImage(file=folder_location_online + "ProvideLink_Button.png")
Cancel_button2 = PhotoImage(file=folder_location_online + "Cancel_Button.png")


def downloadImage(query, fileLocation, name, n=1):
    URL = "https://www.google.com/search?tbm=isch&q=" + query + " song cover"
    result = requests.get(URL)
    src = result.content

    soup = BeautifulSoup(src, 'html.parser')
    imgTags = soup.find_all('img', class_='yWs4tf')

    count = 0
    for i in imgTags:
        if count == n: break
        try:
            urllib.request.urlretrieve(i['src'], f'{fileLocation}' + str(name + "_raw") + '.png')
            count += 1
        except Exception as e:
            raise e


def reset():
    global play
    play = False
    mixer.music.stop()
    NameLabel.config(text=" ")
    song_current_time.config(text="", foreground="grey1")
    song_total_time.config(text="")

    NameLabel2.config(text="", foreground="turquoise4")
    song_total_time2.config(text="", foreground="turquoise4")
    CategoryLabel.config(text="", foreground="turquoise4")
    ImageLabel.config(image="")

    volLabel.destroy()
    previous_btn.destroy()
    next_btn.destroy()
    pause_btn.destroy()
    volume_slider.destroy()
    stop_btn.destroy()
    song_slider.destroy()


def song_current_info():
    global play
    global est_time
    global name_list
    global current_name

    try:
        current_time = mixer.music.get_pos() / 1000
        est_time = round(current_time, 1)
        est_time += 0.5
        cur_index = name_list.index(current_name)
        list_len = int(len(name_list)) - 1
        if est_time >= est_length:
            if cur_index == list_len:
                reset()
            else:
                previous_song()
        if play:
            time_format = time.strftime('%M:%S', time.gmtime(current_time))
            song_current_time.config(text=time_format, foreground="cyan")
            song_slider.config(value=current_time)

            song_current_time.after(1000, song_current_info)

        else:
            pass

    except:
        pass


def song_slide(x): song_current_info()


def go_online():
    download_window = Toplevel()
    download_window.geometry("400x500")
    download_window.title("Go Online")

    def goPage():
        """This function takes the user to the webpage of the song"""
        global topic
        if topic == "":
            messagebox.showerror("Use brain please", "Required field detected empty")
            download_window.destroy()
            os.system("Download.py")
        else:
            search_title = topic
            video_search = VideosSearch(search_title, limit=1)
            result = video_search.result()
            link = result["result"][0]['link']
            webbrowser.open(link)

    def cancel():
        all_song()
        download_window.destroy()

    def screen2():
        global topic
        global name_save
        global category1
        global temp

        topic = topicEntryBox.get()

        if topic == "":
            messagebox.showerror("Use brain please", "Required field detected empty")
            download_window.destroy()
            go_online()

        else:
            name_save = nameSaveEntry.get()

            categoryEntryget1 = CategoryEntryBox1.get()
            categoryEntryget2 = categoryEntryget1.replace(" ", "")
            categoryEntryget = categoryEntryget2.capitalize()

            if categoryEntryget == "" or categoryEntryget == "Party/Love/Workout/Sleep":
                category1 = "None"

            else:
                category1 = categoryEntryget

            topicEntryBox.destroy()
            nameSaveEntry.destroy()
            SearchLabel.destroy()
            EntryLabel.destroy()
            EntryLabel2.destroy()
            EntryLabel5.destroy()
            SSALabel.destroy()
            Submit_but.destroy()
            Provide_Link_bt.destroy()
            Cancel_but.destroy()
            Category_Label.destroy()
            CategoryEntryBox1.destroy()

            Go_to_site_bt = Button(download_window, image=Go_To_Site_button, border=0, bg="gray1",
                                   activebackground="gray1",
                                   command=goPage)
            Go_to_site_bt.place(x=87, y=280)

            Download_bt = Button(download_window, image=Download_button, border=0, bg="gray1", activebackground="gray1",
                                 command=download)
            Download_bt.place(x=87, y=335)

            Cancel_bt = Button(download_window, image=Cancel_button2, border=0, bg="gray1", activebackground="gray1",
                               command=cancel)
            Cancel_bt.place(x=87, y=390)

    def download():
        global topic
        global name_save
        global category1

        try:
            os.remove("thumb.png")
        except:
            pass

        category = category1.replace(" ", "")

        messagebox.showinfo("Sorry for trouble :(", "You will get message once download is complete")

        download_window.title("Download-Go Online")

        search_title = topic
        video_search = VideosSearch(search_title, limit=1)
        result = video_search.result()
        title = result["result"][0]['title']
        link = result["result"][0]['link']

        if name_save == "":
            name_save = title
        else:
            name_save = name_save

        length = len(name_save)

        if length > 25:
            name_to_save = name_save[:26]
        else:
            name_to_save = name_save

        search_query = name_to_save

        to_download = str(file_path) + "\\Dependencies\\Thumbnails\\"

        downloadImage(name_to_save, to_download, name_to_save)

        image_to_resize = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_raw.png"
        resize_path = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_thumbnail.png"
        save_path = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\" + str(search_query) + "_thumbnailplay.png"

        imge = Image.open(image_to_resize)
        crop_image = imge.resize((50, 50))
        crop_image.save(resize_path)

        see_contact_img = imge.resize((120, 120))
        see_contact_img.save(save_path)

        os.remove(image_to_resize)

        audio_downloder = YoutubeDL({'format': 'bestaudio/audio', 'codec': 'wav',
                                     'preferredquality': '192', 'noplaylist': True,
                                     'outtmpl': name_to_save + '.%(ext)s'})

        audio_downloder.extract_info(link)

        list_of_files = os.listdir()

        if name_to_save + ".webm" in list_of_files:
            target = name_to_save + ".webm"

        else:
            target = name_to_save + ".m4a"

        wav_audio = AudioSegment.from_file(target)
        os.remove(target)
        song_download = str(file_path) + "\\Dependencies\\DownloadedSongs\\" + name_to_save + ".mp3"
        wav_audio.export(song_download, format="mp3")

        thumbnail_path = resize_path
        thumbnail_play = save_path
        filename = song_download

        Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
        song_save = (name_to_save, category, filename, thumbnail_path, thumbnail_play)

        mycursor.execute(Formula, song_save)
        mydatabase.commit()

        all_song()
        toaster.show_toast("Done :)", "Your song has been successfully downloaded and added to SoulSync", threaded=True,
                           duration=15)
        messagebox.showinfo("Finally", "Download Complete\nYou will now be redirected to main screen")
        download_window.destroy()

    def link_download():
        topicEntryBox.destroy()
        SearchLabel.destroy()
        EntryLabel.destroy()
        EntryLabel2.destroy()
        EntryLabel5.destroy()
        SSALabel.destroy()
        Submit_but.destroy()
        Provide_Link_bt.destroy()
        Category_Label.destroy()
        Cancel_but.destroy()
        nameSaveEntry.destroy()

        download_window.title("Link Download-Go Online")

        link2, name, category1 = "", "", ""

        def screen3():
            global name
            global link2
            global category1
            global temp

            link = linkEntry.get()
            link2 = link

            if link2 == "" or link2 == " ":
                messagebox.showerror("U crazy?", "Link missing")
                download_window.destroy()
                go_online()
            else:
                name_save2 = nameSaveEntry2.get()
                name = name_save2

                categoryEntryget1 = CategoryEntryBox1.get()
                # categoryEntryget2 = categoryEntryget1.replace(" ", "")

                if categoryEntryget1 == "" or categoryEntryget1 == "Party/Love/Workout/Sleep":
                    category1 = "None"

                else:
                    category1 = categoryEntryget1

                LinkLabel.destroy()
                nameSaveEntry.destroy()
                EntryLabel2.destroy()
                EntryLabel3.destroy()
                EntryLabel4.destroy()
                EntryLabel6.destroy()
                Cancel_but.destroy()
                nameSaveEntry.destroy()
                linkEntry.destroy()
                SanLabel.destroy()
                Submit_bt.destroy()
                SanLabel.destroy()
                Category_Label2.destroy()
                CategoryEntryBox1.destroy()
                CategoryEntry.destroy()
                Cancel_but3.destroy()
                nameSaveEntry2.destroy()


                Download_bt = Button(download_window, image=Download_button, border=0, bg="gray1",
                                     activebackground="gray1",
                                     command=download_link)
                Download_bt.place(x=87, y=305)

                Cancel_bt = Button(download_window, image=Cancel_button2, border=0, bg="gray1",
                                   activebackground="gray1",
                                   command=cancel)
                Cancel_bt.place(x=87, y=370)

        def download_link():
            global link2
            global name
            global category1
            CategoryEntryBox1.destroy()

            try:
                os.remove("thumb.png")
            except:
                pass

            messagebox.showinfo("Sorry for Trouble :(", "You will get message when your download is complete.")

            length = len(name)

            if length > 25:
                name_to_save = name[:26]
            else:
                name_to_save = name


            audio_downloder = YoutubeDL({'format': 'bestaudio/audio', 'codec': 'wav',
                                         'preferredquality': '192', 'noplaylist': True,
                                         'outtmpl': name_to_save + '.%(ext)s'})

            audio_downloder.extract_info(link2)

            list_of_files = os.listdir()

            if name_to_save + ".webm" in list_of_files:
                target = name_to_save + ".webm"

            else:
                target = name_to_save + ".m4a"

            wav_audio = AudioSegment.from_file(target)
            song_download = str(file_path) + "\\Dependencies\\DownloadedSongs\\" + name_to_save + ".mp3"
            wav_audio.export(song_download, format="mp3")
            os.remove(target)

            search_query = name_to_save

            to_download = str(file_path) + "\\Dependencies\\Thumbnails\\"
            downloadImage(name_to_save, to_download, name_to_save)

            image_to_resize = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_raw.png"
            resize_path = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_thumbnail.png"
            save_path = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\" + str(
                search_query) + "_thumbnailplay.png"

            imge = Image.open(image_to_resize)
            crop_image = imge.resize((50, 50))
            crop_image.save(resize_path)

            see_contact_img = imge.resize((120, 120))
            see_contact_img.save(save_path)

            os.remove(image_to_resize)

            thumbnail_path = resize_path
            thumbnail_play = save_path
            filename = song_download

            Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
            song_save = (name_to_save, category1, filename, thumbnail_path, thumbnail_play)

            mycursor.execute(Formula, song_save)
            mydatabase.commit()

            cancel()
            toaster.show_toast("Done :)", "Your song has been successfully downloaded and added to SoulSync", threaded=True,
                           duration=15)
            messagebox.showinfo("Finally :)", "Download Complete!\nYou will now be redirected to MainScreen.")

        LinkLabel = Label(download_window, image=LinkL, border=0, bg="gray1")
        LinkLabel.place(x=20, y=164)

        EntryLabel3 = Label(download_window, image=EL, border=0, bg="gray1")
        EntryLabel3.place(x=20, y=200)

        EntryLabel4 = Label(download_window, image=EL, border=0, bg="gray1")
        EntryLabel4.place(x=20, y=289)

        nameSaveEntry2 = Entry(download_window, relief=FLAT, width="18", bg="DarkSlateGray1",
                               font=("Berlin Sans FB", 24))
        nameSaveEntry2.place(x=24, y=291)

        linkEntry = Entry(download_window, relief=FLAT, width="18", bg="DarkSlateGray1", font=("Berlin Sans FB", 24))
        linkEntry.place(x=24, y=202)
        SanLabel = Label(download_window, image=SAName, border=0, bg="gray1")
        SanLabel.place(x=18, y=253)

        Category_Label2 = Label(download_window, image=Category, border=0, bg="gray1")
        Category_Label2.place(x=17, y=339)

        EntryLabel6 = Label(download_window, image=EL, border=0, bg="gray1")
        EntryLabel6.place(x=20, y=374)
        CategoryEntry = Entry(download_window, relief=FLAT, width="18", bg="DarkSlateGray1",
                              font=("Berlin Sans FB", 24))
        CategoryEntry.place(x=24, y=376)

        Submit_bt = Button(download_window, image=Submit_button, border=0, bg="gray1", activebackground="gray1",
                           command=screen3)
        Submit_bt.place(x=76, y=452)
        Cancel_but3 = Button(download_window, image=Cancel_button, border=0, activebackground="gray1", bg="gray1",
                             command=cancel)
        Cancel_but3.place(x=210, y=452)

    BG_label = Label(download_window, image=BG2, border=0)
    BG_label.place(x=0, y=0)

    SearchLabel = Label(download_window, image=SearchL, border=0, bg="gray1")
    SearchLabel.place(x=20, y=164)

    EntryLabel = Label(download_window, image=EL, border=0, bg="gray1")
    EntryLabel.place(x=20, y=200)
    topicEntryBox = Entry(download_window, relief=FLAT, width="18", bg="DarkSlateGray1", font=("Berlin Sans FB", 24))
    topicEntryBox.place(x=24, y=203)

    SSALabel = Label(download_window, image=SSAName, border=0, bg="gray1")
    SSALabel.place(x=17, y=253)
    EntryLabel2 = Label(download_window, image=EL, border=0, bg="gray1")
    EntryLabel2.place(x=20, y=289)
    nameSaveEntry = Entry(download_window, relief=FLAT, width="18", bg="DarkSlateGray1", font=("Berlin Sans FB", 24))
    nameSaveEntry.place(x=24, y=291)

    Submit_but = Button(download_window, image=Submit_button, border=0, bg="gray1", activebackground="gray1",
                        command=screen2)
    Submit_but.place(x=76, y=432)

    Provide_Link_bt = Button(download_window, image=Provide_Link_button, border=0, bg="gray1", activebackground="gray1",
                             command=link_download)
    Provide_Link_bt.place(x=100, y=475)

    Category_Label = Label(download_window, image=Category, border=0, bg="gray1")
    Category_Label.place(x=17, y=339)

    EntryLabel5 = Label(download_window, image=EL, border=0, bg="gray1")
    EntryLabel5.place(x=20, y=374)

    CategoryEntryBox1 = Entry(download_window, relief=FLAT, width="18", bg="DarkSlateGray1",
                              font=("Berlin Sans FB", 24))
    CategoryEntryBox1.place(x=24, y=376)

    Cancel_but = Button(download_window, image=Cancel_button, border=0, bg="gray1", activebackground="gray1",
                        command=cancel)
    Cancel_but.place(x=210, y=432)

    mainloop()


def add_song():
    # GUI Window Initiation
    addwindow = Toplevel()
    addwindow.geometry("400x500")
    addwindow.title("Add Song")

    BG_label = Label(addwindow, image=BG2, border=0)
    BG_label.place(x=0, y=0)

    def submit_add():
        """This is function which will run when submit button is clicked"""
        nameEntryget = NameEntryBox.get()
        name_of_song1 = nameEntryget

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=[("Songs", ".mp3")])

        if filename == "":
            addwindow.destroy()
        else:
            search_query_name = os.path.basename(filename)
            search_query_split = search_query_name.split(".")
            search_query = search_query_split[0]
            to_download = str(file_path) + "\\Dependencies\\Thumbnails\\"

            if name_of_song1 == "":
                name_of_song1 = search_query
            else:
                pass

            length = len(name_of_song1)

            if length > 25:
                name_of_song = name_of_song1[:26]
            else:
                name_of_song = name_of_song1

            categoryEntryget1 = categoryEntryBox.get()
            categoryEntryget2 = categoryEntryget1.replace(" ", "")
            categoryEntryget = categoryEntryget2.capitalize()

            if categoryEntryget == "" or categoryEntryget == "Party/Love/Workout/Sleep":
                category = "None"

            else:
                category = categoryEntryget

            downloadImage(name_of_song, to_download, search_query)

            image_to_resize = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_raw.png"
            resize_path = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(search_query) + "_thumbnail.png"
            save_path = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\" + str(search_query) + "_thumbnailplay.png"

            imge = Image.open(image_to_resize)
            crop_image = imge.resize((50, 50))
            crop_image.save(resize_path)

            imge2 = Image.open(image_to_resize)
            see_contact_img = imge2.resize((120, 120))
            see_contact_img.save(save_path)

            os.remove(image_to_resize)

            thumbnail_path = resize_path
            thumbnail_play = save_path

            Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
            song_save = (name_of_song, category, filename, thumbnail_path, thumbnail_play)

            mycursor.execute(Formula, song_save)
            mydatabase.commit()
            all_song()
            addwindow.destroy()

    def catentrydel(*args):
        """Function to clear CategoryEntryBox on click on EntryBox"""
        categoryEntryBox.delete(0, END)
        return None

    # Main code
    SSALabel = Label(addwindow, image=SSAName, border=0, bg="gray1")
    SSALabel.place(x=18, y=172)

    nameEntryBG = Label(addwindow, image=EL, border=0, bg="gray1")
    nameEntryBG.place(x=20, y=210)

    NameEntryBox = Entry(addwindow, relief=FLAT, width="18", bg="DarkSlateGray1", font=("Berlin Sans FB", 24))
    NameEntryBox.place(x=24, y=212)

    Category_Label = Label(addwindow, image=Category, border=0, bg="gray1")
    Category_Label.place(x=17, y=272)

    CatEntryBG = Label(addwindow, image=EL, border=0, bg="gray1")
    CatEntryBG.place(x=20, y=308)

    categoryEntryBox = Entry(addwindow, relief=FLAT, width="18", bg="DarkSlateGray1", font=("Berlin Sans FB", 24))
    categoryEntryBox.place(x=24, y=310)
    categoryEntryBox.insert(END, "Party/Love/Workout/Sleep")
    categoryEntryBox.bind("<Button-1>", catentrydel)

    submitButton = Button(addwindow, image=Submit_button, activebackground="gray1", border=0, bg="gray1",
                          command=submit_add)
    submitButton.place(x=140, y=385)

    cancelbutton = Button(addwindow, image=Cancel_button, border=0, activebackground="gray1", bg="gray1",
                          command=addwindow.destroy)
    cancelbutton.place(x=140, y=422)

    mainloop()


def add_folder():
    global song_list
    global name_list
    global thumbnail_list

    folder_path = fd.askdirectory(title='Select a Folder', initialdir='/')

    if folder_path == "":
        pass
    else:
        targetPattern = str(folder_path) + "/*.mp3"
        songs = glob.glob(targetPattern)

        name_tosave_list, path_tosave_list = [], []

        messagebox.showwarning("Sorry for Trouble",
                               "The program might freeze from some seconds just wait for it to get normal. You will receive a message when songs are added to Player")
        for s in songs:
            to_name = s.split("\\")
            raw_name = to_name[-1]
            raw_save = raw_name.split(".")
            to_save = raw_save[0]
            path = folder_path + "/" + str(raw_name)
            path_tosave_list.append(path)
            name_tosave_list.append(to_save)

        category = "None"

        to_download = str(file_path) + "\\Dependencies\\Thumbnails\\"
        for (name_of_song1, filename) in zip(name_tosave_list, path_tosave_list):
            length = len(name_of_song1)
            if length > 25:
                name_of_song = name_of_song1[:26]
            else:
                name_of_song = name_of_song1

            downloadImage(name_of_song1, to_download, name_of_song)

            image_to_resize = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(name_of_song) + "_raw.png"
            resize_path = str(file_path) + "\\Dependencies\\Thumbnails\\" + str(name_of_song) + "_thumbnail.png"
            save_path = str(file_path) + "\\Dependencies\\ThumbnailsPlay\\" + str(name_of_song) + "_thumbnailplay.png"

            imge = Image.open(image_to_resize)
            crop_image = imge.resize((50, 50))
            crop_image.save(resize_path)

            see_contact_img = imge.resize((120, 120))
            see_contact_img.save(save_path)

            os.remove(image_to_resize)

            thumbnail_path = resize_path
            thumbnail_play = save_path

            Formula = "INSERT INTO All_Songs (SONG_NAME,CATEGORY,SONG_PATH,THUMBNAIL, THUMBNAIL_PLAY) VALUES(%s, %s, %s, %s, %s)"
            song_save = ((name_of_song, category, filename, thumbnail_path, thumbnail_play))

            mycursor.execute(Formula, song_save)
            mydatabase.commit()
            all_song()
        toaster.show_toast("Done :)", "Your songs have been successfully added to SoulSync", threaded=True,
                           duration=15)
        messagebox.showinfo("Thenks for waiting", "Songs have been added successfully.")
        mainloop()


def play_music(song_path, song_name, category, thumbnail_play):
    global current_path
    global current_name
    global volume_set
    global est_length
    global play
    current_name = song_name
    current_path = song_path

    stop_music()

    play = True

    def mute(*args):
        global volume_set
        setvolume = 0
        volume_set = setvolume
        mixer.music.set_volume(setvolume)
        volume_slider.config(value=setvolume)
        volLabel.config(image=Mute, command=unmute)
        main_window.bind("<m>", unmute)

    def unmute(*args):
        global volume_set
        setvolume = 1
        volume_set = setvolume
        mixer.music.set_volume(setvolume)
        volume_slider.config(value=setvolume)
        volLabel.config(image=HighVol, command=mute)
        main_window.bind("<m>", mute)

    def volume_control(x):
        global volume_set
        global volLabel
        setvolume = volume_slider.get()
        image_vol = round(setvolume, 1)
        if image_vol == 0.7 or image_vol == 0.6 or image_vol == 0.5:
            volLabel.config(image=MediumVol)
        elif image_vol == 0.1 or image_vol == 0.2 or image_vol == 0.3 or image_vol == 0.4:
            volLabel.config(image=LowVol)
        elif image_vol == 0.8 or image_vol == 0.9 or image_vol == 1.0:
            volLabel.config(image=HighVol)
        elif image_vol == 0.0:
            volLabel.config(image=Mute)

        mixer.music.set_volume(setvolume)
        volume_set = setvolume
    

    song_load = MP3(song_path)
    song_length_raw = song_load.info.length
    est_length = int(song_length_raw)
    song_length = time.strftime('%M:%S', time.gmtime(song_length_raw))
    song_total_time.config(text=song_length, foreground="cyan")
    song_total_time2.config(text=song_length, foreground="cyan")
    CategoryLabel.config(text=category, foreground="cyan")

    thumbnail = PhotoImage(file=thumbnail_play)
    ImageLabel.config(image=thumbnail)
    ImageLabel.image = thumbnail

    currentlengthname = len(current_name)
    if currentlengthname > 15:
        current_name1 = current_name[0:15]
    else:
        current_name1 = current_name

    NameLabel2.config(text=current_name1, foreground="cyan")

    global stop_btn
    stop_btn = Button(main_window, image=Stop, border=0, bg="Gray1", activebackground="Gray1", command=stop_music)
    stop_btn.place(x=582, y=624)

    global pause_btn
    pause_btn = Button(main_window, image=Pause, border=0, bg="Gray1", activebackground="Gray1",
                       command=lambda: pause_music(paused))
    pause_btn.place(x=635, y=624)

    global next_btn
    next_btn = Button(main_window, image=Next, border=0, bg="Gray1", activebackground="Gray1", command=previous_song)
    next_btn.place(x=683, y=624)

    global previous_btn
    previous_btn = Button(main_window, image=Previous, border=0, bg="Gray1", activebackground="Gray1",
                          command=next_song)
    previous_btn.place(x=527, y=624)

    global song_slider
    style1 = ttk.Style()
    style1.configure("myStyle.Horizontal.TScale", background="gray1")
    song_slider = ttk.Scale(main_window, from_=0, to=est_length, command=song_slide, length=980,
                            style="myStyle.Horizontal.TScale")
    song_slider.place(x=100, y=587)

    global volume_slider
    volume_slider = ttk.Scale(main_window, from_=0, to=1, orient=HORIZONTAL, value=volume_set, command=volume_control,
                              length=120, style="myStyle.Horizontal.TScale")
    volume_slider.place(x=150, y=639)

    global volLabel
    volLabel = Button(main_window, image=HighVol, background='gray1', activebackground="gray1", bd=0, command=mute)
    volLabel.place(x=97, y=633)

    main_window.bind("<m>", mute)
    main_window.bind("<Left>", next_song)
    main_window.bind("<Right>", previous_song)
    main_window.bind("<BackSpace>", stop_music)
    main_window.bind("<space>", lambda x: pause_music(paused))

    mixer.music.load(song_path)
    mixer.music.play(loops=0)

    currentlengthname2 = len(current_name)
    if currentlengthname2 > 16:
        current_name2 = current_name[0:20]
    else:
        current_name2 = current_name

    NameLabel.config(text=current_name2, foreground="cyan")
    song_current_info()


def stop_music(*args):
    global play

    try:
        play = False
        mixer.music.stop()
        NameLabel.config(text=" ")

        song_current_time.config(text="", foreground="gray1")
        song_total_time.config(text="", foreground="gray1")

        NameLabel2.config(text="", foreground="turquoise4")
        song_total_time2.config(text="", foreground="turquoise4")
        CategoryLabel.config(text="", foreground="turquoise4")
        ImageLabel.config(image="")

        volLabel.destroy()
        previous_btn.destroy()
        next_btn.destroy()
        pause_btn.destroy()
        volume_slider.destroy()
        stop_btn.destroy()
        song_slider.destroy()
    except:
        pass


def pause_music(is_paused):
    global paused
    paused = is_paused

    if paused:
        pause_btn.config(image=Pause)
        mixer.music.unpause()
        paused = False
    else:
        pause_btn.config(image=Play)
        mixer.music.pause()
        paused = True


def next_song(*args):
    global pause_btn
    global current_path
    global current_name

    try:
        for songs in song_list:
            if songs == current_path:
                cur_index = song_list.index(songs)

                if cur_index == 0:
                    pass
                else:
                    next_song = song_list[cur_index - 1]
                    name_song = name_list[cur_index - 1]
                    category = category_list[cur_index - 1]
                    thumbnail = thumbnailplay_list[cur_index - 1]
                    current_name, current_path = name_song, next_song
                    stop_music()
                    play_music(next_song, name_song, category, thumbnail)

    except:
        pass


def previous_song(*args):
    global pause_btn
    global current_path
    global current_name
    try:
        for songs in song_list:
            if songs == current_path:
                cur_index = song_list.index(songs)
                next_song = song_list[cur_index + 1]
                name_song = name_list[cur_index + 1]
                category = category_list[cur_index + 1]
                thumbnail = thumbnailplay_list[cur_index + 1]
                current_name, current_path = name_song, next_song
                stop_music()
                play_music(next_song, name_song, category, thumbnail)

                break

    except:
        pass


def delete(song_name, song_path, song_thumbnail, song_playthumbnail):
    if play:
        stop_music()
    os.remove(song_path)
    os.remove(song_thumbnail)
    os.remove(song_playthumbnail)
    command = f"DELETE FROM ALL_SONGS WHERE SONG_NAME='{song_name}';"
    mycursor.execute(command)
    mydatabase.commit()
    all_song()


def main_screen(cat="None"):
    global song_list
    global name_list
    global current_name
    global current_path
    global thumbnail_list
    global thumbnailplay_list
    global category_list
    global current_thumbnail
    global all_list
    global all_name_list
    global all_thumbnail_list
    global all_thumbnailplay_list
    global all_category_list
    global DelButton

    style = ttk.Style()

    style.configure("Vertical.TScrollbar", gripcount=0,
                    background="Cyan", darkcolor="gray6", lightcolor="LightGreen",
                    troughcolor="Turquoise4", bordercolor="gray6", arrowcolor="gray6", arrowsize=15)

    wrapper1 = LabelFrame(main_window, width="1600", height="100", background="gray6", bd=0)
    mycanvas = Canvas(wrapper1, background="gray6", borderwidth=0, highlightthickness=0, width=770, height=362)
    mycanvas.pack(side=LEFT, expand=False, padx=0)

    yscrollbar = ttk.Scrollbar(wrapper1, orient="vertical", command=mycanvas.yview)
    yscrollbar.pack(side=RIGHT, fill="y", expand=False)

    mycanvas.configure(yscrollcommand=yscrollbar.set)

    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox("all")))

    myframe = Frame(mycanvas)
    mycanvas.create_window((0, 0), window=myframe, anchor="n")

    def OnMouseWheel(event):
        mycanvas.yview_scroll(-1 * (int(event.delta / 120)), "units")

    mycanvas.bind_all("<MouseWheel>", OnMouseWheel)

    wrapper1.place(x=416, y=138)

    see = "SELECT * from All_Songs"
    mycursor.execute(see)
    show_result = mycursor.fetchall()

    all_list, all_name_list, all_thumbnail_list, all_thumbnailplay_list, all_category_list = [], [], [], [], []
    cat_list, cat_name_list, cat_thumbnail_list, cat_thumbnailplay_list, cat_category_list = [], [], [], [], []

    for song in show_result:
        all_name_list.append(song[0])
        all_category_list.append(song[1])
        all_list.append(song[2])
        all_thumbnail_list.append(song[3])
        all_thumbnailplay_list.append(song[4])

        if song[1] == cat:
            cat_list.append(song[2])
            cat_name_list.append(song[0])
            cat_category_list.append(cat)
            cat_thumbnail_list.append(song[3])
            cat_thumbnailplay_list.append(song[4])

    if cat == "None":
        song_list = all_list
        name_list = all_name_list
        category_list = all_category_list
        thumbnail_list = all_thumbnail_list
        thumbnailplay_list = all_thumbnailplay_list

    else:
        song_list = cat_list
        name_list = cat_name_list
        category_list = cat_category_list
        thumbnail_list = cat_thumbnail_list
        thumbnailplay_list = cat_thumbnailplay_list


    list_len = len(song_list)

    for i in range(0, list_len):
        current_path1 = song_list[i]
        current_name1 = name_list[i]
        current_category = category_list[i]
        current_thumbnail = thumbnail_list[i]
        current_playthumnail = thumbnailplay_list[i]

        current_path = current_path1
        current_name = current_name1

        song_load = MP3(current_path)
        song_length_raw = song_load.info.length
        song_length = time.strftime('%M:%S', time.gmtime(song_length_raw))

        Button(myframe, image=ML, bg="gray6", activebackground="gray6", bd=0,
               command=lambda current_path2=current_path1, current_name=current_name, current_category=current_category,
                              current_playthumbnail1=current_playthumnail: play_music(current_path2, current_name,
                                                                                      current_category,
                                                                                      current_playthumbnail1)).grid(
            row=i)

        thumbnail = ImageTk.PhotoImage(Image.open(current_thumbnail))

        thumbnail_btn = Button(myframe, image=thumbnail, borderwidth=0, activebackground="turquoise1", bg="turquoise1",
                               command=lambda current_path2=current_path1, current_name=current_name,
                                              current_category=current_category,
                                              current_playthumbnail1=current_playthumnail: play_music(
                                   current_path2, current_name, current_category, current_playthumbnail1))
        thumbnail_btn.grid(row=i, sticky=W, padx=10, pady=(3, 0))

        name_Button = Button(myframe, text=current_name, bd=0, bg="turquoise1", activebackground="turquoise1",
                             font=("Microsoft JhengHei UI", 22),
                             command=lambda current_path2=current_path1, current_name=current_name,
                                            current_category=current_category,
                                            current_playthumbnail1=current_playthumnail: play_music(
                                 current_path2, current_name, current_category, current_playthumbnail1))
        name_Button.grid(row=i, sticky=W, padx=69, pady=(3, 0))

        length_Button = Button(myframe, text=song_length, bd=0, bg="turquoise1", activebackground="turquoise1",
                               font=("Calibri Light", 17, "bold"),
                               command=lambda current_path2=current_path1, current_name=current_name,
                                              current_category=current_category,
                                              current_playthumbnail1=current_playthumnail: play_music(
                                   current_path2, current_name, current_category, current_playthumbnail1))
        length_Button.grid(row=i, sticky=E, padx=(0, 15), pady=(3, 0))

        DelButton = Button(myframe, bd=0, activebackground="turquoise1", background="turquoise1", image=Delete,
                           command=lambda songname1=current_name, songpath2=current_path1, songthumbnail=current_thumbnail, songplaythumbnail=current_playthumnail: delete(songname1, songpath2, songthumbnail, songplaythumbnail))
        DelButton.grid(row=i, sticky=E, padx=(0, 90), ipady=5)

        thumbnail_btn.image = thumbnail


def all_song(cat="None"):
    main_screen("None")

    if cat == "Party":
        Party_but.config(image=Party, command=party)
    elif cat == "Sleep":
        Sleep_but.config(image=Sleep, command=sleep)
    elif cat == "Love":
        Love_but.config(image=Love, command=love)
    elif cat == "Workout":
        Workout_but.config(image=Workout, command=workout)
    elif cat == "None":
        Party_but.config(image=Party, command=party)
        Sleep_but.config(image=Sleep, command=sleep)
        Love_but.config(image=Love, command=love)
        Workout_but.config(image=Workout, command=workout)


def party():
    main_screen("Party")
    Sleep_but.config(image=Sleep, command=sleep)
    Love_but.config(image=Love, command=love)
    Workout_but.config(image=Workout, command=workout)
    Party_but.config(image=All_Songs, command=lambda: all_song("Party"))


def workout():
    main_screen("Workout")
    Party_but.config(image=Party, command=party)
    Sleep_but.config(image=Sleep, command=sleep)
    Love_but.config(image=Love, command=love)
    Workout_but.config(image=All_Songs, command=lambda: all_song("Workout"))


def love():
    main_screen("Love")
    Party_but.config(image=Party, command=party)
    Sleep_but.config(image=Sleep, command=sleep)
    Workout_but.config(image=Workout, command=workout)
    Love_but.config(image=All_Songs, command=lambda: all_song("Love"))


def sleep():
    main_screen("Sleep")
    Party_but.config(image=Party, command=party)
    Love_but.config(image=Love, command=love)
    Workout_but.config(image=Workout, command=workout)
    Sleep_but.config(image=All_Songs, command=lambda: all_song("Sleep"))


if __name__ == '__main__':
    BG_label = Label(main_window, image=BG, border=0)
    BG_label.place(x=0, y=0)

    AddSongButton = Button(main_window, image=Add_Song, border=0, bg="turquoise4", activebackground="turquoise4",
                           command=add_song)
    AddSongButton.place(x=20, y=290)

    AddFolderButton = Button(main_window, image=Add_from_Folder, border=0, bg="turquoise4",
                             activebackground="turquoise4",
                             command=add_folder)
    AddFolderButton.place(x=20, y=362)

    Go_Online_but = Button(main_window, image=Go_Online, border=0, bg="turquoise4", activebackground="turquoise4",
                           command=go_online)
    Go_Online_but.place(x=20, y=434)

    NameLabel = Label(main_window, text=" ", font=("Century Gothic", 18), foreground="gray1", background="gray1")
    NameLabel.place(x=500, y=553)

    song_current_time = Label(main_window, text=" ", foreground="gray1", background="gray1",
                              font=("Century Gothic", 11, "bold"))
    song_current_time.place(x=55, y=587)

    song_total_time = Label(main_window, text=" ", foreground="gray1", background="gray1",
                            font=("Century Gothic", 11, "bold"))
    song_total_time.place(x=1083, y=587)

    # Current
    ImageLabel = Label(main_window, background="turquoise4")
    ImageLabel.place(x=8, y=136)

    NameLabel2 = Label(main_window, text=" ", font=("Century Gothic", 17), foreground="turquoise4",
                       background="turquoise4")
    NameLabel2.place(x=150, y=139)

    song_total_time2 = Label(main_window, text=" ", foreground="turquoise4", background="turquoise4",
                             font=("Century Gothic", 15))
    song_total_time2.place(x=150, y=174)

    CategoryLabel = Label(main_window, text=" ", font=("Century Gothic", 18), foreground="turquoise4",
                          background="turquoise4")
    CategoryLabel.place(x=150, y=222)

    # Playlist Bar
    Sleep_but = Button(main_window, image=Sleep, border=0, bg="Gray1", activebackground="Gray1", command=sleep)
    Sleep_but.place(x=1082, y=7)

    Workout_but = Button(main_window, image=Workout, border=0, bg="Gray1", activebackground="Gray1", command=workout)
    Workout_but.place(x=966, y=7)

    Love_but = Button(main_window, image=Love, border=0, bg="Gray1", activebackground="Gray1", command=love)
    Love_but.place(x=850, y=7)

    Party_but = Button(main_window, image=Party, border=0, bg="Gray1", activebackground="Gray1", command=party)
    Party_but.place(x=734, y=7)


    main_screen()
    mainloop()
