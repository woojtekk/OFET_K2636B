import cv
import opencv.highgui
import time

def get_image():
    image = opencv.highgui.cvQueryFrame(camera)
    
    return opencv.adaptors.Ipl2PIL(image)

camera = opencv.highgui.cvCreateCameraCapture(-1)

while 1:
    image = get_image()
    image.thumbnail((32, 24, ))
    image = tuple(ord(i) for i in image.tostring())
    x = int((int((max(image) / 256.0) * 10) + 1) ** 0.5 / 3 * 10)
    print(x)
    # cmd = ("sudo su -c 'echo " + str(x) +
    #     " > /sys/devices/virtual/backlight/acpi_video0/brightness'")
    # status, output = commands.getstatusoutput(cmd)
    # assert status is 0
    