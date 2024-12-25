import requests
import json


def get_access_token(QIANFAN_ACCESS_KEY, QIANFAN_SECRET_KEY):
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={QIANFAN_ACCESS_KEY}&client_secret={QIANFAN_SECRET_KEY}'
    print(url)
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    access_token = response.json().get("access_token")
    return access_token


def single_main(course, comment, access_token='24.cf1f945ed80f4ed3699370d78afdd508.2592000.1737698654.282335-115433128'):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token

    payload = json.dumps({
        "system": """
        你是一个AI助教，根据学生的选修课程，结合他们的学习需求和问题，提供个性化的学习规划或解决方案。主要要求：

        1. **课程类型**：
           - 对于编程类课程（如Python、Web开发），给出代码示例和实践指导。
           - 对于理论类课程（如机器学习、算法），解释原理并提供案例。

        2. **回答风格**：
           - 清晰、简洁、易懂。
           - 鼓励学生独立思考，提供进一步学习的方向。

        3. **示例课程**：Python编程、数据分析、机器学习、深度学习、Web开发等。

        请根据学生的课程和问题，提供最佳的解决方案。
        """,
        "max_output_tokens": 512,
        "messages": [
            {
                "role": "user",
                "content": f"学生选择的课程是：{course}，提出的问题是：{comment}，请给出简洁的解答。"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    return result["result"]


if __name__ == '__main__':
    # QIANFAN_ACCESS_KEY = "..."
    # QIANFAN_SECRET_KEY = "..."
    # access_token = get_access_token(QIANFAN_ACCESS_KEY, QIANFAN_SECRET_KEY)
    access_token = '24.cf1f945ed80f4ed3699370d78afdd508.2592000.1737698654.282335-115433128'

    selected_course = "C++编程基础"
    student_question = "如何使用C++连接MySQL？能否提供代码示例？"

    res = single_main(selected_course, student_question, access_token)
    print(res)
