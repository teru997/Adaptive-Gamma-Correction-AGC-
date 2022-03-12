# Adaptive-gamma-correction
## 適正ガンマ補正を実装
汎用性,可逆性のある画像強調手法として提案されたAdaptive gamma correction(AGC)を実装しました.
画質の評価指標にはOpenCVのBRISQUEモデルを利用しています．
https://github.com/opencv/opencv_contrib/tree/master/modules/quality/samples
AGC以外に,Histogram equalizationやCLAHE(Contrast Limited Adaptive Histogram Equalization)も利用できます．

## 参考論文：
Shanto Rahman, Md Mostafijur Rahman, M. Abdullah-Al-Wadud, Golam Dastegir Al-Quaderi  Mohammad Shoyaib ,
 ” An adaptive gamma correction for image enhancement”, EURASIP Journal on Image and Video Processing 2016,Article number:35
https://jivp-eurasipjournals.springeropen.com/articles/10.1186/s13640-016-0138-1
