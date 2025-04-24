import json
import aiohttp
import asyncio

async def get_post(session, pid):
    url = "https://winry.khashaev.ru/posts/" + str(pid) 
    try:
        resp = await session.get(url)
        if resp.status == 200:
            data = await resp.json()  
            return data
        else:
            print(f"ID {pid} 404")  
            return None
    except Exception as e:
        print("error:",e)
        return None

def find_ids(node):
    id_list = [node["id"]]  
    for child in node["replies"]:
        id_list += find_ids(child)
    return id_list


def add_content(node, content_map):
    node["body"] = content_map.get(node["id"], "") 
    for child_node in node["replies"]:
        add_content(child_node, content_map)

async def main():
    
    input_json = input()
    data = json.loads(input_json)
    
    all_ids = find_ids(data)
    
    contents = {}
    i = 0
    async with aiohttp.ClientSession() as session:
        task_list = []
        for pid in all_ids:
            task = asyncio.create_task(get_post(session, pid))
            task_list.append(task)
        
        results = []
        for task in task_list:
            results.append(await task)
    
        i = 0
        while i < len(all_ids):
            pid = all_ids[i]
            res = results[i]
            if res is not None:
                contents[pid] = res.get("body", "") 
            i += 1
    
    add_content(data, contents)
    print(json.dumps(data, indent=2))


asyncio.run(main())