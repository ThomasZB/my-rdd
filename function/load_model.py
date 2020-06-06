import tensorflow as tf


def wrap_frozen_graph(graph_def, inputs, outputs):
  def _imports_graph_def():  
    tf.compat.v1.import_graph_def(graph_def, name="")
  wrapped_import = tf.compat.v1.wrap_function(_imports_graph_def, [])
  import_graph = wrapped_import.graph
  return wrapped_import.prune(
      tf.nest.map_structure(import_graph.as_graph_element, inputs),
      tf.nest.map_structure(import_graph.as_graph_element, outputs))

def load_tf1_model:
  graph_def = tf.compat.v1.GraphDef()
  loaded = graph_def.ParseFromString(open('frozen_inference_graph_mobilenet.pb','rb').read())
  mobile_func = wrap_frozen_graph(graph_def, inputs='image_tensor:0', outputs=('detection_boxes:0', 'detection_scores:0','detection_classes:0', 'num_detections:0'))