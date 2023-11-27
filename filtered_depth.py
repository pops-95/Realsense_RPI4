## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt 
import cv2
import threading

global pipe
global processed_frame
global stop
global point

    # Define a callback function for mouse events
def mouse_callback(event, x, y, flags, param):
     if event == cv2.EVENT_LBUTTONDOWN:
        # Get the depth frame
        global point
        point=(x,y)
        print(point)
        return point

# Create a window and set the mouse callback function
cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE)



stop=False
color_map=rs.colorizer()
dec=rs.decimation_filter()
dec.set_option(rs.option.filter_magnitude,2)
depth2disparity=rs.disparity_transform()
disparity2depth=rs.disparity_transform(False)
spat=rs.spatial_filter()
spat.set_option(rs.option.holes_fill,5)
temp=rs.temporal_filter()
align_to=rs.align(rs.stream.color)


def post_processing_thread(lock):
    global pipe
    while(not stop):
        
        data=pipe.poll_for_frames()
        if(data):
            data=align_to.process(data)
            # print("ok")
            # data=data.get_depth_frame()
            data.as_frameset()
            # print(data.get_height())
            lock.acquire()
            data=depth2disparity.process(data)
            data=spat.process(data)
            data=temp.process(data)
            data=disparity2depth.process(data)
            processed_frame.enqueue(data)
            lock.release()

if __name__=="__main__":
    point=(400,200)
    pipe=rs.pipeline()
    cfg=rs.config()
    lock=threading.Lock()
    
    cfg.enable_stream(rs.stream.depth, 1280,720, rs.format.z16, 6)
    cfg.enable_stream(rs.stream.color, 1280,720, rs.format.bgr8, 30)
    
    profile=pipe.start(cfg)
    sensor=profile.get_device().first_depth_sensor()
    sensor.set_option(rs.option.visual_preset,4)
    
    stream=profile.get_stream(rs.stream.depth).as_video_stream_profile()
    
    processed_frame=rs.frame_queue()
    threading.Thread(target=post_processing_thread,args=(lock,)).start()
    while(True):
        # cv2.setMouseCallback("Color Stream", mouse_callback)
        # print("Inside main")
        cv2.setMouseCallback("Frame",mouse_callback)
        current_frameset=processed_frame.poll_for_frame().as_frameset()
        if(current_frameset.is_frameset()):
            depth=current_frameset.get_depth_frame()
            color=current_frameset.get_color_frame()
            depth_value = depth.get_distance(point[0],point[1])
            color_image = np.asanyarray(color.get_data())
            cv2.putText(color_image,"{:.3f}m".format(depth_value),(point[0],point[1]-20),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
            cv2.imshow("Frame",color_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop=True
            pipe.stop()
            break
    
    
    
    