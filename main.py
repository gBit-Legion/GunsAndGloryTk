import os
import shutil
import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk

import customtkinter
import cv2
from PIL import Image, ImageTk
import numpy
import matplotlib.pyplot as plt

from ultralytics import YOLO

model = YOLO('model/best.pt')

class_colors = \
    {
        0: (255, 0, 0),
        1: (0, 255, 0),
        2: (0, 0, 255)
    }

class_font = cv2.FONT_HERSHEY_SIMPLEX
class_font_scale = 1.2


class App:
    def __init__(self, root):
        super().__init__()
        # Создаем главное окно и настраиваем
        self.root = root
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")
        self.root.title("Guns and Glory")
        self.root.geometry('600x400')
        self.root.config(bg="#E5E5E5")
        self.root.resizable(width=False, height=False)

        root.iconbitmap("images/pngwing.com.ico")

        # Создание меню и добавление в него пунктов
        self.menu = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Сохранить")

        self.menu.add_cascade(label="Файл", menu=self.file_menu)
        self.menu.add_command(label="О программе", command=self.add_message)
        self.menu.add_command(label="Выйти", command=root.destroy)

        self.root.config(menu=self.menu)

        # Стили фреймов
        self.style = ttk.Style()
        self.style.configure("RoundedFrame.TFrame", background="#14213D", borderedwidth=5, borderradius=200)

        # Создаем фреймы
        self.frame_for_left = ttk.Frame(self.root, style="RoundedFrame.TFrame")
        self.frame_for_left.place(height=400, width=300, x=50, y=50)
        self.frame_for_right = ttk.Frame(root, style="RoundedFrame.TFrame")
        self.frame_for_right.place(height=400, width=300, x=390, y=50)

        # Создаем рамку для картинки
        self.canvas = tk.Canvas(self.frame_for_left, width=150, height=150, bg='#14213D')
        self.img = Image.open('images/icons8-бобина-с-пленкой-90.png')
        self.new_image = self.img.resize((150, 150))
        self.image = ImageTk.PhotoImage(self.new_image)
        self.canvas.create_image(75, 75, image=self.image)
        self.canvas.place(width=150, height=150, x=75, y=75)

        # Cоздаем картинку для второго фрейма
        self.canvas2 = tk.Canvas(self.frame_for_right, width=150, height=150, bg='#14213D')
        self.img2 = Image.open('images/security-camera.png')
        self.new_image = self.img2.resize((150, 150))
        self.image2 = ImageTk.PhotoImage(self.new_image)
        self.canvas2.create_image(75, 75, image=self.image2)
        self.canvas2.place(width=150, height=150, x=75, y=75)

        # Добавляем кнопки
        self.btn_for_photo = ttk.Button(self.frame_for_left, text="Выберите фото",
                                        style='Accent.TButton',
                                        command=self.image_dialog)
        self.btn_for_photo.place(width=150, height=50, x=75, y=250)
        self.btn_for_video = ttk.Button(self.frame_for_left, text="Выберите видео",
                                        style='Accent.TButton',
                                        command=self.file_open_video_dialog)
        self.btn_for_video.place(width=150, height=50, x=75, y=320)
        self.btn_for_camera = ttk.Button(self.frame_for_right, text="Подключить камеру",
                                         style='Accent.TButton',
                                         command=self.camera_dialog)
        self.btn_for_camera.place(width=150, height=50, x=75, y=280)

    def file_open_dialog(self):
        filetypes = (('Файлы изображений', '*.jpeg'),
                     ('Файлы видео', '*.mp4'),
                     ('Все файлы', '*.*'))

        filenames = fd.askopenfilenames(title='Open a file', initialdir='/', filetypes=filetypes)

    def image_dialog(self):
        filetypes = (("Файлы изображеий", "*.jpeg *.png *.jpg"),)
        filenames = fd.askopenfilenames(title='Open a file', initialdir='/', filetypes=filetypes)
        if len(filenames) != 0:
            self.root.destroy()
            ip = ImagePlayer(filenames)
            ip.MainWindowForImagePlayer.TopLevel()

    def camera_dialog(self):
        dialog = Dialog(self.root)

    def file_open_video_dialog(self):
        filetypes = (("Файлы видео", "*.mp4"),)

        filenames = fd.askopenfilenames(title='Open a file', initialdir='/', filetypes=filetypes)
        # сюда нужно подставить обработку файлов
        if len(filenames) != 0:
            self.root.destroy()
            vp = VideoPlayer(filenames)
            vp.VideoPlayerMainWindow.TopLevel()

        # подставляем обработку видео

    def add_message(self):
        tk.messagebox.showinfo(title="Реклама", message="Вступайте в ряды МВД России")


# Класс для работы с видео
class VideoPlayer:
    def __init__(self, video_paths):
        self.video_paths = video_paths
        self.videos = []

        self.VideoPlayerMainWindow = tk.Tk()
        self.VideoPlayerMainWindow.title("Video Player")

        self.VideoPlayerMainWindow.iconbitmap("images/pngwing.com.ico")

        self.frames = []
        self.canvases = []

        self.calculate_grid_dimensions(len(self.video_paths))
        self.VideoPlayerMainWindow.geometry(
            f"{self.VideoPlayerMainWindow.winfo_screenwidth()}x{self.VideoPlayerMainWindow.winfo_screenheight()}")
        for i in range(self.rows):
            for j in range(self.columns):
                index = i * self.columns + j
                if index < len(self.video_paths):
                    path = self.video_paths[index]
                    cap = cv2.VideoCapture(path)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                    video_frame = tk.Frame(self.VideoPlayerMainWindow, width=self.grid_width, height=self.grid_height)
                    video_frame.grid(row=i, column=j)

                    canvas = tk.Canvas(video_frame, width=self.grid_width, height=self.grid_height)
                    canvas.pack()

                    self.canvases.append(canvas)
                    self.frames.append(video_frame)

                    self.videos.append({
                        'cap': cap,
                        'width': width,
                        'height': height,
                        'canvas': canvas,
                    })
                else:
                    placeholder_frame = tk.Frame(self.VideoPlayerMainWindow, width=self.grid_width,
                                                 height=self.grid_height)
                    placeholder_frame.grid(row=i, column=j)

                    placeholder_image = Image.open("images/placeholder.jpg").resize(
                        (self.grid_width, self.grid_height))
                    placeholder_photo = ImageTk.PhotoImage(placeholder_image)
                    placeholder_label = tk.Label(placeholder_frame, image=placeholder_photo)
                    placeholder_label.image = placeholder_photo
                    placeholder_label.pack()
        self.VideoPlayerMainWindow.protocol('WM_DELETE_WINDOW', self.back_to_start_window)

        self.play_videos()

        self.VideoPlayerMainWindow.mainloop()

    def calculate_grid_dimensions(self, num_videos):
        # Calculate the number of rows and columns in the grid
        self.columns = 3
        self.rows = (num_videos + self.columns - 1) // self.columns

        # Calculate the size of each video frame in the grid
        self.grid_width = self.VideoPlayerMainWindow.winfo_screenwidth() // self.columns
        self.grid_height = self.VideoPlayerMainWindow.winfo_screenheight() // self.rows

    def back_to_start_window(self):
        self.VideoPlayerMainWindow.destroy()
        root = customtkinter.CTk()
        app = App(root)
        app.root.mainloop()

    def play_videos(self):
        for video in self.videos:
            ret, frame = video['cap'].read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame)

                resized_image = image.resize((self.grid_width, self.grid_height))
                photo = ImageTk.PhotoImage(resized_image)

                video['canvas'].create_image(0, 0, image=photo, anchor=tk.NW)
                video['canvas'].image = photo
            else:
                placeholder_image = Image.open("images/placeholder.jpg").resize((self.grid_width, self.grid_height))
                placeholder_photo = ImageTk.PhotoImage(placeholder_image)

                video['canvas'].create_image(0, 0, image=placeholder_photo, anchor=tk.NW)
                video['canvas'].image = placeholder_photo

        self.VideoPlayerMainWindow.after(1, self.play_videos)


# Класс для работы с изображениями
class ImagePlayer:
    def __init__(self, img_list):
        self.image_list = img_list
        self.MainWindowForImagePlayer = tk.Tk()
        self.MainWindowForImagePlayer.title("Image Explorer")
        self.MainWindowForImagePlayer.geometry("800x600")
        self.MainWindowForImagePlayer.iconbitmap("images/pngwing.com.ico")

        self.image_labels = []

        self.open_images_dialog()
        self.MainWindowForImagePlayer.protocol('WM_DELETE_WINDOW', self.back_to_start_window)
        self.MainWindowForImagePlayer.mainloop()

    def back_to_start_window(self):
        self.MainWindowForImagePlayer.destroy()
        root = customtkinter.CTk()
        app = App(root)
        app.root.mainloop()

    def open_images_dialog(self):
        filenames = self.image_list

        # Clear existing images (if any)
        for image_label in self.image_labels:
            image_label.destroy()

        # Calculate image size based on the number of files
        num_files = len(filenames)
        max_size = 100  # Maximum size of the image
        min_size = 800  # Minimum size of the image
        if num_files == 0:
            image_size = min_size
        else:
            image_size = max_size - ((max_size - min_size) / num_files)

        # Create new image labels
        for i, filename in enumerate(filenames):
            row = i // 3
            column = i % 3
            path = 'images'
            if not os.path.exists(path):
                os.makedirs(path)
            if not os.path.exists('output_files'):
                os.makedirs('output_files')

            virat_img = cv2.imread(filename)
            borderoutput = cv2.copyMakeBorder(virat_img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[0, 0, 0])
            cv2.imwrite('images/output.png', borderoutput)

            result = model('images/output.png', save_txt=True, save_crop=True)

            print(result)
            for result_item in result:

                boxes = result_item.boxes.cpu().numpy()
                img = cv2.imread('images/output.png')

                for box in boxes:
                    r = box.xyxy[0].astype(int)
                    cls = box.cls[0].astype(int)
                    if cls == 0:
                        label = "Man with weapon"
                    if cls == 1:
                        label = "Short weapons"
                    if cls == 2:
                        label = "Long weapons"

                    box_color = class_colors.get(cls, (255, 255, 255))

                    (label_width, label_height), _ = cv2.getTextSize(label, class_font, class_font_scale, 1)

                    text_position = (r[0], r[1] - 3 - label_height)

                    cv2.rectangle(img, (r[0], r[1]), (r[2], r[3]), box_color, 2)
                    cv2.putText(img, label, text_position, class_font, class_font_scale, box_color, 2)
                    cv2.imwrite('images/output.png', img)
                    file_name = os.path.basename(filename)
                    shutil.copy2('images/output.png', f'output_files/{file_name}')

            image = Image.open('images/output.png')
            image = image.resize((int(image_size), int(image_size)))
            image = ImageTk.PhotoImage(image)

            image_label = tk.Label(self.MainWindowForImagePlayer, image=image)
            image_label.image = image
            image_label.grid(row=row, column=column, padx=10, pady=10)

            self.image_labels.append(image_label)

        os.remove('images/output.png')
        self.MainWindowForImagePlayer.update_idletasks()
        self.MainWindowForImagePlayer.geometry(
            f"{self.MainWindowForImagePlayer.winfo_reqwidth()}x{self.MainWindowForImagePlayer.winfo_reqheight()}")
        self.MainWindowForImagePlayer.resizable(width=False, height=False)


# Класс для создания сообщения (заглушка для камеры)
class Dialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.top.geometry('300x200')
        self.top.resizable(width=False, height=False)

        self.top.iconbitmap("images/pngwing.com.ico")
        self.myLabel = tk.Label(self.top, text='Введите ip адрес камеры')
        self.myLabel2 = tk.Label(self.top, text="Порт")
        self.myLabel.place(x=50, y=30)
        self.myLabel2.place(x=50, y=80)
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox2 = tk.Entry(top)
        self.myEntryBox2.place(x=50, y=50)
        self.myEntryBox.place(x=50, y=100)
        self.mySubmitButton = tk.Button(top, text='Подтвердить', command=self.send)
        self.mySubmitButton.place(x=50, y=150)

    def send(self):
        mb = tk.messagebox.showinfo(title='Не готово', message="Функция недоступна в данное время")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    root = customtkinter.CTk()
    app = App(root)
    root.mainloop()
