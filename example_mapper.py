import mapper
import numpy as np
import matplotlib.pyplot as plt

'''
    Step 1: Input
'''
import gzip
filename = 'YOUR FILE.csv'
with open(filename, 'r') as inputfile:
    data = np.loadtxt(inputfile, delimiter=',', dtype=np.float)
    # or pandas with (pd.read_csv, etc))
    
# Preprocessing
'''
point_labels = None
mask = None
Gauss_density = mapper.filters.Gauss_density
kNN_distance  = mapper.filters.kNN_distance
crop = mapper.crop
# Custom preprocessing code

# End custom preprocessing code
data, point_labels = mapper.mask_data(data, mask, point_labels)
'''
'''
    Step 2: Metric
'''
intrinsic_metric = False
if intrinsic_metric:
    is_vector_data = data.ndim != 1
    if is_vector_data:
        metric = Euclidean
        if metric != 'Euclidean':
            raise ValueError('Not implemented')
    data = mapper.metric.intrinsic_metric(data, k=1, eps=1.0)
is_vector_data = data.ndim != 1
'''
    Step 3: Filter function
'''
if is_vector_data:
    metricpar = {'metric': 'euclidean'}
    f = mapper.filters.eccentricity(data,
        metricpar=metricpar,
        exponent=1.0)
else:
    f = mapper.filters.eccentricity(data,
        exponent=1.0)
# Filter transformation
'''
mask = None
crop = mapper.crop
# Custom filter transformation

# End custom filter transformation
'''
'''
    Step 4: Mapper parameters
'''
cover = mapper.cover.cube_cover_primitive(intervals=15, overlap=50.0)
cluster = mapper.single_linkage()
if not is_vector_data:
    metricpar = {}
mapper_output = mapper.mapper(data, f,
    cover=cover,
    cluster=cluster,
    point_labels=point_labels,
    cutoff=None,
    metricpar=metricpar)
cutoff = mapper.cutoff.first_gap(gap=0.1)
mapper_output.cutoff(cutoff, f, cover=cover, simple=False)
mapper_output.draw_scale_graph()
plt.savefig('scale_graph.pdf')
'''
    Step 5: Display parameters
'''
# Node coloring
'''
nodes = mapper_output.nodes
node_color = None
point_color = None
name = 'custom scheme'
# Custom node coloring

# End custom node coloring
node_color = mapper_output.postprocess_node_color(node_color, point_color, point_labels)
minsizes = []
mapper_output.draw_2D(minsizes=minsizes,
    node_color=node_color,
    node_color_scheme=name)
plt.savefig('mapper_output.pdf')
plt.show()
'''
