from tkinter import Menu
from customtkinter import CTk

import i18n

from src.myworld.model.factories import project_factory
from src.myworld.model.project import Project
from src.myworld.view.viewport.world_viewport import WorldViewport


class EditorWindow(CTk):
    parent: any
    viewport: WorldViewport

    current_project: Project

    def __init__(self):
        super().__init__()
        self.build()

    def build(self):
        self.title(i18n.t("myworld.editor_window.title"))
        self.geometry("800x600")
        self._build_menu()
        self._build_widgets()

    def _build_menu(self):
        menu_bar = Menu(master=self)
        self._build_apple_menu(menu_bar)
        self._build_file_menu(menu_bar)
        self.config(menu=menu_bar)

    def _build_apple_menu(self, menu_bar):
        apple_menu = Menu(master=menu_bar, name="apple")
        menu_bar.add_cascade(menu=apple_menu)
        apple_menu.add_command(label=i18n.t("myworld.editor_window.menu.apple.about"), state="disabled")

    def _build_file_menu(self, menu_bar):
        file_menu = Menu(master=menu_bar, tearoff=0)
        menu_bar.add_cascade(label=i18n.t("myworld.editor_window.menu.file.title"), menu=file_menu)
        file_menu.add_command(label=i18n.t("myworld.editor_window.menu.file.new"), command=self.on_new_project)
        file_menu.add_command(label=i18n.t("myworld.editor_window.menu.file.open"))
        file_menu.add_command(label=i18n.t("myworld.editor_window.menu.file.save"))
        file_menu.add_command(label=i18n.t("myworld.editor_window.menu.file.save_as"))

    def _build_widgets(self):
        self.viewport = WorldViewport(master=self)
        self.viewport.pack(fill="both", expand=True)

    def on_new_project(self):
        # check if there is a project already, that perhaps needs to be saved

        # TODO: Remove, only for development
        self.current_project = project_factory.load_project_from_dir("res/assets/project_templates/demo_project")

        #self.current_project = project_factory.make_empty_project()
        self.viewport.world = self.current_project.worlds[0]
        self.viewport.update()
