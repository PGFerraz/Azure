import json, os

class User:

    user_list = []  # Lista Contendo Usuários Registrados
    user_list_all = []  # Lista Contendo Todos os Usuários
    temp_login = []
    ud_json_path = os.path.join('userdata', 'user_reg.json')  # Caminho do arquivo JSON de registro de usuários

    @classmethod
    def from_dict(cls, data):
        user = cls()
        user.name = data['name']
        user.password = data['password']
        return user

    def __init__(self):
        self.name = 'Null'
        self.password = 'Null'

    @staticmethod
    def ud_main_folder_path(name):
        return os.path.join('userdata', f'{name}_main')

    @staticmethod
    def ud_main_user_json(name):
        return os.path.join('userdata', f'{name}_main', f'{name}_data.json')

    def create_user_data(self):
        os.makedirs(self.ud_main_folder_path(self.name), exist_ok=True)
        with open(self.ud_main_user_json(self.name), 'a') as f:
            json.dump(User.user_list, f, indent=4)
        with open(self.ud_json_path, 'a') as f:
            json.dump(User.user_list, f, indent=4)

    def registrationGUI(self, username, password):
        if not username or not password:
            return False

        self.name = username
        self.password = password

        # Salvando dados do usuário em seu respectivo arquivo JSON
        User.user_list.append({
            'id': 'data',
            'name': self.name,
            'password': self.password
        })
        os.makedirs(self.ud_main_folder_path(self.name), exist_ok=True)
        with open(self.ud_main_user_json(self.name), 'a') as f:
            json.dump(User.user_list, f, indent=4)

        # Atualizando o arquivo JSON principal de usuários
        User.user_list_all.append({
            'name': self.name,
            'password': self.password
        })
        with open(self.ud_json_path, 'w') as f:
            json.dump(User.user_list_all, f, indent=4)