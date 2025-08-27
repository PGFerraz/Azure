# Arquivo de configuração dos Widgets principais
from user import User
from kivy.uix.boxlayout import BoxLayout
from paths import *
from kivy_garden.graph import MeshLinePlot
import json, datetime, webbrowser
from kivy_garden.graph import SmoothLinePlot

# Classe que contém os widgets principais
class MainLayout(BoxLayout):
    _imgDefaultAvatar = IMG_DEFAULT_AVATAR
    _imgConfigGear = IMG_CONFIG_GEAR
    _imgRegGlic = IMG_REG_GLIC
    _imgCnnNews = IMG_CNN_NEWS
    _imgLogoAzure = IMG_LOGO_AZURE
    _imgCnnNews = IMG_CNN_NEWS
    _imgNoticia2 = IMG_NOTICIA2

    # inicializando a classe
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        graph_day = self.ids.profile_graph_day
        graph_month = self.ids.profile_graph_month

        # Configura escala fixa para o gráfico diário
        graph_day.xmin = 0
        graph_day.xmax = 24
        graph_day.ymin = 0
        graph_day.ymax = 300

        # Adiciona linhas de grade os valores
        graph_day.x_ticks_major = 6
        graph_day.y_ticks_major = 70

        # Adiciona os plots
        plot = MeshLinePlot(color=[0, 0.6, 1, 1])
        plot.points = []
        graph_day.add_plot(plot)

        # Escala fixa para o gráfico mensal
        graph_month.xmin = 0
        graph_month.xmax = 31
        graph_month.ymin = 0
        graph_month.ymax = 300
        plot_month = MeshLinePlot(color=[0, 0.6, 1, 1])
        plot_month.points = []
        graph_month.add_plot(plot_month)

        # Customiza os labels do eixo X e Y do gráfico diário
        graph_day.x_labels = ['06:00', '12:00', '18:00', '00:00']
        graph_day.y_labels = ['0', '70', '180', '300']

    # Função para abrir links externos
    def open_link(self, url):
        """Abre um link no navegador padrão"""
        webbrowser.open(url)

    def show_password(self, checkbox, value):
        if value:
            self.ids.password.password = False
            self.ids.password_text.text = "Ocultar Senha"
        else:
            self.ids.password.password = True
            self.ids.password_text.text = "Mostrar Senha"

    def login_state(self, username):
        self.ids.profile_username.text = username

    # Função para verificar se há usuário logado
    @staticmethod
    def is_user_logged_in():
        try:
            with open('last_user.json', 'r') as f:
                data = json.load(f)
                username = data.get('username')
                if username:
                    return username
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return None

    # Função para obter o usuário logado
    @staticmethod
    def get_logged_in_user():
        username = MainLayout.is_user_logged_in()
        if username:
            return username
        return None

    # Função para deslogar o usuário atual
    def logout_user(self):
        with open('last_user.json', 'w') as f:
            json.dump({}, f)

        # Limpa o estado do usuário atual na UI
        self.ids.profile_username.text = ""

        # Volta para tela de login/registro
        self.ids.screen_manager.current = 'screen_login'

    # Atualiza os gráficos com os dados do usuário
    def load_glicemia_records(self, username):
        user_json_path = User.ud_main_user_json(username)
        try:
            with open(user_json_path, 'r') as f:
                user_data = json.load(f)
                if not isinstance(user_data, dict):
                    user_data = {'name': username}
                return user_data.get('glycemia', {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # Função para atualizar gráfico mensal
    def update_monthly_graph(self, username):
        user_glycemia = self.load_glicemia_records(username)
        graph_month = self.ids.profile_graph_month

        # Remove plots antigos
        while graph_month.plots:
            graph_month.remove_plot(graph_month.plots[0])

        now = datetime.datetime.now()
        month_id = now.strftime("%Y-%m")
        month_points = []

        # Filtra dias do mês atual
        days_in_month = [day for day in user_glycemia if day.startswith(month_id)]
        days_in_month.sort()

        # Calcula média diária
        for day in days_in_month:
            values = [entry['value'] for entry in user_glycemia[day]]
            avg_value = sum(values) / len(values) if values else 0
            day_num = int(day.split('-')[2])
            month_points.append((day_num, avg_value))

        # Linha principal
        plot_month = SmoothLinePlot(color=[0, 0.6, 1, 1])
        plot_month.points = month_points if month_points else []
        graph_month.add_plot(plot_month)
        
        for x, y in month_points:
            dot = MeshLinePlot(color=[1, 1, 1, 1])
            dot.points = [(x, y), (x + 0.1, y + 5)]
            dot.line_width = 14
            graph_month.add_plot(dot)

        # Limites do gráfico
        graph_month.xmin = 0
        graph_month.xmax = 31
        graph_month.ymin = 0
        graph_month.ymax = 300

    def update_daily_graph(self, username):
        user_glycemia = self.load_glicemia_records(username)
        graph_day = self.ids.profile_graph_day

        # limpa plots anteriores
        while graph_day.plots:
            graph_day.remove_plot(graph_day.plots[0])

        # linha principal
        plot_day = MeshLinePlot(color=[0, 0.6, 1, 1])
        plot_day.line_width = 2

        now = datetime.datetime.now()
        day_id = now.strftime("%Y-%m-%d")
        day_points = []

        for entry in user_glycemia.get(day_id, []):
            try:
                hour = int(entry['time'].split(':')[0])
                minute = int(entry['time'].split(':')[1])
                value = float(entry['value'])
                x = hour + minute / 60.0
                day_points.append((x, value))
            except (ValueError, TypeError, KeyError):
                continue

        if day_points:
            # adiciona a linha principal
            plot_day.points = day_points
            graph_day.add_plot(plot_day)

            # adiciona bolinhas em cada ponto
            for x, y in day_points:
                dot = MeshLinePlot(color=[1, 0.3, 0, 1])
                dot.points = [(x, y), (x, y + 5)]
                dot.line_width = 18
                graph_day.add_plot(dot)

        # configura eixos
        graph_day.xmin = 0
        graph_day.xmax = 24
        graph_day.ymin = 0
        graph_day.ymax = 300
        graph_day.x_ticks_major = 6
        graph_day.y_ticks_major = 70
        graph_day.x_labels = ['06:00', '12:00', '18:00', '00:00']
        graph_day.y_labels = ['0', '70', '180', '300']

    # Salva o último usuário logado
    @staticmethod
    def save_last_logged_in_user(username):
        with open('last_user.json', 'w') as f:
            json.dump({'username': username}, f)

    # Função para registrar nova glicemia
    def register_glycemia(self):
        glycemia_value = self.ids.glycemia_input.text
        try:
            glycemia_value = float(glycemia_value)
        except (ValueError, TypeError):
            self.ids.glycemia_status.text = "Valor inválido."
            return
        now = datetime.datetime.now()
        day_id = now.strftime("%Y-%m-%d")
        time_id = now.strftime("%H:%M:%S")
        username = self.ids.profile_username.text
        user_json_path = User.ud_main_user_json(username)
        # carrega dados existentes
        try:
            with open(user_json_path, 'r') as f:
                user_data = json.load(f)
                if not isinstance(user_data, dict):
                    user_data = {'name': username}
        except (FileNotFoundError, json.JSONDecodeError):
            user_data = {'name': username}
        # registra nova glicemia
        if 'glycemia' not in user_data:
            user_data['glycemia'] = {}
        if day_id not in user_data['glycemia']:
            user_data['glycemia'][day_id] = []
        user_data['glycemia'][day_id].append({'time': time_id, 'value': glycemia_value})
        # salva dados atualizados
        with open(user_json_path, 'w') as f:
            json.dump(user_data, f, indent=2)
        # atualiza status e limpa input
        self.ids.glycemia_status.text = f"Glicemia {glycemia_value} mg/dL registrada!"
        self.ids.glycemia_input.text = ""
        graph_day = self.ids.profile_graph_day
        # atualiza gráfico diário
        while graph_day.plots:
            graph_day.remove_plot(graph_day.plots[0])
        # Line plot
        plot_day = MeshLinePlot(color=[0, 0.6, 1, 1])
        plot_day.line_width = 3
        day_points = []
        for entry in user_data['glycemia'][day_id]:
            try:
                hour = int(entry['time'].split(':')[0])
                minute = int(entry['time'].split(':')[1])
                value = float(entry['value'])
                x = hour + minute / 60.0
                day_points.append((x, value))
            except (ValueError, TypeError, KeyError):
                continue
        if day_points:
            plot_day.points = day_points
            graph_day.add_plot(plot_day)
            for x, y in day_points:
                dot = SmoothLinePlot(color=[1, 0.3, 0, 1])
                dot.points = [(x, y)]
                dot.line_width = 0
                dot.marker = 'circle'
                dot.marker_size = 8
                graph_day.add_plot(dot)
        graph_day.xmin = 0
        graph_day.xmax = 24
        graph_day.ymin = 0
        graph_day.ymax = 300
        graph_day.x_ticks_major = 6
        graph_day.y_ticks_major = 70
        graph_day.x_labels = ['06:00', '12:00', '18:00', '00:00']
        graph_day.y_labels = ['0', '70', '180', '300']

        graph_month = self.ids.profile_graph_month
        while graph_month.plots:
            graph_month.remove_plot(graph_month.plots[0])
        plot_month = MeshLinePlot(color=[0, 0.6, 1, 1])
        plot_month.line_width = 3
        month_id = now.strftime("%Y-%m")
        month_points = []
        days_in_month = [day for day in user_data['glycemia'] if day.startswith(month_id)]
        days_in_month.sort()
        for day in days_in_month:
            values = [entry['value'] for entry in user_data['glycemia'][day]]
            avg_value = sum(values) / len(values) if values else 0
            day_num = int(day.split('-')[2])
            month_points.append((day_num, avg_value))
        plot_month.points = month_points if month_points else []
        graph_month.add_plot(plot_month)

        # Adiciona marcadores
        for x, y in month_points:
            dot = SmoothLinePlot(color=[1, 0.3, 0, 1])
            dot.points = [(x, y)]
            dot.line_width = 0
            dot.marker = 'circle'
            dot.marker_size = 8
            graph_month.add_plot(dot)

        graph_month.xmin = 0
        graph_month.xmax = 31
        graph_month.ymin = 0
        graph_month.ymax = 300

        # Volta para o perfil do usuário
        self.ids.screen_manager.current = 'screen_profile'
    
    # Função para registrar novo usuário
    def user_registration(self):
        try:
            reg_username = self.ids.username.text
            reg_password = self.ids.password.text
            if not reg_username or not reg_password:
                if 'login_status' in self.ids:
                    self.ids.login_status.text = "Por favor, preencha todos os campos."
                return

            # Cria o usuário
            User().registrationGUI(reg_username, reg_password)

            # Faz login automático
            self.login_state(reg_username)
            User.temp_login = [reg_username, reg_password]

            # Salva como último usuário logado
            self.save_last_logged_in_user(reg_username)

            # Atualiza gráficos
            self.update_daily_graph(reg_username)
            self.update_monthly_graph(reg_username)

            # Vai para tela inicial
            self.ids.screen_manager.current = 'screen_home'

        except KeyError as e:
            print(f"Erro: id '{e.args[0]}' não encontrado no layout.")

        
    # Função para fazer login do usuário
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
                        self.save_last_logged_in_user(login_username)
                        
                        self.update_daily_graph(login_username)
                        self.update_monthly_graph(login_username)
                        
                        self.ids.screen_manager.current = 'screen_home'
                        return
                self.ids.login_status.text = "Usuário ou senha incorretos."
        except FileNotFoundError:
            self.ids.login_status.text = "Nenhum usuário registrado. Por favor, registre-se primeiro."
        except json.JSONDecodeError:
            self.ids.login_status.text = "Erro ao ler dados do usuário. O arquivo pode estar corrompido."