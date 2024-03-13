#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace rs2;
using namespace cv;
using namespace std;

int main(int argc , char *argv[]){
    namedWindow("Capture",WINDOW_AUTOSIZE);
    pipeline pipe;
    config cfg;

    cfg.enable_stream(RS2_STREAM_COLOR);
    pipe.start(cfg);

     while (waitKey(1) < 0 )
    {
        frameset data = pipe.wait_for_frames(); // Wait for next set of frames from the camera
        frame depth = data.get_color_frame();

        // Query frame size (width and height)
        const int w = depth.as<rs2::video_frame>().get_width();
        const int h = depth.as<rs2::video_frame>().get_height();

        // Create OpenCV matrix of size (w,h) from the colorized depth data
        Mat image(Size(w, h), CV_8UC3, (void*)depth.get_data(), Mat::AUTO_STEP);

        // Update the window with new data
        imshow("Capture", image);
    }

    return 0;
}





