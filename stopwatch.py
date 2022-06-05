import time
from datetime import datetime


# get datetime string
def dtstr():
    now = datetime.now()
    return now.strftime("%m%d%Y%H%M%S"), now


class TimeLimitException(Exception):
    def __init__(self, message="Out of time limit"):
        self.message = message
        super().__init__(self.message)


class Stopwatch:
    def __init__(self, name='stopwatch', digits=None, on=True, timebgt=None, raise_err=False):
        self.timebgt = timebgt
        self.raise_err = raise_err
        self.name = name
        self.on = on
        self.hist = {}
        self.digits = digits
        self.lap_idx = 0

    def start(self):
        if not self.on:
            return 0
        self.lap_idx = 0
        self.hist = {}
        self.hist['start'] = time.time()
        return self.hist['start']

    def lap(self, name=None):
        if not self.on:
            return 0
        self.lap_idx += 1
        if name is None:
            name = 'lap' + str(self.lap_idx)
        self.hist[name] = time.time()
        if self.timebgt is None:
            res = self.hist[name]
        else:
            res = self.timebgt - (self.hist[name] - self.hist['start'])
            if res <= 0 and self.raise_err:
                raise TimeLimitException
        return res

    # histType: 0: absolute times; 1: relative times; 2: time lapse
    def info(self, histType=1):
        if not self.on:
            return 0
        if histType == 0:
            res = self.hist
        elif histType == 1:
            keys = list(self.hist)
            res = {keys[i]: self.hist[keys[i]] - self.hist[keys[0]] for i in range(1, len(keys))}
        else:
            keys = list(self.hist)
            res = {keys[i]: self.hist[keys[i]] - self.hist[keys[i-1]] for i in range(1, len(keys))}
        if self.digits is not None:
            res = {key: round(res[key], self.digits) for key in res}
        return res

    # get total time
    def total_time(self):
        keys = list(self.hist)
        res = self.hist[keys[-1]] - self.hist[keys[0]]
        if self.digits is not None:
            res = round(res, self.digits)
        return res


def main():
    import numpy as np
    sw = Stopwatch('test')
    iters = 6
    gaps = np.random.random(iters) * 5
    sw.start()
    for i in range(iters):
        time.sleep(gaps[i])
        sw.lap('round' + str(i))
    print(sw.info(0))
    print(sw.info(1))
    print(sw.info(2))


if __name__ == '__main__':
    main()
