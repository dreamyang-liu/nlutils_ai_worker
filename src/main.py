from AIWorkerSocket import AIWorkerSocketStore


worker = AIWorkerSocketStore('127.0.0.1', 22105)
worker.bind()
worker.run()