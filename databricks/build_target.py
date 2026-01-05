"""
BuildTarget题
给一个dependency tree，需要找出bottlencks。task可以concurrent build, 假设每个task build的时间相同，在同一时间只有一个task在build的情况就是一个bottleneck
给了BFS的解法，问了复杂度，写了test cases，还是挂了
"""