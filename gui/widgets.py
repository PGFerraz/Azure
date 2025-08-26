# Arquivo de configuração dos Widgets principais
from user import User
from kivy.uix.boxlayout import BoxLayout
from paths import *
from kivy.garden.graph import MeshLinePlot
import json

# Classe que contém os widgets principais
class MainLayout(BoxLayout):
    _imgDefaultAvatar = IMG_DEFAULT_AVATAR
    _imgConfigGear = IMG_CONFIG_GEAR
    _imgRegGlic = IMG_REG_GLIC
    _imgCnnNews = IMG_CNN_NEWS
    _imgLogoAzure = IMG_LOGO_AZURE

    # inicializando a classe
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        graph_day = self.ids.profile_graph_day
        graph_month = self.ids.profile_graph_month
        plot = MeshLinePlot(color=[0, 0.6, 1, 1])
        plot.points = [(x, x/10.0) for x in range(51)]
        plot_month = MeshLinePlot(color=[0, 0.6, 1, 1])
        plot_month.points = [(x, x/10.0) for x in range(51)]
        graph_day.add_plot(plot)
        graph_month.add_plot(plot_month)
    
    def show_password(self, checkbox, value):
        if value:
            self.ids.password.password = False
            self.ids.password_text.text = "Ocultar Senha"
        else:
            self.ids.password.password = True
            self.ids.password_text.text = "Mostrar Senha"
    
    def login_state(self, username):
        self.ids.profile_username.text = username

    def user_registration(self):
        reg_username = self.ids.username.text
        reg_password = self.ids.password.text
        if User().registrationGUI(reg_username, reg_password):
            self.login_state(reg_username)
            self.ids.screen_manager.current = 'screen_home'
            User.temp_login = [reg_username, reg_password]
        else:
            self.ids.login_status.text = "Por favor, preencha todos os campos."
        

    def user_login(self):
        login_username = self.ids.username.text
        login_password = self.ids.password.text
        try:
            with open(User.ud_json_path, 'r') as f:
                users = json.load(f)
                for user_data in users:
                    if user_data['name'] == login_username and user_data['password'] == login_password:
                        User.temp_login = [user_data['name'], user_data['password']]
                        self.login_state(login_username)
                        self.ids.screen_manager.current = 'screen_home'
                        return
                self.ids.login_status.text = "Usuário ou senha incorretos."
        except FileNotFoundError:
            self.ids.login_status.text = "Nenhum usuário registrado. Por favor, registre-se primeiro."
        except json.JSONDecodeError:
            self.ids.login_status.text = "Erro ao ler dados do usuário. O arquivo pode estar corrompido."
    

