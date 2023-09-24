import i18n
from customtkinter import CTk

from src.myworld.view.editor_window import EditorWindow

if __name__ == '__main__':
    i18n.load_path.append("res/locales")

    application = EditorWindow()
    application.mainloop()
