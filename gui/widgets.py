# Arquivo de configuração dos Widgets principais
from kivy.uix.boxlayout import BoxLayout
from paths import *
from kivy.garden.graph import MeshLinePlot

# Classe que contém os widgets principais
class MainLayout(BoxLayout):
    _imgDefaultAvatar = IMG_DEFAULT_AVATAR
    _imgConfigGear = IMG_CONFIG_GEAR
    _imgRegGlic = IMG_REG_GLIC

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