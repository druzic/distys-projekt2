from aiohttp import web
import random
import asyncio
import string

routes = web.RouteTableDef()

@routes.get("/")
async def function(request):
	try:
		sleep_time = random.uniform(0.1, 0.3)
		await asyncio.sleep(sleep_time)
		data = await request.json()
		words = data.get("data").translate(str.maketrans("", "", string.punctuation)).split()
		wordsNumber = len(words)
		await asyncio.sleep(sleep_time)

		return web.json_response({"name": "W6", "wordsNumber": wordsNumber})
	except Exception as e:
		return web.json_response({"name": "W6", "error": str(e)})

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port = 8087)