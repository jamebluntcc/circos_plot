#coding=utf-8
#this a python script to generate circos plot
# version == 0.1 heatmap hist and scatter
import jinja2
import os
import configparser

test_dir = '/home/chencheng/onmath_project/circos_plot'
circos_env = jinja2.Environment(
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.join(test_dir,"templates"))
)
#some default configure
heatmap_color = ('brbg-3-div-rev','spectral-3-div-rev','rdbu-3-div-rev')
out_circle = 0.99  # or 0.95
paired_dist = 0.01
track_dist = 0.05
max_track_width = 0.2
# now we just have 5 plot layouts, you can add more in here
track_r = {'plot_1':['0.95r','0.75r'], #track_width = 0.2
               'plot_2':['0.95r','0.80r','0.65r','0.50r'], #track_width = 0.15 track_dist = 0.15
               'plot_3':['0.95r','0.80r','0.65r','0.50r','0.35r','0.20r'],
               'plot_4':['0.95r','0.80r','0.75r','0.60r','0.50r','0.35r','0.30r','0.15r'],
               'plot_6':['0.99r','0.89r','0.88r','0.78r','0.68r','0.58r','0.57r','0.47r','0.37r','0.27r','0.26r','0.16r']
               }

def create_track_r(plots_num):
    plot_key = '_'.join(['plot',str(plots_num)])
    if plot_key in track_r:
        return track_r.get(plot_key)

class circos_plot(object):
    def __init__(self,file,min,max,r1,r0):
        self.file = file
        self.min = min
        self.max = max
        self.r1 = r1
        self.r0 = r0
    def mesg(self):
        print "file:%s\nvalue_range:(%f,%f)\nr_range(%d,%d)"%(self.file,self.min,self.max,self.r0,self.r1)

class heatmap_plot(circos_plot):
    def __init__(self,color,scale_log_base):
        self.color = color
        self.scale_log_base = scale_log_base
    def get_scale_log_base(self):
        print "scale_log_base:%f\nheatmap_color:%s"%(self.scale_log_base,self.color)

class hist_plot(circos_plot):
    def __init__(self,fill_color):
        self.fill_color = fill_color
    def get_fill_color(self):
        print "fill_color:%s"%(self.fill_color)

class scatter_plot(circos_plot):
   def __init__(self,color,glyph,glyph_size):
       self.color = color
       self.glyph = glyph
       self.glyph_size = glyph_size

#template = circos_env.get_template('.conf')
if __name__ == "__main__":
    circos_data_dir = 'home/public/software/circos-0.69-3/circos-0.69-3/data/'

    command = configparser.ConfigParser()
    command.read('circos_plot.conf')
    plot_type = command.get('circos_plot','type')
    plot_data = command.get('circos_plot','data_list')
    value_range = command.get('circos_plot','range_list')
    karyotype = command.get('circos_plot','karyotype')

    plot_data_list = plot_data.split(',')
    value_range_list = value_range.split(',')
    plot_track = create_track_r(len(plot_data_list))

    if plot_type == 'heatmap':
        heatmap_color = command.get('circos_plot','color')
        heatmap_scale_log_base = command.get('circos_plot','scale_log_base')
        heatmap_scale_log_base_list = heatmap_scale_log_base.split(',')
        heatmap_color_list = heatmap_color.split(',')
        heatmap_track = plot_track

        heatmap_plot_list = []
        j = 0
        for i in range(len(plot_data_list)):
            tmp = heatmap_plot(scale_log_base=heatmap_scale_log_base_list[i],color=heatmap_color_list[i])
            tmp.file = plot_data_list[i]
            tmp.min = value_range_list[j]
            tmp.max = value_range_list[j+1]
            tmp.r1 = heatmap_track[j]
            tmp.r0 = heatmap_track[j+1]
            j = j + 2
            heatmap_plot_list.append(tmp)

        template = circos_env.get_template('circos_heatmap.conf')
        with open('test.conf', 'w') as f:
            f.write(template.render(chrom_name=karyotype,
                                plot_type=plot_type,
                                plots=heatmap_plot_list,
                                axes=True))


    elif plot_type == 'hist':
        hist_fill_color = command.get('circos_plot','fill_color')
        hist_fill_color_list = hist_fill_color.split(',')
        hist_track = plot_track

        hist_plot_list = []
        j = 0
        for i in range(len(plot_data_list)):
            tmp = hist_plot(fill_color=hist_fill_color_list[i])
            tmp.file = plot_data_list[i]
            tmp.min = value_range_list[j]
            tmp.max = value_range_list[j + 1]
            tmp.r1 = hist_track[j]
            tmp.r0 = hist_track[j + 1]
            j = j + 2
            hist_plot_list.append(tmp)

        template = circos_env.get_template('circos_hist.conf')
        with open('test2.conf', 'w') as f:
                f.write(template.render(chrom_name=karyotype,
                                        plot_type=plot_type,
                                        plots=hist_plot_list,
                                        hist_fill_color=False,
                                        axes=True))

    elif plot_type == 'scatter':
        scatter_color = command.get('circos_plot', 'color')
        scatter_glyph = command.get('circos_plot','glyph')
        scatter_glyph_size = command.get('circos_plot','glyph_size')
        scatter_glyph_list = scatter_glyph.split(',')
        scatter_color_list = scatter_color.split(',')
        scatter_glyph_size_list = scatter_glyph_size.split(',')
        scatter_track = plot_track

        scatter_plot_list = []
        j = 0
        for i in range(len(plot_data_list)):
            tmp = scatter_plot(color=scatter_color_list[i],glyph=scatter_glyph_list[i],glyph_size=scatter_glyph_size_list[i])
            tmp.file = plot_data_list[i]
            tmp.min = value_range_list[j]
            tmp.max = value_range_list[j + 1]
            tmp.r1 = scatter_track[j]
            tmp.r0 = scatter_track[j + 1]
            j = j + 2
            scatter_plot_list.append(tmp)

        template = circos_env.get_template('circos_scatter.conf')
        with open('test3.conf', 'w') as f:
            f.write(template.render(chrom_name=karyotype,
                                    plot_type=plot_type,
                                    plots=scatter_plot_list,
                                    axes=True))









