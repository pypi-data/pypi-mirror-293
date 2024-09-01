import argparse
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from ourcustompkg.yolov7.utils.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages, LoadWebcam
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel

### Hand Module ###
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np

import logging
from datetime import datetime

BaseOptions = python.BaseOptions
HandLandmarker = vision.HandLandmarker
HandLandmarkerOptions = vision.HandLandmarkerOptions
HandLandmarkerResult = vision.HandLandmarkerResult
VisionRunningMode = vision.RunningMode

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

class HandLModule():
    def __init__(self):
        self.MARGIN = 10  # pixels
        self.FONT_SIZE = 1
        self.FONT_THICKNESS = 2
        self.HANDEDNESS_TEXT_COLOR = (88, 205, 54)  # vibrant green
        self.results = None

        self.scale = -1
        self.z_scale = 5
        self.thresh = 0.1

        self.car_pos_buf = []
        self.thumb = []

        self.car_in_hand = 0

        self.fps = 1
        self.wind_up = False
        self.osc = False
        self.wind = 0
        self.release = False
        self.throw = 0

        self.h1_last = None
        self.h2_last = None
        self.h1 = ''
        self.h2 = ''


    def draw_landmarks_on_image(self, rgb_image, detection_result):
        if detection_result is None:
            return rgb_image
        hand_landmarks_list = detection_result.hand_landmarks
        world_landmarks = detection_result.hand_world_landmarks
        handedness_list = detection_result.handedness
        annotated_image = np.copy(rgb_image)

        # Loop through the detected hands to visualize.
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            handedness = handedness_list[idx]

            # Draw the hand landmarks.
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend([
                landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
            ])
            solutions.drawing_utils.draw_landmarks(
                annotated_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style(),
                solutions.drawing_styles.get_default_hand_connections_style())

            # Get the top left corner of the detected hand's bounding box.
            height, width, _ = annotated_image.shape
            x_coordinates = [landmark.x for landmark in hand_landmarks]
            y_coordinates = [landmark.y for landmark in hand_landmarks]
            text_x = int(min(x_coordinates) * width)
            text_y = int(min(y_coordinates) * height) - self.MARGIN

            # Draw handedness (left or right hand) on the image.
            cv2.putText(annotated_image, f"{handedness[0].category_name}",
                        (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                        self.FONT_SIZE,
                        self.HANDEDNESS_TEXT_COLOR, self.FONT_THICKNESS, cv2.LINE_AA)

        return annotated_image

    def reset(self):
        self.throw = 0
        self.release = False
        self.car_pos_buf = []

        self.wind = 0
        self.wind_up = False

        self.osc = False
        self.h1_last, self.h2_last = None, None
        self.h1, self.h2 = '', ''
        return

    def getHands(self, detection_result):
        if detection_result is None:
            return None, None

        hand_landmarks_list = detection_result.hand_landmarks
        handedness_list = detection_result.handedness

        if len(handedness_list) == 0:
            return None, None

        hand1 = hand2 = None

        if handedness_list[0][0].category_name == 'Left':
            hand1 = hand_landmarks_list[0]
            if len(handedness_list) == 2:
                hand2 = hand_landmarks_list[1]
        else:
            hand2 = hand_landmarks_list[0]
            if len(handedness_list) == 2:
                hand1 = hand_landmarks_list[1]

        return hand1, hand2


    def car_inhand(self, car, hand1, hand2, shape, thresh=15):
        if not car:
            self.car_in_hand = 0
            return

        if self.within_area(car, shape, hand1, thresh) or self.within_area(car, shape, hand2, thresh):
            self.car_in_hand = 1
        else:
            if self.car_in_hand != 0:
                self.car_in_hand += 1
            if self.car_in_hand > 3:  # Must let go for 5 frames to be considered released
                self.car_in_hand = 0

    def detect_release(self, car, hand1, hand2, shape, thresh=20, thresh_mv=100, reset=False):
        if reset:
            self.reset()
            return "RESET", False

        if not car:
            self.reset()
            return "Car Off Screen", True

        car_pos = np.array([car[0]*shape[1], car[1]*shape[0]])

        if self.wind_up:
            if self.car_in_hand == 0 and not self.release:
                self.release = True

            if self.release and self.car_in_hand > 0:
                self.reset()
                return "Touch After Release [RESET]", True

            if self.car_in_hand > 0 and (not self.within_area(car, shape, hand1, thresh) or not self.within_area(car, shape, hand2, thresh)):
                self.throw += 1
                if self.throw > 9:
                    self.reset()
                    return "Invalid Move [RESET]", True

            if self.release and self.car_in_hand == 0:
                self.car_pos_buf.append(car_pos)
                # Buffer only contains car position of last half second
                if len(self.car_pos_buf) > self.fps/2:
                    self.car_pos_buf.pop(0)
                    car_dist = np.linalg.norm(self.car_pos_buf[-1] - self.car_pos_buf[0])
                    if car_dist > thresh_mv:
                        self.reset()
                        return "Release Detected", True
            return "Wind-up Detected", False
        return "Wind-up Detected", False

    def detect_wind_up(self, car, hand1, hand2, shape, thresh=30, reset=False):
        if reset:  # Manual Restart
            self.reset()
            return "RESET", False

        if self.wind_up:
            return "Wind-up Detected", True

        if not car:
            return "NO CAR", False

        if not hand1 or not hand2:
            return "HAND(S) MISSING", False

        if self.within_area(car, shape, hand1, thresh) and self.within_area(car, shape, hand2, thresh):
            self.wind += 1
            if self.wind > self.fps*2 and self.osc:  # If both hands are on the car for 2 seconds, assume wind up
                self.wind_up = True
                self.wind = 0
                return "Wind-up Detected", True
        else:
            self.reset()

        if self.wind > self.fps/2:
            return "No Twist Detected", False

        return "Ready", False

    def detect_oscillation(self, car, hand1, hand2, shape, thresh=10, reset=False):
        if reset:
            self.reset()
            return "RESET", False

        if self.osc:
            return "Oscillation Detected", False

        if not car:
            self.reset()
            return "NO CAR", False

        if not hand1 or not hand2:
            self.reset()
            return "HAND(S) MISSING", False

        if not self.within_area(car, shape, hand1, 30) or not self.within_area(car, shape, hand2, 30):
            self.reset()
            return "", False

        # Thumb and index
        if hand1:
            h1_1, h1_2 = hand1[4], hand1[8]
            h1_dx = (h1_1.x - h1_2.x)*shape[1]
            h1_dy = (h1_1.y - h1_2.y)*shape[0]
            h1_d = np.linalg.norm(np.array([h1_dx, h1_dy]))

            if self.h1_last:
                if h1_d - self.h1_last > thresh:
                    self.h1 += 'a'
                    self.h1_last = h1_d
                elif self.h1_last - h1_d > thresh:
                    self.h1 += 'd'
                    self.h1_last = h1_d
                if len(self.h1) > 7:
                    self.h1 = self.h1[1:]

            if self.h1_last is None:
                self.h1_last = h1_d

            if self.testDeltaStr(self.h1):
                self.osc = True
                return "Twisting Detected", True

        if hand2:
            h2_1, h2_2 = hand2[4], hand2[8]
            h2_dx = (h2_1.x - h2_2.x)*shape[1]
            h2_dy = (h2_1.y - h2_2.y)*shape[0]
            h2_d = np.linalg.norm(np.array([h2_dx, h2_dy]))

            if self.h2_last:
                if h2_d - self.h2_last > thresh:
                    self.h2 += 'a'
                    self.h2_last = h2_d
                elif self.h2_last - h2_d > thresh:
                    self.h2 += 'd'
                    self.h2_last = h2_d
                if len(self.h2) > 7:
                    self.h2 = self.h2[1:]
            if self.h2_last is None:
                self.h2_last = h2_d

            if self.testDeltaStr(self.h2):
                self.osc = True
                return "Twisting Detected", True

        return "Ready", False

    def within_area(self, car, shape, hand, thresh=15):
        if hand is None:
            return False
        landmarks = [4, 8, 12, 16, 20, 9]

        low_x = (car[0] - car[2]/2)*shape[1] - thresh
        top_x = (car[0] + car[2]/2)*shape[1] + thresh

        low_y = (car[1] - car[3]/2)*shape[0] - thresh
        top_y = (car[1] + car[3]/2)*shape[0] + thresh

        for point in landmarks:
            hand_pos = np.array([hand[point].x*shape[1], hand[point].y*shape[0]])

            if low_x <= hand_pos[0] <= top_x and low_y <= hand_pos[1] <= top_y:
                return True
        return False

    def testDeltaStr(self, d_str):
        if not d_str or len(d_str) < 4:
            return False
        if not 'a' in d_str or not 'd' in d_str:
            return False
        if d_str.find('aa') > -1 or d_str.find('dd') > -1 or d_str.find('ad') > -1 or d_str.find('da') > -1:
            self.osc = True
            return True
        return False

    # Create a hand landmarker instance with the live stream mode:
    def print_result(self, result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
        self.results = result

def detect(save_img=False):
    source, weights, view_img, save_txt, imgsz, trace, id_num = opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size, not opt.no_trace, opt.id
    save_img = not opt.nosave and not source.endswith('.txt')  # save inference images
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
        ('rtsp://', 'rtmp://', 'http://', 'https://'))

    # Directories
    save_dir = Path(increment_path(Path(opt.project) / opt.name, exist_ok=opt.exist_ok))  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    device = select_device(opt.device)
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check img_size

    # Load hand module
    hand_module = HandLModule()

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path='./hand_landmarker.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=hand_module.print_result,
        num_hands=2,
        min_hand_detection_confidence=0.1,  # experiment with this
        min_hand_presence_confidence=0.1,  # experiment with this
        min_tracking_confidence=0.2)  # experiment with this

    if trace:
        model = TracedModel(model, device, opt.img_size)

    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadWebcam(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    old_img_w = old_img_h = imgsz
    old_img_b = 1

    t0 = time.time()

    start = time.perf_counter()
    curr_date = str(datetime.now().strftime("%b-%d-%Y %H:%M:%S"))
    trial_num = 1

    logger = logging.getLogger(__name__)
    log_name = 'logs/' + id_num + '_windup.log'
    logging.basicConfig(filename=log_name, encoding='utf-8', format="%(message)s", level=logging.INFO)
    history_str = curr_date + ',' +  str(trial_num)
    with HandLandmarker.create_from_options(options) as landmarker:
        tstamp = 0

        # Stages
        stage = 0  # 1 = oscillation, 2 = windup, 3 =

        msg_timer = 0
        msg = "Ready"

        for path, img, im0s, vid_cap in dataset:
            # image for mediapipe
            tstamp += 1
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=im0s)
            hand_module.fps = vid_cap  # Fix this

            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)


            landmarker.detect_async(mp_image, tstamp)
            hand_mod_results = hand_module.results
            hand1, hand2 = hand_module.getHands(hand_mod_results)

            annotated_image = hand_module.draw_landmarks_on_image(mp_image.numpy_view(), hand_mod_results)

            # Warmup
            if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    model(img, augment=opt.augment)[0]

            # Inference
            t1 = time_synchronized()
            with torch.no_grad():  # Calculating gradients would cause a GPU memory leak
                pred = model(img, augment=opt.augment)[0]
            t2 = time_synchronized()

            # Apply NMS
            pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
            t3 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)


            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0, frame = path[i], '%g: ' % i, annotated_image, dataset.count
                else:
                    p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    max_conf = -1
                    xywh = None
                    xyxy_max = None
                    label_max = None
                    cls_max = None

                    for *xyxy, conf, cls in reversed(det):
                        if conf > max_conf:
                            max_conf = conf
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                            xyxy_max = xyxy
                            label_max = f'{names[int(cls)]} {conf:.2f}'
                            cls_max = cls

                    im0 = im0.astype(np.uint8)
                    plot_one_box(xyxy_max, im0, label=label_max, color=colors[int(cls_max)], line_thickness=1)  # plot box with highest confidence

                    if xywh is not None:
                        xywh = xywh[:4]

                    hand_module.car_inhand(xywh[:4], hand1, hand2, im0.shape)
                    osc_msg, osc_interrupt = hand_module.detect_oscillation(xywh, hand1, hand2, im0.shape)
                    windup_msg, windup = hand_module.detect_wind_up(xywh, hand1, hand2, im0.shape)
                    release_msg, release = hand_module.detect_release(xywh, hand1, hand2, im0.shape)

                    # Set Message
                    if osc_interrupt:
                        curr_time = time.perf_counter()
                        history_str += f',{float(curr_time-start):.2f},{osc_msg}'

                    match stage:
                        case 2:
                            if msg_timer == 0:  # Logs immediately instead of 2 seconds later
                                logger.info(history_str)

                            msg_timer += 1
                            if msg_timer >= hand_module.fps*2:
                                msg_timer = 0
                                stage = 0
                                msg = 'Ready'
                                trial_num += 1

                                history_str = curr_date + ',' +  str(trial_num)
                                start = time.perf_counter()

                        case 1:
                            msg = release_msg
                            if release:
                                curr_time = time.perf_counter()
                                history_str += f',{float(curr_time-start):.2f},{msg}'
                                stage += 1
                        case 0:
                            if windup_msg != "":
                                msg = windup_msg
                            if windup:
                                curr_time = time.perf_counter()
                                history_str += f',{float(curr_time-start):.2f},{msg}'
                                stage += 1

                # Print time (inference + NMS)
                print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')
                im0 = im0.astype(np.uint8)
                legal = ['Ready', 'Release Detected', 'Oscillation Detected', 'Wind-up Detected']
                if msg in legal:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                textsize = cv2.getTextSize(msg, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]

                tX = int((im0.shape[1] - textsize[0]) / 2)
                tY = int(textsize[1])

                im0 = cv2.putText(im0, msg, (tX, tY), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA, False)

                # Stream results
                if view_img:
                    cv2.imshow("hands", im0)
                    cv2.waitKey(1)  # 1 millisecond

        print(f'Done. ({time.time() - t0:.3f}s)')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='tiny_car.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='inference/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--id', default='guest', type=str, help='id number')
    parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--no-trace', action='store_true', help='don`t trace model')
    global opt
    opt = parser.parse_args()
    print(opt)

    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['tiny_car.pt']:
                detect()
                strip_optimizer(opt.weights)
        else:
            detect()


if __name__ == '__main__':
    main()
