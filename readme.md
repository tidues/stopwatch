# A Simple Stopwatch for Timing Python Code

It works like a stop watch. An example:

    from stopwatch import Stopwatch
    import numpy as np

    sw = Stopwatch('test')  # a new stopwatch named test
    
    # randomly generate six waiting times within (0, 5)
    iters = 6
    gaps = np.random.random(iters) * 5

    sw.start()  # start the stopwath

    for i in range(iters):
        time.sleep(gaps[i])
        sw.lap('round' + str(i))  # lap the stopwatch with a name

    print(sw.getHist(0))  # get all lap info as absolute times
    print(sw.getHist(1))  # get all lap info as times relative to the starting time
    print(sw.getHist(2))  # get all lap info as durations
      