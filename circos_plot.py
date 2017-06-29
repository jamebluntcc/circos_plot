#coding=utf-8
'''
this a script to tidy & quickly generate circos plot
version == 0.1 plot type:heatmap hist scatter
'''
import os
import json
import pandas as pd
from . import circos_env,track_r

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

    def create_track_r(self,plots_num):
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

    def render_template(self,conf_path,axes=True):
        render_plots = []
        track_range = self.create_track_r(len(self.data))
        value_range = self._get_data_range()
        j=0
        for i in range(len(self.data)):
            tmp_dict = dict(file=self.data[i],min=value_range[j],
                            max=value_range[j+1],r0=track_range[j],r1=track_range[j+1],
                            color=self.color[i],scale_log_base=self.scale_log_base[i])
            j += 2
            render_plots.append(tmp_dict)

        template = circos_env.get_template('circos_heatmap.conf')
        render_dict = dict(chrom_name=self.karyotype,plot_type='heatmap',plots=render_plots,axes=axes)

        with open(os.path.join(conf_path,'heatmap_conf.conf'),'w') as f:
            f.write(template.render(render_dict))

class hist(circos):

    def __init__(self,karyotype,data,fill_color):
        circos_plot.__init__(self,karyotype,data)
        self.fill_color = fill_color[:]
        self.scale_log_base = scale_log_base[:]

    def __repr__(self):
        print "<circos:hist>"

    def render_template(self,conf_path,hist_fill_color=True,axes=True):
        render_plots = []
        track_range = self.create_track_r(len(self.data))
        value_range = self._get_data_range()
            j=0
            for i in range(len(self.data)):
                tmp_dict = dict(file=self.data[i],min=value_range[j],
                                max=value_range[j+1],r0=track_range[j],r1=track_range[j+1],
                                fill_color=self.fill_color[i],)
                j += 2
                render_plots.append(tmp_dict)

        template = circos_env.get_template('circos_hist.conf')

        render_dict = dict(chrom_name=self.karyotype,plot_type='hist',
                           plots=render_plots,hist_fill_color=hist_fill_color,axes=axes)

        with open(os.path.join(conf_path,'hist_conf.conf'),'w') as f:
            f.write(template.render(render_dict))

class scatter(circos):

    def __init__(self,karyotype,data,color,glyph,glyph_size):
        circos_plot.__init__(self,karyotype,data)
        self.color = color[:]
        self.glyph = glyph[:]
        self.glyph_size = glyph_size[:]

    def __repr__(self):
        print "<circos:scatter>"

    def render_template(self,conf_path,axes=True):
        render_plots = []
        track_range = self.create_track_r(len(self.data))
        value_range = self._get_data_range()
        j=0
        for i in range(len(self.data)):
            tmp_dict = dict(file=self.data[i],min=value_range[j],
                            max=value_range[j+1],r0=track_range[j],r1=track_range[j+1],
                            color=self.color[i],
                            glyph=seif.glyph[i],
                            glyph_size=self.glyph_size[i])
            j += 2
            render_plots.append(tmp_dict)

        template = circos_env.get_template('circos_hist.conf')

        render_dict = dict(chrom_name=self.karyotype,plot_type='scatter',
                           plots=render_plots,axes=axes)

        with open(os.path.join(conf_path,'scatter_conf.conf'),'w') as f:
            f.write(template.render(render_dict))
