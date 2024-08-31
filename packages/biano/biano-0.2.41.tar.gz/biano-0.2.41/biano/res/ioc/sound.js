{
    id: obj.frate
    type: obj
    src: biano.sound1.F4
    args: [
        [ref, sound.fps]
        [ref, sound.base.count]
        [ref, sound.base.rate]
    ]
}
{
    id: obj.cfrate
    type: obj
    src: biano.sound1.CacheFc
    args: [
        [ref, obj.frate]
        [ref, sound.sec, 1.0]
    ]
}
{
    id: src.stream
    type: obj
    src: biano.sound1.create
    args: [
        [ref, sound.fps]
    ]
}
{
    id: obj.sound
    type: obj
    src: biano.sound1.Sound
    args: [
        [ref, obj.cfrate]
        [ref, src.stream]
        [ref, obj.stream.cache]
    ]
}