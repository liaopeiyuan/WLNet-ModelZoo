import re

import caffe2.proto.caffe2_pb2 as caffe
import numpy as npy
import wolframclient.serializers as wxf


def layer_iter(layers):
    '''add layer name when confused'''
    for layer in layers:
        layer_name = re.sub('[-/]', '_', layer.name)
        layer_type = layer.type
        layer_blobs = layer.blobs
        yield (layer_name, layer_type, layer_blobs)


def caffe2wxf(path):
    data = dict()
    model = caffe.NetParameter()
    model.ParseFromString(open(path, 'rb').read())

    get_array = lambda p: npy.array(p.data, dtype='float32').reshape(p.shape.dim)

    def add_array(node):
        for i in range(len(node.blobs)):
            data[node.name + "_" + str(i + 1)] = get_array(node.blobs[i])

    def add_node(layers):
        for i in range(len(layers)):
            add_array(layers[i])

    add_node(model.layer)
    wxf.export(data, path + '.wxf', target_format='wxf')
