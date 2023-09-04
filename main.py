import os
import pathlib
import shutil
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
from customtkinter import ThemeManager
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

HOME_DIR = ALBUM_DIR = os.path.expanduser("~")
DEFAULT_DISPLAY_SIZE = (700, 500)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.images = []
        self.album_images = []
        self.current_image_idx = 0
        self.current_image = None

        self.display_size = DEFAULT_DISPLAY_SIZE

        self.geometry("500x500")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.load_assets()
        self.set_layout()

    def set_layout(self):
        # Create the config frame
        self.settings_frame = ctk.CTkFrame(master=self)
        self.settings_frame.grid(row=0, column=0, sticky="nsew")
        self.settings_frame.grid_rowconfigure(8, weight=1)
        self.set_settings_menu()

        self.image_selectors_frame = ctk.CTkFrame(master=self)
        self.image_selectors_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.set_image_display()

    def load_assets(self):
        assets_path = pathlib.Path("./assets")
        self.folder_icon = ctk.CTkImage(
            Image.open(assets_path / "folder_icon.png"), size=(20, 20)
        )

    def set_settings_menu(self):
        # Source path
        self.source_path = tk.StringVar(value=HOME_DIR)

        source_path_title = ctk.CTkLabel(
            master=self.settings_frame, text="Images", font=("Arial", 16)
        )
        source_path_title.grid(row=0, column=0, sticky="nw", padx=10, pady=(10, 0))

        source_frame = ctk.CTkFrame(master=self.settings_frame)
        source_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        source_path_entry = ctk.CTkEntry(
            master=source_frame,
            width=150,
            textvariable=self.source_path,
        )
        source_path_entry.grid(row=0, column=0, sticky="nsew")
        frame_fg_color = ThemeManager.theme["CTkFrame"]["fg_color"][1]

        self.source_path_button = ctk.CTkButton(
            master=source_frame,
            text="",
            image=self.folder_icon,
            fg_color=frame_fg_color,
            bg_color=frame_fg_color,
            width=10,
            command=lambda: self.get_path(
                self.source_path.get(), "Select Image Directory", self.source_path
            ),
        )
        self.source_path_button.grid(row=0, column=1, sticky="nsew")

        # Album path
        # self.album_path = tk.StringVar(value=HOME_DIR)
        self.album_path = tk.StringVar(value=ALBUM_DIR)

        album_path_title = ctk.CTkLabel(
            master=self.settings_frame, text="Album", font=("Arial", 16)
        )
        album_path_title.grid(row=2, column=0, sticky="nw", padx=10, pady=(10, 0))

        album_frame = ctk.CTkFrame(master=self.settings_frame)
        album_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.album_path_entry = ctk.CTkEntry(
            master=album_frame, width=150, textvariable=self.album_path
        )
        self.album_path_entry.grid(row=0, column=0, sticky="nsew")
        self.album_path_button = ctk.CTkButton(
            master=album_frame,
            text="",
            image=self.folder_icon,
            fg_color=frame_fg_color,
            bg_color=frame_fg_color,
            width=10,
            command=lambda: self.get_path(
                self.album_path.get(), "Select Album Directory", self.album_path
            ),
        )
        self.album_path_button.grid(row=0, column=1, sticky="nsew")

        # Album name
        self.album_name = tk.StringVar(value="New Album")
        album_name_title = ctk.CTkLabel(
            master=self.settings_frame, text="Album Name", font=("Arial", 16)
        )
        album_name_title.grid(row=4, column=0, sticky="nw", padx=10, pady=(10, 0))
        self.album_name_entry = ctk.CTkEntry(
            master=self.settings_frame, width=150, textvariable=self.album_name
        )
        self.album_name_entry.grid(
            row=5, column=0, sticky="nsew", padx=10, columnspan=2
        )

        # Create the start button
        self.start_button = ctk.CTkButton(
            master=self.settings_frame,
            text="Start",
            command=self.configure,
        )
        self.start_button.grid(
            row=6, column=0, sticky="nsew", padx=10, pady=(10, 0), columnspan=2
        )

        # Display album size
        self.album_size_label = ctk.CTkLabel(master=self.settings_frame, text="")
        self.album_size_label.grid(
            row=7, column=0, sticky="nsew", padx=10, pady=(10, 0), columnspan=2
        )

    def set_image_display(self):
        self.accept_button = ctk.CTkButton(
            master=self.image_selectors_frame,
            text="Accept",
            width=10,
            command=self.accept_image,
        )
        self.accept_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.reject_button = ctk.CTkButton(
            master=self.image_selectors_frame,
            text="Reject",
            width=10,
            command=self.reject_image,
        )
        self.reject_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.disable_buttons()

        width, height = self.display_size
        self.image_label = ctk.CTkLabel(
            master=self.image_selectors_frame,
            width=width,
            height=height,
            text="",
        )

        self.image_label.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=10, columnspan=2
        )
        # set the image counter
        self.image_counter = ctk.CTkLabel(master=self.image_selectors_frame, text="")
        self.image_counter.grid(
            row=2, column=0, sticky="nsew", padx=10, pady=10, columnspan=2
        )

    def get_path(self, initial_dir, title, tkvar):
        path = filedialog.askdirectory(initialdir=initial_dir, title=title)
        tkvar.set(path)

    def start(self):
        self.configure()
        self.display_image(self.images[self.current_image_idx])
        self.enable_buttons()

    def configure(self):
        self.images = []
        self.album_images = []
        # Build the required directories
        source_dir = pathlib.Path(self.source_path.get())

        album_dir = pathlib.Path(self.album_path.get()) / self.album_name.get()
        if not os.path.exists(album_dir):
            os.makedirs(album_dir, exist_ok=True)
            os.makedirs(album_dir / ".rejected", exist_ok=True)

        if not os.path.exists(source_dir):
            raise ValueError("Source directory does not exist")

        # Get the images
        self.images, self.album_images = self.load_new_images()

        # Display the first image
        self.current_image_idx = 0
        self.album_size_label.configure(
            text=f"Album size: {len(self.album_images)} images"
        )

    def load_new_images(self):
        source_dir = pathlib.Path(self.source_path.get())
        album_dir = pathlib.Path(self.album_path.get()) / self.album_name.get()
        album_images, rejected_images = self.load_album_images(album_dir)
        image_extensions = [".jpg", ".jpeg", ".png"]
        images = []

        for image in source_dir.iterdir():
            if image.name in album_images or image.name in rejected_images:
                continue
            if image.suffix.lower() in image_extensions:
                images.append(image)
        return images, album_images

    def accept_image(self):
        image = self.images[self.current_image_idx]
        album_dir = pathlib.Path(self.album_path.get()) / self.album_name.get()
        shutil.copy(image, album_dir / image.name)
        self.album_images.append(image)
        self.album_size_label.configure(
            text=f"Album size: {len(self.album_images)} images"
        )
        self.current_image_idx += 1
        if self.current_image_idx >= len(self.images):
            self.clear_image()
            self.disable_buttons()
        else:
            self.display_image(self.images[self.current_image_idx])

    def scale_image(self, image: Image.Image, display_size: tuple):
        width, height = image.size
        if width > height:
            new_width = display_size[0]
            new_height = int(height * (new_width / width))
        else:
            new_height = display_size[1]
            new_width = int(width * (new_height / height))
        return image.resize((new_width, new_height))

    def reject_image(self):
        image = self.images[self.current_image_idx]
        album_dir = pathlib.Path(self.album_path.get()) / self.album_name.get()
        shutil.copy(image, album_dir / ".rejected" / image.name)
        self.current_image_idx += 1
        if self.current_image_idx >= len(self.images):
            self.clear_image()
            self.disable_buttons()
        else:
            self.display_image(self.images[self.current_image_idx])

    def disable_buttons(self):
        self.accept_button.configure(state="disabled")
        self.reject_button.configure(state="disabled")

    def enable_buttons(self):
        self.accept_button.configure(state="normal")
        self.reject_button.configure(state="normal")

    def clear_image(self):
        if self.current_image is not None:
            self.current_image.close()

    def display_image(self, image_path: pathlib.Path):
        if self.current_image is not None:
            self.current_image.close()
        image = Image.open(image_path)
        scaled_image = self.scale_image(image, self.display_size)
        image.close()
        self.current_image = scaled_image
        image_width, image_height = scaled_image.size
        tk_image = ctk.CTkImage(scaled_image, size=(image_width, image_height))
        self.image_label.configure(image=tk_image)
        self.image_counter.configure(
            text=f"{self.current_image_idx + 1}/{len(self.images)}"
        )

    def load_album_images(self, album_path: pathlib.Path):
        album_images = []
        rejected_images = []

        for image in album_path.iterdir():
            if image.is_file():
                album_images.append(image.name)

        for image in (album_path / ".rejected").iterdir():
            if image.is_file():
                rejected_images.append(image.name)

        return album_images, rejected_images


if __name__ == "__main__":
    app = App()

    app.mainloop()
