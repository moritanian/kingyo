# -*- coding: utf-8 -*-
import numpy as np
import cv2
import screeninfo
import random

if __name__ == '__main__':


    # hyper parameters
    MIN_AREA = 500

    cap = cv2.VideoCapture(0)


    screen_id = 0
    # get the size of the screen
    screen = screeninfo.get_monitors()[screen_id]
    width, height = screen.width, screen.height
    
    fgbg = cv2.createBackgroundSubtractorMOG2()
    #fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    #fgbg=cv2.bgsegm.createBackgroundSubtractorGMG()    
    
    while(True):
        # フレームをキャプチャする
        ret, original_frame = cap.read()

        fgmask = fgbg.apply(original_frame)

        # 二値変換
        thresh = 1.0
        max_pixel = 1.0
        ret, binary_frame = cv2.threshold(fgmask,
                                     thresh,
                                     max_pixel,
                                     cv2.THRESH_BINARY)
        #fgmask = np.ones(fgmask.shape)
        #fgmask = dilate(fgmask)
        kernel1 = np.ones((3,3),np.uint8)
        kernel2 = np.ones((13,13),np.uint8)

        closed_frame = cv2.morphologyEx(binary_frame, cv2.MORPH_CLOSE, kernel2)
        #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel1)

        #nLabels, labelImage = cv2.connectedComponents(closed_frame)
        nLabels, labelImage, contours, CoGs = cv2.connectedComponentsWithStats(closed_frame)
        result = np.zeros(original_frame.shape)
        #result[:,:,0] = original_frame[:,:,0] * fgmask
        #result[:,:,1] = original_frame[:,:,1] * fgmask
        #result[:,:,2] = original_frame[:,:,2] * fgmask

     

        cand_num = 0
        cand_info_list = []
        for nLabel in range(1, nLabels):
            x,y,w,h,size = contours[nLabel]
            xg,yg = CoGs[nLabel]

            if size < MIN_AREA:
                continue    

            indexes = (labelImage == nLabel)*1.0 / 255.0
    
            #result[:,:,0] += indexes * colors[i][0]
            #result[:,:,1] += indexes * colors[i][1]
            #result[:,:,2] += indexes * colors[i][2]
            cv2.circle(result, (int(xg), int(yg)), 2, (255, 0, 0), -1)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
            result[:,:,0] += original_frame[:,:,0] * indexes
            result[:,:,1] += original_frame[:,:,1] * indexes
            result[:,:,2] += original_frame[:,:,2] * indexes


            cand_num += 1


        # 画面に表示する
        window_name = 'projector'
        if False:
            cv2.namedWindow(window_name, cv2.WINDOW_KEEPRATIO | cv2.WND_PROP_FULLSCREEN)
            cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                                  cv2.WINDOW_FULLSCREEN)

        # write info
        font = cv2.FONT_HERSHEY_PLAIN
        font_size = 0.6
        text = "cand_num = " + str(cand_num)
        cv2.putText(result,text,(20,20),font, font_size,(255,255,255))

        # windows
        cv2.imshow("original", original_frame)
        cv2.imshow("fgbg", fgmask)
        
        cv2.imshow(window_name, result)


        # キーボード入力待ち
        key = cv2.waitKey(1) & 0xFF

        # qが押された場合は終了する
        if key == ord('q'):
            break



    # キャプチャの後始末と，ウィンドウをすべて消す
    cap.release()
    cv2.destroyAllWindows()
