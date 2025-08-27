# Importando Módulos
import os
#from kivy.config import Config
#Config.set('graphics', 'width', '422')
#Config.set('graphics', 'height', '844')
from kivy.lang import Builder
from kivymd.app import MDApp
from gui.widgets import MainLayout
  
# Classe MDApp principal
class MainApp(MDApp):
    def build(self):
        Builder.load_file(os.path.join(os.path.dirname(__file__), "gui", "mainlayout.kv"))
        self.theme_cls.theme_style = "Dark"
        layout = MainLayout()

        # Verifica se há usuário salvo
        last_user = layout.get_logged_in_user()
        if last_user:
            layout.login_state(last_user)
            layout.update_daily_graph(last_user)
            layout.update_monthly_graph(last_user)
            layout.ids.screen_manager.current = "screen_home"

        return layout
      
# Criando e executando o objeto da classe MainApp

MainApp().run()
