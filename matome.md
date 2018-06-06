# 概要
webクライアント　金魚リアルタイム表示
webcam 水槽撮影
webserver
	- socket io
	- python 画像処理



# 実装
## client
processing
https://github.com/dasl-/my-life-aquatic/blob/master/public/processing/Fish.pjs

## anakonda
http://imagingsolution.net/program/python/anaconda/python-multi-version-environment/

## server 

### 動画配信
webrtc
 pythonで加工した画像を配信したい
 openRTC?

 https://qiita.com/mechamogera/items/ae283c651ae93cf76310

### webrtc capture
https://github.com/muaz-khan/WebRTC-Experiment/tree/master/Pluginfree-Screen-Sharing

結局以下のextensionを手動で追加
https://chrome.google.com/webstore/detail/screen-capturing/ajhifddimkapgcifgcodmmfdlknahffk

## chrome 操作
https://www.inet-solutions.jp/technology/python-selenium/

## 画像処理
- R-CNN
- fast R-CNN
- SSD

### cuda環境
The following packages will be DOWNGRADED: python: 3.6.4-h6538335_1 --> 3.5.4-h1357f44_23

/*
 ダメ conda install -c menpo opencv3
	conda install python=3.5
	でバージョン戻せる
*/
https://qiita.com/cointoss1973/items/92d82f9accb239a276a0
pip install opencv-python
pip install opencv-contrib-python

```
conda info -e
activate cuda-env
jupyter notebook
```

https://qiita.com/nkn-khr/items/92a0e8f94521349b1515
http://tecsingularity.com/cuda/version/

```
// https://developer.nvidia.com/rdp/cudnn-download
// https://developer.nvidia.com/rdp/cudnn-download
conda create -n [仮想環境名] python=3.6
activate [仮想環境名]
pip install tensorflow-gpu==1.3.0
pip install keras==1.2

```
- power shell 文字コード
chcp 65001

### ssd300 sample 結果
CPUで1.5fps
GPUで30fps
### 学習
http://ai-coordinator.jp/ssd-keras-train

# webVR * WebRTC
 https://qiita.com/mechamogera/items/ae283c651ae93cf76310
 
