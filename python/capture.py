# -*- coding: utf-8 -*-
import numpy as np
import cv2
import screeninfo

def kmeans_effect(frame):
    Z = frame.reshape((-1,3))
 
    # float32に変換
    Z = np.float32(Z)

    # K-Means法
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2
    ret,label,center=cv2.kmeans(Z,
              K,
              None,
              criteria,
              10,
              cv2.KMEANS_RANDOM_CENTERS)

    # UINT8に変換
    center = np.uint8(center)
    res = center[label.flatten()]
    frame = res.reshape((frame.shape))
    return frame

def blur_effect(frame):
    return cv2.GaussianBlur(frame, ksize=(5,5),sigmaX=2)
def bilateral_effect(frame):
    return cv2.bilateralFilter(frame, d=5, sigmaColor=5, sigmaSpace=2)

def movement_detect(frame, back_frame):
    frame = frame.astype(np.float32)

    # 差分計算
    diff_frame = cv2.absdiff(frame, back_frame)

    # 背景の更新
    cv2.accumulateWeighted(frame, back_frame, 0.05)

    return (diff_frame, back_frame)

# 膨張処理
def dilate(frame, ksize=3):
    # 入力画像のサイズを取得
    h, w = frame.shape
    # 入力画像をコピーして出力画像用配列を生成
    dst = frame.copy()
    # 注目領域の幅
    d = int((ksize-1)/2)

    for y in range(0, h):
        for x in range(0, w):
            # 近傍に白い画素が1つでもあれば、注目画素を白色に塗り替える
            roi = frame[y-d:y+d+1, x-d:x+d+1]
            if np.count_nonzero(roi) > 0:
                dst[y][x] = 255

    return dst

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)


    screen_id = 0
    # get the size of the screen
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height

    # first frame
    ret, original_frame = cap.read()
    frame = original_frame
    #frame = cv2.Canny(original_frame, 50, 110)


    # 背景フレーム
    back_frame = np.zeros_like(frame, np.float32)

    while(True):
        # フレームをキャプチャする
        ret, original_frame = cap.read()

        #frame = blur_effect(frame)
        #frame = bilateral_effect(frame)
        
        #frame = cv2.Canny(original_frame, 50, 110)
        frame = original_frame
        (diff_frame, back_frame) = movement_detect(frame, back_frame)
        
        #diff_frame = dilate(diff_frame)

         # グレースケールに変換
        img_gray = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
     
        # 二値変換
        thresh = 1.0
        max_pixel = 1.0
        ret, frame = cv2.threshold(img_gray,
                                     thresh,
                                     max_pixel,
                                     cv2.THRESH_BINARY)

        
        frame = original_frame.copy()
        #diff_frame = np.ones(diff_frame.shape)
        frame[:,:,0] = img_gray * original_frame[:,:,0]
        frame[:,:,1] = img_gray * original_frame[:,:,1]
        frame[:,:,2] = img_gray * original_frame[:,:,2]

        # 画面に表示する
        window_name = 'projector'
        if False:
            cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO | cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                                  cv2.WINDOW_FULLSCREEN)

        #cv2.imshow(window_name,frame)
        cv2.imshow(window_name, frame)

        # キーボード入力待ち
        key = cv2.waitKey(1) & 0xFF

        # qが押された場合は終了する
        if key == ord('q'):
            break



    # キャプチャの後始末と，ウィンドウをすべて消す
    cap.release()
    cv2.destroyAllWindows()
