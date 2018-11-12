from multiprocessing.pool import ThreadPool
import threading
import time
import json
example = {
    'one': range(0,10),
    'two': range(10, 20),
    'three': range(20, 30),
    'four': range(40, 50),
    'five': range(50, 60)
}
output = {
	'one':[],
	'two':[],
	'three':[],
	'four':[],
	'five':[],
}

def with_thread():

	def worker(key):
		for num in example[key]:
			output[key].append({num: threading.current_thread().name})
			print( threading.current_thread())
			print (num)
			time.sleep(.1)

	pool = ThreadPool(3)

	pool.map(worker, (example.keys()))

	pool.close()
	pool.join()

def without_thread():
	for key in example:
		for num in example[key]:
			output[key].append({num: 'asdf'})
			time.sleep(1)


s = time.time()
with_thread()
# print(time.time() - s)
# print(json.dumps(output, indent=4))

# output = {
# 	'one':[],
# 	'two':[],
# 	'three':[],
# 	'four':[],
# 	'five':[],
# }
# s = time.time()
# without_thread()
# print(time.time() - s)