from aiohttp import web
import random
import asyncio
import aiohttp
from datetime import datetime

M = 1000
reqReceived = 0
rezRes = 0
randInt = random.randint(5, 10)
workers = {"worker" + str(id): [] for id in range(1, randInt + 1)}
routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		global randInt, workers, M, reqReceived, rezRes

		reqReceived += 1

		current_date_and_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print("[",current_date_and_time,"]", "Request recieved. Received total of",reqReceived, "requests")

		data = await request.json()
		pyCodeLength = len(data["pyCode"])
		code = "\n".join(data["pyCode"])
		code = code.split("\n")
		data["pyCode"] = ["\n".join(code[i:i+M]) for i in range(0, len(code), M)]

		tasks = []
		results = []

		async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
			currentWorker = 1
			for i in range(len(data["pyCode"])):
				task = asyncio.create_task(
					session.get(f"http://127.0.0.1:{8080 + currentWorker}/", json = { "id": data["client"], "data": data["pyCode"][i] })
				)
				tasks.append(task)
				workers["worker" + str(currentWorker)].append(task)
				currentWorker = 1 if currentWorker == randInt else currentWorker + 1

			results = await asyncio.gather(*tasks)
			results = [await result.json() for result in results]
			results = [result.get("wordsNumber") for result in results]

		rezRes += 1
		current_date_and_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print("[",current_date_and_time,"]","Response sent. Sent total of", rezRes ,"responses")

		avgNumOfWords = round(sum(results) / pyCodeLength, 2)
		return web.json_response({"name": "master", "status": "OK", "client": data["client"], "avgNumOfWords": avgNumOfWords})
	except Exception as e:
		return web.json_response({"name": "master", "error": str(e)})

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8080)