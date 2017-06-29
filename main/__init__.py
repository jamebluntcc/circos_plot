# coding=utf-8
'''
circos plot init file
circos_plot's configure
'''
import os
import jinja2
import configparser

base_dir = os.path.join(__file__)
configFilePath = os.path.join(base_dir,'circos_plot.conf')

command = configparser.Configparser()
command.read(configFilePath)

circos_data_dir = command.get('circos_config','circos_data_dir')

circos_env = jinja2.Environment(
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.join(base_dir,"templates"))
)

heatmap_color = ('brbg-3-div-rev','spectral-3-div-rev','rdbu-3-div-rev')

circos_conf = {'out_circle':0.99,
               'paired_dist':0.01,
               'track_dist':0.05,
               'max_track_width'：0.2}

track_r = {'plot_1':['0.95r','0.75r'], #track_width = 0.2
           'plot_2':['0.95r','0.80r','0.65r','0.50r'], #track_width = 0.15 track_dist = 0.15
           'plot_3':['0.95r','0.80r','0.65r','0.50r','0.35r','0.20r'],
           'plot_4':['0.95r','0.80r','0.75r','0.60r','0.50r','0.35r','0.30r','0.15r'],
           'plot_6':['0.99r','0.89r','0.88r','0.78r','0.68r','0.58r','0.57r','0.47r','0.37r','0.27r','0.26r','0.16r']
          }
