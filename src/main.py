from AIWorkerSocket import AIWorkerSocketStore


worker = AIWorkerSocketStore()
worker.bind()
worker.run()