import mxnet as mx
from mxnet.gluon.model_zoo import vision
import gluoncv as gcv
from gluoncv.model_zoo import get_model
from gluoncv.data import VOCDetection
import json
import time
from gluoncv.utils import viz           # gluoncv specific visualization capabilities
from gluoncv.utils import export_block
from matplotlib import pyplot as plt
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageEnhance
import io
import os
import numpy as np


threshold = 0.69

# don't touch!!! used to convert sagemaker's integer classes back to card values.
class_map = {"AC": 0, "2C": 1, "3C": 2, "4C": 3, "5C": 4, "6C": 5, "7C": 6, "8C": 7, "9C": 8, "10C": 9, "JC": 10, "QC": 11, "KC": 12, "AD": 13, "2D": 14, "3D": 15, "4D": 16, "5D": 17, "6D": 18, "7D": 19, "8D": 20, "9D": 21, "10D": 22, "JD":23, "QD": 24, "KD": 25, "AH": 26, "2H": 27, "3H": 28, "4H": 29, "5H": 30, "6H": 31, "7H": 32, "8H": 33, "9H": 34, "10H": 35, "JH": 36, "QH": 37, "KH": 38, "AS": 39, "2S": 40, "3S": 41, "4S": 42, "5S": 43, "6S": 44, "7S": 45, "8S": 46, "9S": 47, "10S": 48, "JS": 49, "QS": 50, "KS": 51}

object_categories = list(class_map.keys())
klasses = ["ac", "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "jc", "qc", "kc", "ad", "2d", "3d", "4d", "5d",
           "6d", "7d", "8d", "9d", "10d", "jd", "qd", "kd", "ah", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h",
           "jh", "qh", "kh", "as", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "js", "qs", "ks"]

num_classes = [str(x) for x in range(len(klasses)+1)]



class VOCLike(VOCDetection):
    CLASSES = ["ac", "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "jc", "qc", "kc", "ad", "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "jd", "qd", "kd", "ah", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "jh", "qh", "kh", "as", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "js", "qs", "ks"]
    def __init__(self, root, splits, transform=None, index_map=None, preload_label=True):
        super(VOCLike, self).__init__(root, splits, transform, index_map, preload_label)

def model_fn():
    """
    Load the gluon model. Called once when hosting service starts.

    :param: model_dir The directory where model files are stored.
    :return: a model (in this case a Gluon network)
    """
    net = get_model("yolo3_mobilenet1.0_custom", classes = num_classes, ctx=mx.gpu(0))
    net.load_parameters('model/yobile-0000.params', ctx=mx.gpu(0))
    net.collect_params().reset_ctx(mx.gpu(0))

    return net

def transform_fn(net, observation):
    """
    Transform a request using the Gluon model. Called once per request.

    :param net: The Gluon model.
    :param output_content_type: The (desired) response content type.
    :return: response payload and content type.
    """
    x, image = gcv.data.transforms.presets.yolo.load_test(observation, 608)
    cid, score, bbox = net(x.as_in_context(mx.gpu(0)))
    cid_list = cid[0].asnumpy().tolist()
    score_list = score[0].asnumpy().tolist()
    bbox_list = bbox[0].asnumpy().tolist()

    response = {'prediction': []}

    for x in cid_list:
        response['prediction'].append(x)
    for idx, val in enumerate(score_list):
        response['prediction'][idx].append(val[0])
    for idx, val in enumerate(bbox_list):
        for x in val:
            response['prediction'][idx].append(x)

    response_body = json.dumps(response)
    return response_body

def visualize(index, img, dets, classes=[], thresh=0.6):
    class_map = {"AC": 0, "2C": 1, "3C": 2, "4C": 3, "5C": 4, "6C": 5, "7C": 6, "8C": 7, "9C": 8, "10C": 9, "JC": 10,
                 "QC": 11, "KC": 12, "AD": 13, "2D": 14, "3D": 15, "4D": 16, "5D": 17, "6D": 18, "7D": 19, "8D": 20,
                 "9D": 21, "10D": 22, "JD": 23, "QD": 24, "KD": 25, "AH": 26, "2H": 27, "3H": 28, "4H": 29, "5H": 30,
                 "6H": 31, "7H": 32, "8H": 33, "9H": 34, "10H": 35, "JH": 36, "QH": 37, "KH": 38, "AS": 39, "2S": 40,
                 "3S": 41, "4S": 42, "5S": 43, "6S": 44, "7S": 45, "8S": 46, "9S": 47, "10S": 48, "JS": 49, "QS": 50,
                 "KS": 51}

    object_categories = list(class_map.keys())
    f = io.BytesIO()
    plt.clf()
    # img=mpimg.imread(img_file, 'jpg')
    plt.imshow(img)
    # height = img.shape[0]
    # width = img.shape[1]
    colors = dict()
    for det in dets:
        (klass, score, x0, y0, x1, y1) = det
        if score < thresh:
            continue
        cls_id = int(klass)
        if cls_id not in colors:
            colors[cls_id] = (random.random(), random.random(), random.random())
        xmin = int(x0)
        ymin = int(y0)
        xmax = int(x1)
        ymax = int(y1)
        rect = plt.Rectangle((xmin, ymin), xmax - xmin,
                             ymax - ymin, fill=False,
                             edgecolor=colors[cls_id],
                             linewidth=3.5)
        plt.gca().add_patch(rect)
        class_name = str(cls_id)
        if classes and len(classes) > cls_id:
            class_name = classes[cls_id]
        plt.gca().text(xmin, ymin - 2,
                       '{:s} {:.3f}'.format(class_name, score),
                       bbox=dict(facecolor=colors[cls_id], alpha=0.5),
                       fontsize=12, color='white')
    ax = plt.gca()
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    fig1 = plt.gcf()
    fig1.set_size_inches(4, 4)
    fig1.savefig("results/results" + str(index) + ".png", format='png', bbox_inches='tight', transparent=True, pad_inches=0, dpi=100)
    #f.seek(0)
    #f.write("results.png")


def create_symbols():
    '''
    my_net = get_model('yolo3_mobilenet1.0_custom', classes=num_classes)
    my_net.load_parameters('model/yobile-0000.params')

    # Convert the model to symbolic format
    my_net.hybridize()

    # Build a fake image to run a single prediction
    # This is required to initialize the model properly
    x = np.zeros([1, 3, 608, 608])
    x = mx.nd.array(x)

    # Predict the fake image
    my_net.forward(x)

    # Export the model
    my_net.export('yobile')


    # gluoncv.model_zoo.get_model()
    net = get_model("yolo3_mobilenet1.0_custom", classes=num_classes, ctx=mx.gpu(0))
    net.load_parameters('model/yolo3_mobilenet1.0_custom_best.params', ctx=mx.gpu(0))
    net.collect_params().reset_ctx(mx.gpu(0))
    #net.save_checkpoint('yolo3_mobilenet1.0',0000)
    #export_block('yolo3_mobilenet1.0', net)
     '''
    # mxnet.gluon.model_zoo.get_model()
    # mnet = vision.get_mobilenet(1,pretrained=False,ctx=mx.gpu(0), root="model") #<-- works but no weights
    #mnet = vision.get_model("mobilenet1.0", pretrained=False, classes=num_classes, ctx=mx.gpu(0), root="model")
    #mx.model.load_checkpoint("model/yobile", 0, ctx=mx.gpu(0))

    #mnet.hybridize()
    #mnet.initialize()
    #mnet.forward(mx.nd.ones((1, 3, 608, 608)))
    #mnet.export("yobile-x")


def infer():
    net = model_fn()
    index = 0
    for r, d, f in os.walk("observations"):
        for file in f:
            #print("file: {}".format(file))

            img = 'observations/' + file
            start = time.time()
            response = transform_fn(net, img)
            end = time.time()
            print("inference duration: {}".format(end-start))
            j = json.loads(response)
            print(j['prediction'])
            pil_img = Image.open(img)
            pil_img = pil_img.resize((608,608), Image.BILINEAR)
            new_img_bytes = io.BytesIO()
            pil_img.save(new_img_bytes, 'JPEG')
            img_file=mpimg.imread(new_img_bytes, 'jpg')

            visualize(index, img=img_file, dets=j['prediction'],classes=object_categories, thresh=threshold)
            index += 1


infer()
#create_symbols()