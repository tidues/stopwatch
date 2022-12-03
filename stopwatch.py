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
    def __init__(self, digits=None, on=True, timebgt=None, raise_err=False):
        self.timebgt = timebgt
        self.raise_err = raise_err
        self.on = on
        self.hist = {}
        self.digits = digits
        self.lap_idx = 0

    def init(self, start=False, name=None):
        if not self.on:
            return 0
        self.lap_idx = 0
        self.hist = {}
        if name is None:
            self.pfix = 'lap'
        else:
            self.pfix = name
        if start:
            self.start()

    def start(self):
        if not self.on:
            return 0
        self.lap_idx += 1
        name = self.pfix + str(self.lap_idx)
        self.hist[name] = [time.time(), None]
        return self.hist[name]

    def lap(self):
        if not self.on:
            return 0
        # check if there exists half-done lap
        tmptime = time.time()
        key = list(self.hist.keys())[-1]
        if self.hist[key][1] is None:
            # start-lap mode
            self.hist[key][1] = tmptime
            name = key
        else:
            # lap-lap mode
            self.lap_idx += 1
            name = self.pfix + str(self.lap_idx)
            self.hist[name] = [self.hist[key][1], tmptime]
        # self.hist[name] = time.time()
        if self.timebgt is None:
            res = self.hist[name]
        else:
            stime = list(self.hist.values())[0][0]
            res = self.timebgt - (tmptime - stime)
            if res <= 0 and self.raise_err:
                raise TimeLimitException
        return res

    # histType: 0: absolute times; 1: relative times; 2: time lapse
    # the first two are dictionary of lists; 2 is a dictionary
    def info(self, histType=1):
        if not self.on:
            return 0
        if histType == 0:
            if self.digits is not None:
                keys = list(self.hist)
                res = {keys[i]: [round(self.hist[keys[i]][0], self.digits), 
                                 round(self.hist[keys[i]][1], self.digits)] for i in range(len(keys))}
            else:
                res = self.hist
        elif histType == 1:
            stime = list(self.hist.values())[0][0]
            keys = list(self.hist)
            if self.digits is not None:
                res = {keys[i]: [round(self.hist[keys[i]][0] - stime, self.digits), 
                                 round(self.hist[keys[i]][1] - stime, self.digits)] for i in range(len(keys))}
            else:
                res = {keys[i]: [self.hist[keys[i]][0] - stime,
                                 self.hist[keys[i]][1] - stime] for i in range(len(keys))}
        else:
            keys = list(self.hist)
            if self.digits is not None:
                res = {keys[i]: round(self.hist[keys[i]][1] - self.hist[keys[i]][0], self.digits) for i in range(len(keys))}
            else:
                res = {keys[i]: self.hist[keys[i]][1] - self.hist[keys[i]][0] for i in range(len(keys))}
        return res

    # get total time
    def total_time(self):
        stime = list(self.hist.values())[0][0]
        etime = list(self.hist.values())[-1][1]
        res = etime - stime
        if self.digits is not None:
            res = round(res, self.digits)
        return res


def main():
    import numpy as np
    sw = Stopwatch()
    iters = 6
    gaps = np.random.random(iters) * 5
    print(gaps)
    # sw.init(start=True, name='round')
    sw.init(start=False)
    for i in range(iters):
        time.sleep(1)
        sw.start()
        time.sleep(gaps[i])
        sw.lap()
    print(sw.info(0))
    print(sw.info(1))
    print(sw.info(2))


if __name__ == '__main__':
    main()
