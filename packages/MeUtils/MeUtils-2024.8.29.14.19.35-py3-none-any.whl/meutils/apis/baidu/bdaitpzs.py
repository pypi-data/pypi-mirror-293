#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : image_tools
# @Time         : 2024/8/28 13:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *
from meutils.config_utils.lark_utils import get_spreadsheet_values, get_next_token_for_polling
from meutils.schemas.openai_types import ImageRequest, ImagesResponse
from meutils.apis.translator import deeplx
from meutils.decorators.retry import retrying
from meutils.schemas.image_types import ASPECT_RATIOS
from meutils.oss.minio_oss import Minio
from meutils.decorators.contextmanagers import try_catcher
from meutils.schemas.baidu_types import BDAITPZSRequest
from meutils.schemas.task_types import Task, TaskType

from meutils.notice.feishu import send_message as _send_message

BASE_URL = "https://image.baidu.com"

url = "https://image.baidu.com/aigc/pccreate"

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/GYCHsvI4qhnDPNtI4VPcdw2knEd?sheet=jrWhAS"

send_message = partial(
    _send_message,
    title=__name__,
    url="https://open.feishu.cn/open-apis/bot/v2/hook/dc1eda96-348e-4cb5-9c7c-2d87d584ca18"
)
async def create_task(request: BDAITPZSRequest, token: Optional[str] = None, is_async: bool = True):
    token = token or await get_next_token_for_polling(feishu_url=FEISHU_URL)
    payload = request.model_dump()

    headers = {
        # 'X-Requested-With': 'XMLHttpRequest',
        'Cookie': token,
        # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post('/aigc/pccreate', data=payload)
        if response.is_success:
            data = response.json()
            if is_async:
                # {
                #     "status": 0,
                #     "pcEditTaskid": "cr7sbuue1pnfd61bjgu0",
                #     "resType": 0,
                #     "timestamp": "1724892667",
                #     "token": "e668cb4457494351f65300d9f388bb2b"
                # }

                task_id = f"{TaskType.pcedit}-{data['pcEditTaskid']}"
                return Task(id=task_id, data=data, system_fingerprint=token)

            else:  # {'algoprocess': 0, 'isGenerate': False, 'progress': 4}
                logger.debug(data)
                task_id = data['pcEditTaskid']
                url = f"https://image.baidu.com/aigc/pcquery?taskId={task_id}"
                for i in range(10):
                    await asyncio.sleep(3)
                    with try_catcher():
                        response = await client.get(url)
                        data = response.json()
                        logger.debug(f"progress: {data['progress']}")

                        if data['isGenerate']:
                            return data


async def get_task(task_id, token: Optional[str] = None):  # 目前不需要token
    task_id = task_id.split("-", 1)[-1]

    params = {
        "taskId": task_id
    }
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:
        response = await client.get('/aigc/pcquery', params=params)
        return response.json()


if __name__ == '__main__':
    arun(create_task('URL_ADDRESS', is_async=False))

    # arun(get_task('cr7s8v6e1pnfd61bj8vg'))
