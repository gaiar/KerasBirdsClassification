import os
import io
import time
import random
from io import StringIO
from collections import defaultdict

import numpy as np
import urllib.request
import six.moves.urllib as urllib
import tensorflow as tf
from PIL import Image

### Place your telegram-bot key here ###
BOT_KEY = "129517685:AAF78SRwWNdaL8XY0z3tDSIKLqcxV6N8eIw"

### Expand it to add more cameras
CAMS = (
  ('http://77.47.7.50:8789/record/current.jpg', 'Bärencam: Blick auf den Bärenberg '),
  ('http://77.47.7.50:8788/record/current.jpg', 'Bärencam: Blick auf den Bärensee '),
  ('http://77.47.7.50:8790/record/current.jpg', 'Bärencam: Bärenbox von Fred &amp; Frode '),
  ('http://77.47.7.50:8791/record/current.jpg', 'Wildkatzencam: Futterplatz der Wildkatzen '),
  ('http://77.47.7.50:8792/record/current.jpg', 'Luchscam: Wo schlafen die Luchse? '),
  ('http://77.47.7.50:8793/record/current.jpg', 'Wolfscam: Fichtenschonung im Wolfsareal'),
  ('http://77.47.7.50:8794/record/current.jpg', 'Wolfscam: Wolfspfad '),
# ('http://77.47.7.50:8795/record/current.jpg', 'Aquacam: Aquatunnel '),
# ('http://77.47.7.50:8796/record/current.jpg', 'Aquacam: Natur-Aquarium '),
  ('http://77.47.7.50:8797/record/current.jpg', 'Luchscam: Futterplatz '),
  ('http://77.47.7.50:8798/record/current.jpg', 'Wolfscam: Futterplatz'),
)

# Heuristic parameters
USE_TH = .35
BAD_TAGS = ('bed','bench','bicycle','couch','fire hydrant','microwave','refrigerator',
  'suitcase','train','tv','wine glass', 'sports ball', 'boat', 'person', 'teddy bear', 
  'kite', 'cup', 'umbrella', 'handbag', 'elephant', 'traffic light', 'bird', 'car', 
  'backpack', 'parking meter', 'surfboard')

### (+) this part is taken from TF tutorial ####
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'
# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in ['num_detections', 'detection_boxes', 'detection_scores', 'detection_classes', 'detection_masks']:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
      # Run inference
      output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image, 0)})
      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict
### (-) this part is taken from TF tutorial ####

# run the object detection process, thenpostprocess and clean the output
def process_img(image,TH=0.5,MAXSIZE=0.15, MAXLINSIZE=0.4):
  image_np = load_image_into_numpy_array(image)
  image_np_expanded = np.expand_dims(image_np, axis=0)
  # Actual detection.
  output_dict = run_inference_for_single_image(image_np, detection_graph)
  tags = []
  for cl,score,box in zip(output_dict['detection_classes'],output_dict['detection_scores'],output_dict['detection_boxes']):
    if score>=TH and (box[2]-box[0])*(box[3]-box[1])<=MAXSIZE and (box[2]-box[0])<=MAXLINSIZE and (box[3]-box[1])<=MAXLINSIZE:
      print(score,category_index[cl]['name'],box,(box[2]-box[0])*(box[3]-box[1]))
      tags.append(category_index[cl]['name'])
  vis_util.visualize_boxes_and_labels_on_image_array(
      image_np,
      output_dict['detection_boxes'],
      output_dict['detection_classes'],
      output_dict['detection_scores'],
      category_index,
      instance_masks=output_dict.get('detection_masks'),
      use_normalized_coordinates=True,
      min_score_thresh=TH,
      line_thickness=8)
  return tags,image_np

# prepare telegram bot
updater = Updater(BOT_KEY)

while True: 
  print('\nanother check')
  for cam in CAMS:
    for attempt in range(3): # on network error retry 3 times 
      try:
        # get a camera image and process it to tags and a labeled image
        #response = urllib.request.urlopen(cam[0])
        response = urllib.request.urlopen("https://www.berlin.de/ba-charlottenburg-wilmersdorf/verwaltung/aemter/umwelt-und-naturschutzamt/naturschutz/pflanzen-artenschutz/mdb-blesshuhn_philip_mackenzie_717748.jpg")
        data = response.read()  
        image = Image.open(io.BytesIO(data))
        tags, pic = process_img(image,TH=USE_TH)
        break
      except:
        print('img grab error, retry\n\t'+cam[0])
        time.sleep(60)
    # remove false and not interesting tags
    tags = list(set(tags)-set(BAD_TAGS))
    if tags: # something interesting found
      print("detected:\n",cam[1], tags)
      # process the image to binary format before sending
      pic_out = io.BytesIO()
      pic_out.name = 'image.jpeg'
      img = Image.fromarray(pic)
      img.save(pic_out, 'JPEG')
      pic_out.seek(0)
      print('sending...')
      for attempt in range(5): # on telegram network api error retry 5 times
        try:
          updater.bot.send_photo("@BirdsOfBerlin", photo=pic_out, 
              caption="Detected: %s at [%s](%s)" % (str(tags), cam[1], cam[0]), 
              parse_mode='Markdown')
          print('sent')
          break
        except:
          print('tg connection error, retry')
          time.sleep(30)
  print('check completed')
  time.sleep(60*5)