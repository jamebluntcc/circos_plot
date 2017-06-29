#coding=utf-8
'''
this a script to tidy & quickly generate circos plot
version == 0.1 plot type:heatmap hist scatter
'''
import os
import json
import pandas as pd
from . import circos_env,track_r
circos_env = jinja2.Environment(
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.join(base_dir,"templates"))
)

class circos(object):

    def __init__(self,karyotype,data):
        self.karyotype = karyotype
        self.data = data[:]
        self.range = self._get_data_range()

    def _get_data_range(self):
        range_list = []

        for each in self.data:
            df = pd.read_table(each,header=None,sep=' ')
            range_list.extend([df[3].min(),df[3].max()])

        return range_list

    def create_track_r(plots_num):
        plot_key = '_'.join(['plot',str(plots_num)])
        if track_r.get(plot_key):
            return track_r[plot_key]


class heatmap(circos):

    def __init__(self,karyotype,data,color,scale_log_base):
        circos_plot.__init__(self,karyotype,data)
        self.color = color[:]
        self.scale_log_base = scale_log_base[:]

    def __repr__(self):
        print "<circos:heatmap>"

    def render_template(self,conf_path):
        render_plots = []
        track_range = _create_track_r(len(self.data))
        value_range = self._get_data_range()
        j=0
        for i in range(len(self.data)):
            tmp_dict = dict(file=self.data[i],min=value_range[j],
                            max=value_range[j+1],r0=track_range[j],r1=track_range[j+1],
                            color=self.color[i],scale_log_base=self.scale_log_base[i])
            j += 2
            render_plots.append(tmp_dict)

        template = circos_env.get_template('circos_heatmap.conf')
        with open(os.path.join(conf_path,'heatmap_conf.conf'),'w') as f:
            f.write(template.render(chrom_name=self.karyotype,
                                    plot_type='heatmap',
                                    plots=render_plots,
                                    axes=True))

class hist(circos):
