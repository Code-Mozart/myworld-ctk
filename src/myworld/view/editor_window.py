from tkinter import Menu
from customtkinter import CTk, CTkToplevel

import i18n


class EditorWindow(CTk):
    parent: any

    def __init__(self):
        super().__init__()
        self.build()

    def build(self):
        self.title(i18n.t("myworld.editor_window.title"))
        self.geometry("800x600")
        self._build_menu()
        self._build_widgets()

    def _build_menu(self):
        menu_bar = Menu(self)

        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=i18n.t("myworld.editor_window.menu.file.title"), menu=file_menu)
        file_menu.add_command(label=i18n.t("myworld.editor_window.menu.file.new"))
        file_menu.add_command(label=i18n.t("myworld.editor_window.menu.file.open"))
        file_menu.add_command(label=i18n.t("myworld.editor_window.menu.file.save"))
        file_menu.add_command(label=i18n.t("myworld.editor_window.menu.file.save_as"))

        self.config(menu=menu_bar)

    def _build_widgets(self):
        pass
