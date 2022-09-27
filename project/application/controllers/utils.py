import base64
import io
import matplotlib
import pandas as pd

matplotlib.use('AGG')
from matplotlib import pyplot as plt

plt.ioff()
plt.tight_layout()

from flask import request
from application.errors import RedirectError

def create_redirect_error(error_str):
  return base64.b64encode(bytes(error_str, "utf-8")).decode("utf-8")

def get_redirect_error():
  encoded_redirect_error = request.args.get('redirect_error', "").strip()
  if encoded_redirect_error != "":
    try:
      decored_redirect_error = base64.b64decode(encoded_redirect_error).decode("utf-8")
      return RedirectError(decored_redirect_error)
    except:
      return None

  return None

def flatten_from_errors(form_errors):
  errors = []
  for k in form_errors:
    errors.extend(form_errors[k])

  return errors

def plot_timeline(timeline, size=(5,6), rotation=60):
  frame = {
      'total': [slice['total'] for slice in timeline],
      'missed': [slice['missed'] for slice in timeline],
      'completed': [slice['completed'] for slice in timeline],
  }

  index = [slice['time'] for slice in timeline]

  df = pd.DataFrame(frame, index=index)

  plot = df.plot(figsize=size)
  fig = plot.get_figure()
  fig.autofmt_xdate(rotation=rotation)

  pic_IObytes = io.BytesIO()
  fig.savefig(pic_IObytes, format='png')
  pic_hash = base64.b64encode(pic_IObytes.getvalue()).decode("utf-8").replace("\n", "")

  plt.close(fig=fig)
  return pic_hash
