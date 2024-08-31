datas: [
    {
        id: obj.confkeys
        type: obj
        src: biano.confkeys.build
        args: [
            [ref, keys.confs]
            [ref, obj.sound]
            [branch, [ref, keyboard.type], {full: [ref, keyboard.type.full], current: [ref, keyboard.type.current]}, null]
        ]
    }
    {
        id: keyboard
        type: mcall
        src: obj.confkeys
        mcall: run
    }
    {
        id: keyboard.type.full
        type: obj
        src: biano.pynkb.KB
        call: {
            type: mcall
            mcall: set_callback
            args: [[ovar, obj.confkeys, press]]
        }
    }
    {
        id: keyboard.type.current
        type: obj
        src: biano.bzkb.KB
        call: {
            type: mcall
            mcall: set_callback
            args: [[ovar, obj.confkeys, press]]
        }
    }
]