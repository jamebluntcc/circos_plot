#coding=utf-8
'''
this a script to tidy & quickly generate circos plot
version == 1.0 plot type:heatmap hist scatter
'''
import os
import sys
import json
import argparse

from main import circos_data_dir
from main.circos_plot import heatmap,hist,scatter,render_ideogram

'''
this is main python script to generate circos plot conf file
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create circos plot')
    parser.add_argument('output_path',help='a dir where you want to generate circos plot')
    parser.add_argument('--axes','-axes',action='store_true',default=False,help='whether show axes to plot default False')
    parser.add_argument('--pairwise','-pairwise',nargs='*',help='whether circos plot have a pairwise')
    args = parser.parse_args()

    with open('circos_info.json','r') as f:
        conf_info = json.load(f)

    conf_info['data'] = [os.path.join(circos_data_dir,each) for each in conf_info['data']]

    if args.pairwise:
        if len(args.pairwise) == 2:
            (gene1,gene2) = args.pairwise
            render_ideogram(args.output_path,gene1,gene2)
        elif len(args.pairwise) == 3:
            (gene1,gene2,spacing) = args.pairwise
            render_ideogram(args.output_path,gene1,gene2,spacing)
        else:
            print 'pairwise params Error!\nyour params seems: like gene1 gene2 spacing'
            sys.exit(1)


    if conf_info['type'] == 'heatmap':
        circos_heatmap = heatmap(conf_info['karyotype'],
                                 conf_info['data'],
                                 conf_info['other']['color'],
                                 conf_info['other']['scale_log_base'])
        circos_heatmap.render_template(args.output_path,axes=args.axes)
        circos_heatmap.run_circos(args.output_path,'heatmap_conf.conf')

    if conf_info['type'] == 'hist':
        circos_hist = hist(conf_info['karyotype'],
                           conf_info['data'],
                           conf_info['other']['fill_color'])
        circos_hist.render_template(args.output_path,axes=args.axes)
        circos_heatmap.run_circos(args.output_path,'hist_conf.conf')

    if conf_info['type'] == 'scatter':
        circos_scatter = scatter(conf_info['karyotype'],
                                 conf_info['data'],
                                 conf_info['other']['glyph'],
                                 conf_info['other']['glyph_size'])
        circos_scatter.render_template(args.output_path,axes=args.axes)
        circos_heatmap.run_circos(args.output_path,'scatter_conf.conf')
