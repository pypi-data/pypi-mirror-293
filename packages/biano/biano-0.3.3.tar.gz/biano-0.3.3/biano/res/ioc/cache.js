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
            zero: [ref, stream.cache.zero]
            fc_pool: [ref, stream.cache.pool]
            pool_size: [ref, stream.cache.pool.size]
        }
    }
    {
        id: stream.cache.pool
        type: branch
        judge: [ref, stream.cache.pool.type]
        vals: {
            max: [var, biano.cache.max_pool]
            avg: [var, biano.cache.avg_pool]
        }
        default: [var, biano.cache.max_pool]
    }
]