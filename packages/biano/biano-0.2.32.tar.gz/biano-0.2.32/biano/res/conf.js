// 左手按键
left: {
    // 1 1# 2 2# 3
    q:0, w:1, e:2, r:3, t:4,
    // 4 4# 5 5#
    a:5, s:6, d:7, f: 8
    // 6 6# 7
    z:9, x:10, c:11
}
// 右手按键
right: {
    // 1 1# 2 2# 3
    y:0, u:1, i:2, o:3, p:4,
    // 4 4# 5 5#
    h:5, j:6, k:7, l: 8
    // 6 6# 7
    n:9, m:10, ',':11
}
// 调整按键基础音调
bases: {
    '1': {left: 16}
    '2': {left: 28}
    '3': {left: 40}
    '4': {left: 52}
    '5': {left: 74}
    '6': {right: 16}
    '7': {right: 28}
    '8': {right: 40}
    '9': {right: 52}
    '0': {right: 74}
}
// 左右按键基础音调调节
offsets: {
    '-': {left:0, right:0}
    '=': {left:-24, right:24}
}
// 声音混合模式: mix/weight
combines: {
    '+': weight
    "_": mix
}
// 按键监听模式: 
// full: 全局
// current: 当前窗口
kb: full
// 初始化，自动按这些键
inits: [
    '3','9', '+', '-'
]