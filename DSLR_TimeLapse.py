#Jose Marquez Doblas
#Canon EOS 1200D TimeLapse

import gphoto2 as gp
import os
import subprocess
import time


#Configuration (READONLY)
N_PHOTOS = 10
LAPSE = 15
CAMERA_DELAY = 3 #Canon EOS 1200D delay
IMG_PATH = ""
VID_PATH = ""


def configured_camera():
    #Getting the camera
    context = gp.Context()
    cam = gp.Camera()
    cam.init(context)

    print cam.get_summary(context)
    return cam

def take_photos():
    cam = configured_camera()
    for n in range(N_PHOTOS):
        file_path = gp.check_result(gp.gp_camera_capture(cam, gp.GP_CAPTURE_IMAGE))
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join(IMG_PATH, file_path.name)
        print('Copying image to', target)
        camera_file = gp.check_result(gp.gp_camera_file_get(cam, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, target))
        time.sleep(LAPSE-CAMERA_DELAY)
        
    gp.check_result(gp.gp_camera_exit(cam))


def create_video():
    subprocess.call("ffmpeg -r 24 -pattern_type glob -i '*.jpg' -i /home/pepe/prueba/capt%04d.jpg -s hd1080 -vcodec libx264 timelapse.mp4")


if __name__ == "__main__":
    take_photos()
    create_video()