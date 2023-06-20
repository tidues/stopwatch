import time
from datetime import datetime
from dateutil import tz


# get datetime string
# fmt: format 'short' or 'long'
def dtstr(local=False, fmt='short'):
    if fmt == 'short':
        fmt_str = "%m%d%Y%H%M%S"
    else:
        fmt_str = "%Y-%m-%d %H:%M:%S"
    if local:
        zone = tz.tzlocal()
    else:
        zone = tz.tzutc()
    now = datetime.now(zone)
    return now.strftime(fmt_str), now


class TimeLimitException(Exception):
    def __init__(self, message="Out of time limit"):
        self.message = message
        super().__init__(self.message)


class Stopwatch:
    def __init__(self, digits=None, on=True, timebgt=None, raise_err=False, start=False, name=None):
        self.timebgt = timebgt
        self.raise_err = raise_err
        self.on = on
        self.stime = None
        self.hist = {}
        self.digits = digits
        self.lap_idx = 0
        if start:
            self.init(start=True, name=name)

    def init(self, start=False, name=None):
        if not self.on:
            return 0
        self.lap_idx = 0
        self.stime = None
        self.hist = {}
        if name is None:
            self.pfix = 'lap'
        else:
            self.pfix = name
        if start:
            return self.start()

    def start(self):
        if not self.on:
            return 0
        self.lap_idx += 1
        name = self.pfix + str(self.lap_idx)
        self.stime = time.time()
        self.hist[name] = [self.stime, None]
        return self.hist[name]

    # res_type: 0[default]: current time; 1: lap_time; 2: time from start; 3: current history
    def lap(self, res_type=0, lapname=None):
        if not self.on:
            return 0
        # check if there exists half-done lap
        tmptime = time.time()
        key = list(self.hist.keys())[-1]
        if self.hist[key][1] is None:
            # start-lap mode
            self.hist[key][1] = tmptime
            if lapname is None:
                name = key
            else:
                name = lapname
                # update key name
                self.hist[name] = self.hist[key]
                del self.hist[key]
        else:
            # lap-lap mode
            self.lap_idx += 1
            if lapname is None:
                name = self.pfix + str(self.lap_idx)
            else:
                name = lapname
            self.hist[name] = [self.hist[key][1], tmptime]
        # self.hist[name] = time.time()
        if self.timebgt is None:
            if res_type == 1:
                res = self.hist[name][1] - self.hist[name][0]
            elif res_type == 2:
                res = self.hist[name][1] - self.stime
            elif res_type == 3:
                res = self.hist[name]
            else:
                res = tmptime
        else:
            stime = list(self.hist.values())[0][0]
            res = self.timebgt - (tmptime - stime)
            if res <= 0 and self.raise_err:
                raise TimeLimitException
        return res

    # histType: 0: absolute times; 1: relative times; 2: time lapse
    # the first two are dictionary of lists; 2 is a dictionary
    def info(self, histType=1, withKey=True):
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
            stime = self.stime
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

        if withKey is False:
            res = list(res.values())
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
    # sw.init(start=True, name='round')
    sw.init(start=False)
    for i in range(iters):
        time.sleep(1)
        sw.start()
        time.sleep(gaps[i])
        sw.lap()
    print('info0:', sw.info(0))
    print('info1:', sw.info(1))
    print('info2:', sw.info(2))


if __name__ == '__main__':
    main()
