# biano
```
键盘按键钢琴，监听按键发出声音，可以后台运行
keyboard piano, listen key press to play sound, can run background
运行(run):
python -m biano
or
python -m biano configpath.js

运行复杂按键模式（建议先看下hard.js配置，在biano模块文件夹/res目录下）:
python -m biano hard.js

按键对应音符:
keys to musical note:

左手(left hand):
 q  w  e  r  t 
 1 #1  2 #2  3
 a  s  d  f
 4 #4  5 #5
 z  x  c
 6 #6  7

右手(right hand):
 y  u  i  o  p
 1 #1  2 #2  3
 h  j  k  l
 4 #4  5 #5
 n  m  ,
 6 #6  7

数字键1,2,3,4,5修改左手基准音调
数字键6,7,8,9,0修改右手基准音调

number keys 1,2,3,4,5 modify base tone of left hand
number keys 6,7,8,9,0 modify base tone of right hand

按键-和=修改数字键音调偏移
keys - and = modify number key tone offset

v0.2.2:
加缓存，原本创建多个声音对象改成使用一个声音对象，用缓存方式进行读写，减少杂音，但会增加延迟
音色有待调整

v0.2.3:
加配置，按键和音调可配置，运行
python -m biano 配置文件.js
配置文件会先从当前目录找（或者输入的是绝对路径，找的就是绝对路径下的文件），找不到会从biano模块文件夹/res目录下找
配置见: biano模块文件夹/res/conf.js(默认配置文件)
程序会先读取默认配置文件，再读取命令行指令配置文件进行更新
噪声有待处理
```
