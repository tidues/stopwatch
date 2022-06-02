import time

class Stopwatch:
    def __init__(self, name='stopwatch', on=True):
        self.name = name
        self.on = on
        self.hist = {}
        self.lap_idx = 0

    def start(self):
        if not self.on:
            return 0
        self.lap_idx = 0
        self.hist = {}
        self.hist['start'] = time.time()

    def lap(self, name=None):
        if not self.on:
            return 0
        self.lap_idx += 1
        if name is None:
            name = 'lap' + str(self.lap_idx)
        self.hist[name] = time.time()

    # histType: 0: absolute times; 1: relative times; 2: time lapse
    def getHist(self, histType=1):
        if not self.on:
            return 0
        if histType == 0:
            return self.hist
        elif histType == 1:
            keys = list(self.hist)
            return {keys[i]: self.hist[keys[i]] - self.hist[keys[0]] for i in range(1, len(keys))}
        else:
            keys = list(self.hist)
            return {keys[i]: self.hist[keys[i]] - self.hist[keys[i-1]] for i in range(1, len(keys))}


def main():
    import numpy as np
    sw = Stopwatch('test')
    iters = 6
    gaps = np.random.random(iters) * 5
    sw.start()
    for i in range(iters):
        time.sleep(gaps[i])
        sw.lap('round' + str(i))
    print(sw.getHist(0))
    print(sw.getHist(1))
    print(sw.getHist(2))


if __name__ == '__main__':
    main()
