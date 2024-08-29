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
from meutils.io.image import image_to_base64

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

    if request.picInfo2.startswith('http'):
        request.picInfo2 = image_to_base64(request.picInfo2)

    payload = request.model_dump()

    headers = {
        # 'X-Requested-With': 'XMLHttpRequest',
        'Cookie': token,
        # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers, timeout=100) as client:
        response = await client.post('/aigc/pccreate', data=payload)

        logger.debug(response.status_code)
        logger.debug(response.text)

        if response.is_success:
            data = response.json()
            if "pcEditTaskid" not in data:
                send_message(f"照片失败\n{request.original_url}")
                raise Exception("无法处理该照片，可联系管理员")

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


async def get_task(
        task_id,
        token: Optional[str] = None,
        response_format: Optional[Literal["url", "b64_json"]] = None
):
    task_id = task_id.split("-", 1)[-1]

    params = {
        "taskId": task_id
    }
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:
        response = await client.get('/aigc/pcquery', params=params)
        data = response.json()

        if response_format == "url":
            for arr in data.get('picArr', []):
                from meutils.io.image import base64_to_url
                if base64_string := arr.pop('src', None):
                    data['url'] = await base64_to_url(base64_string)

        return data


if __name__ == '__main__':
    from meutils.io.image import image_to_base64

    url = "https://oss.ffire.cc/files/kling_watermark.png"
    url = "https://env-00jxgna201cb.normal.cloudstatic.cn/ori/tmp_dc12fc648ab10c4b8d310f3e8645781278e556a0264836d7fdb806c6bb83c493.jpeg"

    # 涂抹消除
    # url = "https://env-00jxgna201cb.normal.cloudstatic.cn/ori/tmp_dc12fc648ab10c4b8d310f3e8645781278e556a0264836d7fdb806c6bb83c493.jpeg"
    # url_ = "https://env-00jxgna201cb.normal.cloudstatic.cn/water/tmp_2954a8d96011173a7f2b6baad8cc28317278e368d1393ca6.jpg"
    # picInfo2 = image_to_base64(url_)
    #
    # request = BDAITPZSRequest(original_url=url, thumb_url=url, picInfo2=picInfo2, type='8')

    request = BDAITPZSRequest(original_url=url, thumb_url=url)

    # arun(create_task(request, is_async=True))

    arun(get_task('cr84hhue1pn8m151of3g', response_format='url'))
