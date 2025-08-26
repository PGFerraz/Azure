# Importando Módulos
import os
import webbrowser
from kivy.config import Config
Config.set('graphics', 'width', '422')
Config.set('graphics', 'height', '844')
from kivy.lang import Builder
from kivymd.app import MDApp
from gui.widgets import MainLayout

# Classe MDApp principal
class MainApp(MDApp):
    def build(self):
        # carrega o arquivo KV antes de retornar o layout
        Builder.load_file(os.path.join(os.path.dirname(__file__), "gui", "mainlayout.kv"))
        self.theme_cls.theme_style = "Dark"
        return MainLayout()

    def open_link(self, url):
        """Abre um link no navegador padrão"""
        webbrowser.open(url)

# Criando e executando o objeto da classe MainApp
MainApp().run()