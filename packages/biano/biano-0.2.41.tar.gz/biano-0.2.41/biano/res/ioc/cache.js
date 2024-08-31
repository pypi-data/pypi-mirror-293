datas: [
    {
        id: obj.stream.cache
        type: obj
        src: biano.cache.Stream
        args: [
            [ovar, src.stream, write]
            [val, 32768.0]
            [ref, stream.cache.num]
            [ref, stream.cache.unit]
            [ref, base.dtype]
            [ref, stream.cache.keep]
        ]
        maps: {
            ws: [ref, stream.filter.ws]
            rate: [ref, sound.voice]
        }
    }
]