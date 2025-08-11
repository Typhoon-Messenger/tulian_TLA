import requests
import json
import time

# 这是一款计算交通灯作业包的小工具，挨个访问作业包下的每一帧来获取标注框数
# 适用于 4V图新的标注平台
# 作者：IMCRY

headers = {
    'appId':'10001',
    'Origin': 'http://ads-mark.navinfo.com',
    'Referer': 'http://ads-mark.navinfo.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Cookie':'替换cookie'   # 需要修改
}
op_headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Access-Control-Request-Headers': 'appid',
    'Access-Control-Request-Method': 'GET',
    'Connection': 'keep-alive',
    'Host': 'ads-gw.navinfo.com',
    'Origin': 'http://ads-mark.navinfo.com',
    'Referer': 'http://ads-mark.navinfo.com/',
    'Sec-Fetch-Mode': 'cors',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36}'
}

def send_work():
    url = 'http://ads-gw.navinfo.com/heartbeat/api/v1/working'
    param = {
        'stage':'browse',
        'task_id':None,
        'type':'dot'
    }
    try:
        requests.post(url=url,headers=headers,params=param)
        print('发送工作状态成功')
    except:
        return

def GetTaskCode():
    url = 'http://ads-mark.navinfo.com/task/work_center/editor_tools.html#/browse'
    param = {
        'task_id':644489968
    }
    res = requests.get(url=url,headers=headers,params=param)
    print(res.raw.read)

def GetFramesList():
    send_work()
    url = "http://ads-gw.navinfo.com/taskflow/api/v1/task/get_info"
    global task_code
    task_code = 'XH2TLA605591485899038734'
    param = {
        'task_code':task_code
    }

    global json_result_data
    try:
        # requests.options(url=url,headers=op_headers,params=param)
        res = requests.get(url=url,headers=headers,params=param)
        json_result_data = json.loads(res.text)['result_data']
        print('帧列表获取成功')
    except:
        json_result_data = {}

def GetCountBox():
    if json_result_data == {}:
        print("获取帧列表失败！！")
        return
    send_work()
    url = 'http://ads-gw.navinfo.com/annosys/api/v1/annotation/workflow/query'
    
    count_list = []
    for x in json_result_data:
        param = {}
        sampleId = x['sampleId']
        index = x['index']
        workflowNodeId = x['workflowNodeId']
        param = {
        'ids':int(sampleId),
        'nodeIds':int(workflowNodeId)
                }

        try:
            # requests.options(url=url,headers=op_headers,params=param,timeout=3)
            time.sleep(0.5)
            res = requests.get(url=url,headers=headers,params=param,timeout=3)
            json_1 = json.loads(res.text)
            count_1 = len(json_1['data'][0]['datas'][0]['annotations']['geometry'])
            print('*'*8)
            count_list.append(count_1)
            print(f"第{index}帧共有 {count_1} 个框")
        except requests.exceptions.Timeout as e:
            print(f"获取第{index}帧数据超时，正在重新获取...")
            time.sleep(0.5)
            try:
                res = requests.get(url=url,headers=headers,params=param,timeout=3)
                json_1 = json.loads(res.text)
                count_1 = len(json_1['data'][0]['datas'][0]['annotations']['geometry'])
                print('*'*30)
                count_list.append(count_1)
                print(f"第{index}帧共有 {count_1} 个框")
            except:
                continue
        except Exception as e:
            print('第 ',index,'帧 获取框数失败:',e)
            
    sum_count = sum(count_list)
    print(f"任务[{task_code}] 有 {sum_count} 个框")

if __name__ == '__main__':
    # GetTaskCode()
    GetFramesList()
    GetCountBox()