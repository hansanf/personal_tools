import cv2
import json
import glog as log

# 打开JSON文件
with open('personal_tools/python/yolox.json', 'r') as f:
    data = json.load(f)
# 现在，data是一个包含JSON文件内容的字典

with open("personal_tools/python/people_result_0.json") as f:
  people = json.load(f)
with open("personal_tools/python/vehicle_result_0.json") as f:
  vehicle = json.load(f)
with open("personal_tools/python/road_result_0.json") as f:
  road_sign = json.load(f)


combo_boxes = data['data']['combo_boxes']

def parse_box(combo_boxes):
  box_list = []
  for i in range(0, len(combo_boxes)):
    box = combo_boxes[i]['main_bbox']
    # box_list.append(
    #   [
    #     [round(box['x1']), round(box['y1'])],
    #     [round(box['x2']), round(box['y2'])]
    #   ]
    # )
    box_list.append(box)
  return box_list

box_list = parse_box(combo_boxes)

def plot_box(img, box_list, people, vehicle, road_sign):
  for i in range(0, len(box_list)):
    # [(x1, y1), (x2, y2)]
    main_bbox = box_list[i]
    box = [
      [round(main_bbox['x1']), round(main_bbox['y1'])],
      [round(main_bbox['x2']), round(main_bbox['y2'])]
    ]
    # 在图像上绘制矩形
    label = main_bbox['label']
    if label == 0: # vehicle
      cv2.rectangle(img, box[0], box[1], (0, 255, 0), 1) # （蓝色，绿色，红色）
    elif label == 1: # person
      cv2.rectangle(img, box[0], box[1], (0, 255, 255), 1)
    else:
      cv2.rectangle(img, box[0], box[1], (0, 0, 255), 1)
    
    # 添加文字
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 标识出分类结果的标签值
    def classify_label(cls_result):
      for c in cls_result:
        if c['yindex'] == i:
          if c['ylabel'] == label:
            for j in range(len(c['label'])):
              cv2.putText(img, str(c['label'][j]), (box[0][0], box[0][1]+20*j), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
          else:
            log.error("det {}th bbox equal to yindex, but not the labels are not equal")
    classify_label(people)
    classify_label(vehicle)
    classify_label(road_sign)
    
    # 标识出检测结果中的第几个框
    cv2.putText(img, str(i), (box[0][0]-10, box[0][1]-10), font, 1, (0, 0, 0), 2, cv2.LINE_AA)

# 读取图像
img = cv2.imread('personal_tools/python/1700881727050.jpg')
plot_box(img, box_list, people, vehicle, road_sign)


# 显示图像
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()