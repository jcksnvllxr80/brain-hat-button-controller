import yaml
import requests
import subprocess
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [CameraButtons] [%(levelname)-5.5s]  %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

tf_obj_recognition_pid_str = "ps aux | grep -ivE \"(grep|venv)\" | grep pitft_labeled_output.py | awk \'{print $2}\'"
stream_preview_pid_str = "ps aux | grep -ivE \"(grep)\" | grep ncat | awk \'{print $2}\'"
HOME_DIR = "/home/pi/brain-hat-button-controller/"
CONFIG_FILE = HOME_DIR + "conf/application.yaml"

class CameraButtons(object):

  def __init__(self):
    self.mode = 'default'
    self.camera_func = 'none'
    self.camera_funcs = ['menu', 'capture', 'video', 'stopmotion', 'timelapse']
    self.default_func = 'none'
    self.default_funcs = ['none', 'preview_stream']
    self.pi_cam_app_settings = {}
    self.stream_settings = {}
    subprocess.Popen(HOME_DIR + "pi_cam_app")
    self.config()

  def config(self):
    config_file = self.read_config_file()
    self.pi_cam_app_settings = {k: v for k, v in config_file['pi_cam_app'].items()}
    self.stream_settings = {k: v for k, v in config_file['stream'].items()}

  def read_config_file(self):
    config_file = None
    with open(CONFIG_FILE, 'r') as ymlfile:
      config_file = yaml.full_load(ymlfile)
    return config_file

  def change_mode(self, new_mode='default'):
    self.mode = new_mode
    if self.mode == 'default':
      self.change_camera_func('none')
    logger.info("Mode changed to {0}".format(self.mode))

  def change_camera_func(self, new_camera_func='capture'):
    self.camera_func = new_camera_func
    logger.info("Camera function changed to {0}".format(self.camera_func))

  def change_default_func(self, new_default_func='none'):
    self.default_func = new_default_func
    logger.info("Default function changed to {0}".format(self.default_func))

  def start_tf_obj_recognition(self):
    # NOTE: in order to get the speaker to work on the brainCraft hat, the following line
    # pipes the detected text into sudo festival in line 150 of the link below.
    # the reason the speaker stuff doesnt just work is that i am nott running the code as root.
    # https://github.com/adafruit/rpi-vision/blob/master/tests/pitft_labeled_output.py
    #######################################################################
    # os.system('echo %s | sudo festival --tts & ' % detecttext)  # this is the changed line
    #######################################################################
    if self.pi_cam_is_previewing():
      self.pi_cam_preview('stop')
      self.change_mode()
    os.environ["DISPLAY"] = ":0"
    subprocess.Popen("{0}tf_obj_recognition".format(HOME_DIR))

  def pi_cam_preview(self, action):
    self.make_get_api_call("http://127.0.0.1:{0}/pi_cam_preview/{1}".format(self.pi_cam_app_settings['port'], action))

  def pi_cam_is_previewing(self):
    api_call_str = "http://127.0.0.1:{0}/is_previewing".format(self.pi_cam_app_settings['port'])
    logger.info("Making a GET call to \'{0}\'".format(api_call_str))
    response = requests.get(api_call_str).content.decode("utf-8")
    logger.info("Camera is previewing: {0}".format(response))
    return True if response == 'True' else False

  def up(self):
    long_press = False
    self.up_handler(long_press)

  def long_up(self):
    long_press = True
    self.up_handler(long_press)

  def down(self):
    long_press = False
    self.down_handler(long_press)

  def long_down(self):
    long_press = True
    self.down_handler(long_press)

  def left(self):
    long_press = False
    self.left_handler(long_press)

  def long_left(self):
    long_press = True
    self.left_handler(long_press)

  def right(self):
    long_press = False
    self.right_handler(long_press)

  def long_right(self):
    long_press = True
    self.right_handler(long_press)

  def photo_bttn(self):
    long_press = False
    self.photo_handler(long_press)

  def long_photo_bttn(self):
    long_press = True
    self.photo_handler(long_press)

  def select(self):
    long_press = False
    self.select_handler(long_press)

  def long_select(self):
    long_press = True
    self.select_handler(long_press)

  def up_handler(self, was_long_press):
    if self.mode == 'camera':
      self.short_or_long_press_func(was_long_press, self.cam_mode_up, CameraButtons.shutdown)
    else:
      self.short_or_long_press_func(was_long_press, self.pass_func, CameraButtons.shutdown)

  def down_handler(self, was_long_press):
    if self.mode == 'camera':
      self.short_or_long_press_func(was_long_press, self.cam_mode_down, self.pi_cam_app)
    else:
      self.short_or_long_press_func(was_long_press, self.pass_func, self.pi_cam_app)

  def left_handler(self, was_long_press):
    if self.mode == 'camera':
      self.short_or_long_press_func(was_long_press, self.left_value, self.left_cam_func)
    else:
      self.short_or_long_press_func(was_long_press, self.pass_func, self.left_default_func)

  def right_handler(self, was_long_press):
    if self.mode == 'camera':
      self.short_or_long_press_func(was_long_press, self.right_value, self.right_cam_func)
    else:
      self.short_or_long_press_func(was_long_press, self.pass_func, self.right_default_func)

  def select_handler(self, was_long_press):
    self.short_or_long_press_func(was_long_press, self.select_func, CameraButtons.reboot)

  def photo_handler(self, was_long_press):
    if self.mode == 'camera':
      self.short_or_long_press_func(was_long_press, self.photo, self.obj_recognition)
    else:
      self.short_or_long_press_func(was_long_press, self.pass_func, self.obj_recognition)

  def photo(self):
    if self.camera_func in ["capture", 'menu']:
      logger.info("Taking photo")
      self.make_get_api_call("http://127.0.0.1:{0}/take_photo/{1}".format(self.pi_cam_app_settings['port'], self.create_new_unique_filename()))
    elif self.camera_func == 'video':
      logger.info("recording video")
      self.make_get_api_call("http://127.0.0.1:{0}/record_video/{1}_vid".format(self.pi_cam_app_settings['port'], self.create_new_unique_filename()))
    elif self.camera_func == 'stopmotion':
      logger.info("Adding stopmotion frame")
      self.make_get_api_call("http://127.0.0.1:{0}/stopmotion/add_frame".format(self.pi_cam_app_settings['port']))
    elif self.camera_func == 'timelapse':
      logger.info("recording timelapse")
      self.make_get_api_call("http://127.0.0.1:{0}/record_timelapse/{1}_timelapse".format(self.pi_cam_app_settings['port'], self.create_new_unique_filename()))
    else:
      self.pass_func()

  def end_stopmotion_scene(self):
    logger.info("Ending stopmotion scene")
    self.make_get_api_call("http://127.0.0.1:{0}/stopmotion/end/{1}_stopmotion".format(self.pi_cam_app_settings['port'], self.create_new_unique_filename()))

  def create_new_unique_filename(self):
    return "{0}".format(datetime.now().strftime("%Y%m%d_%H%M%S"))

  def obj_recognition(self):
    self.kill_pid_or_start_func(tf_obj_recognition_pid_str, self.start_tf_obj_recognition)

  def pi_cam_app(self):
    self.start_or_stop_pi_cam_preview()

  def cam_mode_up(self):
    if self.camera_func == 'menu':
      self.next_menu_item('up')
    else:
      self.cam_zoom('in')

  def cam_mode_down(self):
    if self.camera_func == 'menu':
      self.next_menu_item('down')
    else:
      self.cam_zoom('out')

  def next_menu_item(self, dir):
    self.make_get_api_call("http://127.0.0.1:{0}/next_menu_item/{1}".format(self.pi_cam_app_settings['port'], dir))

  def cam_zoom(self, dir):
    self.make_get_api_call("http://127.0.0.1:{0}/zoom/{1}".format(self.pi_cam_app_settings['port'], dir))

  def left_value(self):
    self.next_value('left')

  def right_value(self):
    self.next_value('right')

  def next_value(self,dir):
    if self.camera_func == 'menu':
      self.make_get_api_call("http://127.0.0.1:{0}/next_value/{1}".format(self.pi_cam_app_settings['port'], dir))
    else:
      self.pass_func()

  def left_cam_func(self):
    self.next_cam_function('left')

  def right_cam_func(self):
    self.next_cam_function('right')

  def next_cam_function(self, dir):
    current_cam_func_ind = self.camera_funcs.index(self.camera_func)
    if dir == 'left':
      if current_cam_func_ind == 0:
        next_cam_func = self.camera_funcs[len(self.camera_funcs) - 1]
      else:
        next_cam_func = self.camera_funcs[current_cam_func_ind - 1]
    else:
      if current_cam_func_ind == len(self.camera_funcs) - 1:
        next_cam_func = self.camera_funcs[0]
      else:
        next_cam_func = self.camera_funcs[current_cam_func_ind + 1]
    self.change_camera_func(next_cam_func)
    self.make_get_api_call("http://127.0.0.1:{0}/display_and_speak/Function/{1}".format(self.pi_cam_app_settings['port'], next_cam_func))

  def left_default_func(self):
    self.next_default_function('left')

  def right_default_func(self):
    self.next_default_function('right')

  def next_default_function(self, dir):
    current_default_func_ind = self.default_funcs.index(self.default_func)
    if dir == 'left':
      if current_default_func_ind == 0:
        next_default_func = self.default_funcs[len(self.default_funcs) - 1]
      else:
        next_default_func = self.default_funcs[current_default_func_ind - 1]
    else:
      if current_default_func_ind == len(self.default_funcs) - 1:
        next_default_func = self.default_funcs[0]
      else:
        next_default_func = self.default_funcs[current_default_func_ind + 1]
    self.change_default_func(next_default_func)
    self.execute_default_func(next_default_func)

  @staticmethod
  def make_get_api_call(api_call_str):
    logger.info("Making a GET call to \'{0}\'".format(api_call_str))
    response = requests.get(api_call_str)
    logger.info("Response from api call: {0}".format(response.content.decode("utf-8")))

  @staticmethod
  def get_pid(get_pid_cmd_str):
    return subprocess.check_output([get_pid_cmd_str], shell=True).decode().rstrip()

  @staticmethod
  def kill_pid(pid):
    os.system("kill -9 " + str(pid))

  def kill_pid_or_start_func(self, get_pid_str, func):
    pid = CameraButtons.get_pid(get_pid_str)
    if pid:
      CameraButtons.kill_pid(pid)
      self.change_mode()
    else:
      func()

  def start_or_stop_pi_cam_preview(self):
    if self.pi_cam_is_previewing():
      self.pi_cam_preview('stop')
      self.change_mode()
    else:
      pid = CameraButtons.get_pid(tf_obj_recognition_pid_str)
      if pid:
        CameraButtons.kill_pid(pid)
      self.change_mode('camera')
      self.change_camera_func()
      self.pi_cam_preview('start')

  @staticmethod
  def reboot():
    os.system("sudo reboot now")

  @staticmethod
  def shutdown():
    os.system("sudo shutdown -h now")

  def pass_func(self):
    logger.warning("This function has not been implemented for mode: \'{0}\',  camera function: \'{1}\'".format(self.mode, self.camera_func))

  def select_func(self):
    if self.camera_func:
      camera_funcs_with_select_feature = {
          'stopmotion': self.end_stopmotion_scene,
      }
      camera_funcs_with_select_feature.get(self.camera_func, self.pass_func)()

  def start_preview_stream(self):
    os.system("raspivid -n -ih -t 0 -rot 0 -w {0} -h {1} -fps {2} -b {3} -o - | ncat -lkv4 {4} &".format(
      self.stream_settings['width'], self.stream_settings['height'], self.stream_settings['fps'], self.stream_settings['bits'], self.stream_settings['port']))

  @staticmethod
  def stop_preview_stream():
    pid = CameraButtons.get_pid(stream_preview_pid_str)
    if pid:
      CameraButtons.kill_pid(pid)

  def execute_default_func(self, func):
    self.stop_preview_stream()
    if func == 'preview_stream':
      self.pi_cam_preview('stop')
      self.start_preview_stream()