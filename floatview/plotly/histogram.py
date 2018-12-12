from .glueplotly import GluePlotly
from plotly.graph_objs import FigureWidget
import numpy as np

class GlueHistogramPlotly (GluePlotly):
    def __init__(self, data, dimensions, **kwargs):
        GluePlotly.__init__(self, data, dimensions, **kwargs)
        self.DefaultLayoutTitles("", self.dimensions[0], ' '.join([self.dimensions[i] for i in range(1,len(self.dimensions))]))                
        self.updateRender()
        
    def createFigureWidget(self):
        x_id=self.dimensions[0]
        d_val = self.data[x_id]
        if hasattr(self.data[x_id], 'codes'):
            d_val = self.data[x_id].codes
        hist, bin_edges  = np.histogram(d_val, bins='auto')
        xedges = []
        for i in range(len(bin_edges)-1):
            xedges.append((bin_edges[i+1]+bin_edges[i])/2)
        traces = []
        trace = {
            'type': "bar", 'name': self.data.label,
            'marker' : {'color': 'rgba(0, 0, 0, 0.1)'},
            'x': xedges,
            'y': hist,
        }
        if self.only_subsets == False:        
            traces.append(trace)
        for sset in self.data.subsets:
            s_val = sset[x_id]
            if hasattr(sset[x_id], 'codes'):
                s_val = sset[x_id].codes
            hist, bin_edges  = np.histogram(s_val, range=(bin_edges[0], bin_edges[len(bin_edges)-1]),bins=len(bin_edges))
            color = sset.style.color
            trace = {
                'type': "bar", 'name': sset.label,
                'marker' : {'color': color},
                'x': xedges,
                'y': hist,
            }
            traces.append(trace)

        layout = {
            'title' : self.options['title'].value,
            'margin' : {'l':50,'r':0,'b':50,'t':30 },
            'xaxis': { 'autorange' : True, 'zeroline': True, 'title' : self.options['xaxis'].value, },
            'yaxis': { 'autorange':True, 'zeroline': True, 'title' : self.options['yaxis'].value, },
            'showlegend': True,
            'barmode': 'overlay',
        }
        return FigureWidget({
                'data': traces,
                'layout': layout
        })
        
    def updateRender(self):
        self.plotly_fig = self.createFigureWidget()
        GluePlotly.display(self)

    def updateSelection(self, ids):
        pass
		