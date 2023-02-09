import asyncio
import aiohttp
import pandas as pd

print("Just wait...")
clientID = [i for i in range(1, 10001)]
data = pd.read_json("fakedataset.json", lines = True)
print("Fakedataset loaded")

clientRow = int(len(data) / len(clientID)) #TypeError: cannot do positional indexing on RangeIndex with these indexers [0.0] of type float

clients = {id:[] for id in clientID}

for id in clientID:
	content = clients[id]
	start = (id - 1) * clientRow
	end = start + clientRow
	selected_rows = data.iloc[start:end]
	for index, row in selected_rows.iterrows():
		content.append(row["content"])

async def request():
	tasks = []
	global results
	results = []
	async with aiohttp.ClientSession(connector = aiohttp.TCPConnector(ssl = False)) as session:
		for id, content in clients.items():
			task = asyncio.create_task(session.get("http://127.0.0.1:8080/", json = { "client": id, "pyCode": content }))
			tasks.append(task)
		print("Data sent. Please wait...")
		results = await asyncio.gather(*tasks)
		results = [await x.json() for x in results]

run = asyncio.get_event_loop()
run.run_until_complete(request())

for result in results:
	if result.get("client") is not None:
		print("Average number of letters for client ID:", result["client"], "=", result["avgNumOfWords"])