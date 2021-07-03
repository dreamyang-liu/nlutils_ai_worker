from AIWorkerSocket import AIWorkerSocketStore


x = AIWorkerSocketStore('127.0.0.1', 22005)
x.connect()
x.run()