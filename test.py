import cv2
import numpy as np

# 唤醒摄像头
cap = cv2.VideoCapture(0)

print("正在运行颜色追踪...拿起一个蓝色的物品放在摄像头前吧！")

while True:
    success, frame = cap.read()
    if not success:
        break

    # 1. 视角转换：把普通的 RGB 彩色图像转换成 HSV 格式
    # （机器人在 HSV 模式下更容易区分颜色，不受光照强弱的干扰）
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2. 设定“蓝色”的阈值范围
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])

    # 3. 施展魔法：制作一个掩膜（Mask），把蓝色的地方变白，其他地方变黑
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 4. 寻找白色区域的轮廓（也就是蓝色的物体）
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # 过滤掉太小的噪点，只抓取大一点的物体
        if area > 500: 
           # 计算出这个物体的外接矩形坐标：x, y 是左上角，w, h 是宽高
            x, y, w, h = cv2.boundingRect(cnt)
            
            # 计算目标的中心点坐标 (cx, cy)
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            
            # 1. 画绿色的边框
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # 2. 在中心点画一个红色的实心圆点，作为机器人的“瞄准星”
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            
            # 3. 把实时坐标数据打印在画面上（这就是未来传给单片机的反馈信号）
            coord_text = f"Target X:{cx} Y:{cy}"
            cv2.putText(frame, coord_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # 显示处理后的画面
    cv2.imshow('Robot Eye - Vision', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()