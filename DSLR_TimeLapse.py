# Jose Marquez Doblas
# Canon EOS 1200D TimeLapse

import gphoto2 as gp
import os
import time
import cv2

# Configuration
N_PHOTOS = 3
LAPSE = 1
CAMERA_DELAY = 0  # Canon EOS 1200D delay
IMG_PATH = "/home/pepe/Escritorio"
VID_PATH = "/home/pepe/Escritorio/video.avi"


def configured_camera():
    # Getting the camera
    context = gp.Context()
    cam = gp.Camera()
    cam.init(context)

    print(cam.get_summary(context))
    return cam


def take_photos():
    cam = configured_camera()
    for n in range(N_PHOTOS):
        file_path = gp.check_result(gp.gp_camera_capture(cam,
                                                         gp.GP_CAPTURE_IMAGE))

        print('Camera file path: {0}/{1}'.format(file_path.folder,
                                                 file_path.name))

        target = os.path.join(IMG_PATH, file_path.name)
        print('Copying image to', target)

        camera_file = gp.check_result(gp.gp_camera_file_get(cam,
                                      file_path.folder,
                                      file_path.name,
                                      gp.GP_FILE_TYPE_NORMAL))

        gp.check_result(gp.gp_file_save(camera_file, target))
        time.sleep(lapse_time())

    gp.check_result(gp.gp_camera_exit(cam))


def create_video():
    images = [img for img in os.listdir(IMG_PATH) if img.endswith(".jpg")]
    frame = cv2.imread(os.path.join(IMG_PATH, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(VID_PATH, 0, 24, (width, height))

    print "Creating the video"
    for image in images:
        video.write(cv2.imread(os.path.join(IMG_PATH, image)))

    cv2.destroyAllWindows()
    video.release()
    print "Video Created"


# Calculate the time between photos taking into account the camera delay
def lapse_time():
    time = 0
    if LAPSE > CAMERA_DELAY:
        time = LAPSE - CAMERA_DELAY

    return time


if __name__ == "__main__":
    take_photos()
    create_video()
