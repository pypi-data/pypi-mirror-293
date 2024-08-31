{
    // 采样频率(每秒多少采样)，默认327680，减小频率可以减少计算开销（计算开销应该不大，用了numpy）
    // 修改这个记得把stream.cache.unit一起修改了，建议是stream.cache.unit=int(sound.fps*0.05)
    // sound.fps: 327680

    // 声音流单次播放采样数，默认16384==fps*0.05(0.05秒)
    // stream.cache.unit: 16384
    
    // 声音流播放时锁住后续缓存数量，默认1
    // stream.cache.keep: 1

    // 声音流缓存数量，默认100
    // stream.cache.num: 100

    // 池化类型，max或avg，默认max
    // stream.cache.pool.type: max
    // 声波池化，默认0（不池化）
    // stream.cache.pool.size: 0
    // 音量
    sound.voice: 0.15

    // 下面这两个影响音色:

    // 基音+泛音数量
    sound.base.count: 17

    // 基音/泛音每级占比
    // 基音*rate+(1-rate)*rate*泛音[1]+(1-rate)*(1-rate)*rate*泛音[2]+...
    sound.base.rate:0.9

    // 声波衰减级别(0-n)，0衰减最少（还是在衰减）
    // sound.base.dec: 0

    // 定制化按键布局文件路径，默认是空，只有进行按键时用到，可以自己写一个
    // 已有的布局文件: conf.js, hard.js
    // 只对keyboard生效
    fp.keys.custom: hard.js

    // 播放乐谱的配置文件
    // 只对play生效
    play.confs: datas/conf.js

    // 重放的记录文件
    // 只对replay生效
    file.records: null

    // 不同电脑声音设备不一样，
    // 觉得声音有时候突然变小可以试试把这个值设置成false，对应代码biano.cache.Stream.clean_dt
    stream.cache.zero: false

    // 按键模式
    // 只对按键弹奏生效，这里配置了就以这里为准，keyboard配置文件里的kb配置将不会生效
    // keyboard.type: current

    // 运行程序，默认keyboard
    /*
        运行程序，默认keyboard
        可选:
            keyboard: 按键弹奏
            play: 播放乐谱
            replay: 重放keyboard按键记录文件
    */
    run: keyboard

    /*
        降噪算子，权重加起来应该等于1，默认值是按以下计算出来的:
            ws=[0.9, 0.9*0.9, 0.9*0.9*0.9, ...]
            ws = ws/sum(ws)
        要改的话，建议也用代码生成一个
    */
    // stream.filter.ws: 

    // 按键音播放时间，默认1秒
    // sound.sec: 1.0

}