datas: [
    {
        id: obj.play
        type: obj
        src: biano.play.Play
        args: [
            [ref, obj.sound]
        ]
    }
    {
        id: play
        type: mcall
        src: obj.play
        mcall: __call__
        args: [
            [ref, play.confs]
        ]
    }
    {
        id: replay
        type: mcall
        src: obj.play
        mcall: replay
        args: [
            [ref, file.records]
        ]
    }
]