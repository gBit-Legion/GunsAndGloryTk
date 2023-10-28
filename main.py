import tkinter as tk
from tkinter import filedialog as fd, messagebox, ttk, Canvas, Button
import mimetypes

import customtkinter
import cv2
from PIL import Image, ImageTk
from ttkthemes import ThemedTk


class App():
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")
        self.root.title("Guns and Glory")
        self.root.geometry('600x400')
        self.root.config(bg="#E5E5E5")
        self.root.resizable(width=False, height=False)

        root.iconbitmap("pngwing.com.png")

        self.menu = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Сохранить")

        self.menu.add_cascade(label="Файл", menu=self.file_menu)
        self.menu.add_command(label="О программе", command=self.add_message)
        self.menu.add_command(label="Выйти", command=root.destroy)

        self.root.config(menu=self.menu)

        #Стили фреймов
        self.style = ttk.Style()
        self.style.configure("RoundedFrame.TFrame", background="#14213D", borderedwidth=5, borderradius=200)

        # Создаем фреймы
        self.frame1 = ttk.Frame(self.root, style="RoundedFrame.TFrame")
        self.frame1.place(height=400, width=300, x=50, y=50)
        self.frame2 = ttk.Frame(root, style="RoundedFrame.TFrame")
        self.frame2.place(height=400, width=300, x=390, y=50)

        # Создаем рамку для картинки
        self.canvas = tk.Canvas(self.frame1, width=150, height=150, bg='#14213D')
        self.img = Image.open('icons8-бобина-с-пленкой-90.png')
        self.new_image = self.img.resize((150, 150))
        self.image = ImageTk.PhotoImage(self.new_image)
        self.canvas.create_image(75, 75, image=self.image)
        self.canvas.place(width=150, height=150, x=75, y=75)

        # Cоздаем картинку для второго фрейма
        self.canvas2 = tk.Canvas(self.frame2, width=150, height=150, bg='#14213D')
        self.img2 = Image.open('security-camera.png')
        self.new_image = self.img2.resize((150, 150))
        self.image2 = ImageTk.PhotoImage(self.new_image)
        self.canvas2.create_image(75, 75, image=self.image2)
        self.canvas2.place(width=150, height=150, x=75, y=75)

        # Добавляем кнопки
        self.btn = ttk.Button(self.frame1, text="Выберите фото", style='Accent.TButton', command=self.image_dialog)
        self.btn.place(width=150, height=50, x=75, y=250)
        self.btn2 = ttk.Button(self.frame1, text="Выберите видео", style='Accent.TButton',
                               command=self.file_open_video_dialog)
        self.btn2.place(width=150, height=50, x=75, y=320)
        self.btn3 = ttk.Button(self.frame2, text="Подключить камеру", style='Accent.TButton',
                               command=self.camera_dialog)
        self.btn3.place(width=150, height=50, x=75, y=280)



    def file_open_dialog(self):
        filetypes = ('Файлы изображений', '*.jpeg'), ('Файлы видео', '*.mp4'), ('Все файлы', '*.*')

        filenames = fd.askopenfilenames(title='Open a file', initialdir='/', filetypes=filetypes)

    def image_dialog(self):
        filetypes = (("Файлы изображеий", "*.jpeg *.png *.jpg"),)
        filenames = fd.askopenfilenames(title='Open a file', initialdir='/', filetypes=filetypes)
        self.root.destroy()
        ip = ImagePlayer(filenames)
        ip.root.TopLevel()

    def camera_dialog(self):
        dialog = Dialog(self.root)

    def file_open_video_dialog(self):
        filetypes = (("Файлы видео", "*.mp4"),)

        filenames = fd.askopenfilenames(title='Open a file', initialdir='/', filetypes=filetypes)
        # сюда нужно подставить обработку файлов
        self.root.destroy()
        vp = VideoPlayer(filenames)
        vp.root.TopLevel()

        # подставляем обработку видео

    def add_message(self):
        tk.messagebox.showinfo(title="Реклама", message="Вступайте в ряды МВД России")


class VideoPlayer:
    def __init__(self, video_paths):
        self.video_paths = video_paths
        self.videos = []


        self.root = tk.Tk()
        self.root.title("Video Player")

        small_icon = tk.PhotoImage(file="pngwing.com.png")
        large_icon = tk.PhotoImage(file="pngwing.com.png")
        self.root.iconphoto(False, large_icon, small_icon)

        self.frames = []
        self.canvases = []

        self.calculate_grid_dimensions(len(self.video_paths))
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        for i in range(self.rows):
            for j in range(self.columns):
                index = i * self.columns + j
                if index < len(self.video_paths):
                    path = self.video_paths[index]
                    cap = cv2.VideoCapture(path)
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                    video_frame = tk.Frame(self.root, width=self.grid_width, height=self.grid_height)
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
                    placeholder_frame = tk.Frame(self.root, width=self.grid_width, height=self.grid_height)
                    placeholder_frame.grid(row=i, column=j)

                    placeholder_image = Image.open("placeholder.jpg").resize((self.grid_width, self.grid_height))
                    placeholder_photo = ImageTk.PhotoImage(placeholder_image)
                    placeholder_label = tk.Label(placeholder_frame, image=placeholder_photo)
                    placeholder_label.image = placeholder_photo
                    placeholder_label.pack()
        self.root.protocol('WM_DELETE_WINDOW', self.back_to_start_window)

        self.play_videos()

        self.root.mainloop()

    def calculate_grid_dimensions(self, num_videos):
        # Calculate the number of rows and columns in the grid
        self.columns = 3
        self.rows = (num_videos + self.columns - 1) // self.columns

        # Calculate the size of each video frame in the grid
        self.grid_width = self.root.winfo_screenwidth() // self.columns
        self.grid_height = self.root.winfo_screenheight() // self.rows

    def back_to_start_window(self):
        self.root.destroy()
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
                placeholder_image = Image.open("placeholder.jpg").resize((self.grid_width, self.grid_height))
                placeholder_photo = ImageTk.PhotoImage(placeholder_image)

                video['canvas'].create_image(0, 0, image=placeholder_photo, anchor=tk.NW)
                video['canvas'].image = placeholder_photo

        self.root.after(1, self.play_videos)


class ImagePlayer:
    def __init__(self, img_list):
        self.image_list = img_list
        self.root = tk.Tk()
        self.root.title("Image Explorer")
        self.root.geometry("800x600")
        small_icon = tk.PhotoImage(file="pngwing.com.png")
        large_icon = tk.PhotoImage(file="pngwing.com.png")
        self.root.iconphoto(False, large_icon, small_icon)

        self.image_labels = []

        self.open_images_dialog()
        self.root.protocol('WM_DELETE_WINDOW', self.back_to_start_window)
        self.root.mainloop()

    def back_to_start_window(self):
        self.root.destroy()
        root = customtkinter.CTk()
        app = App(root)
        app.root.mainloop()

    def open_images_dialog(self):
        filenames = self.image_list

        # Clear existing images (if any)
        for image_label in self.image_labels:
            image_label.destroy()

        # Create new image labels
        for i, filename in enumerate(filenames):
            row = i // 3
            column = i % 3

            image = Image.open(filename)
            image = image.resize((200, 200))
            image = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.root, image=image)
            image_label.image = image
            image_label.grid(row=row, column=column, padx=10, pady=10)  # Добавлены отступы для отделения изображений
            self.image_labels.append(image_label)

        self.root.update_idletasks()  # Обновление размеров окна
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")  # Изменение размеров окна

        self.root.resizable(width=False, height=False)


class Dialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.top.geometry('300x200')
        self.top.resizable(width=False, height=False)

        small_icon = tk.PhotoImage(file="pngwing.com.png")
        large_icon = tk.PhotoImage(file="pngwing.com.png")
        self.top.iconphoto(False, large_icon, small_icon)
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
        self.mb = tk.messagebox.showinfo(title='Не готово', message="Функция недоступна в данное время")


class GradientFrame(tk.Canvas):
    '''A gradient frame which uses a canvas to draw the background'''

    def __init__(self, parent, color1="red", color2="black", **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2 - r1) / limit
        g_ratio = float(g2 - g1) / limit
        b_ratio = float(b2 - b1) / limit
        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(i, 0, i, height, tags=("gradient",), fill=color)
        self.lower("gradient")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("Dark")
    root = customtkinter.CTk()
    app = App(root)
    root.mainloop()
