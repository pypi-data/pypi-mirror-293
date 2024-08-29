# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_chatpdf']

package_data = \
{'': ['*']}

install_requires = \
['faiss-cpu>=1.7.3,<2.0.0',
 'nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0',
 'numpy>=1.24.2,<2.0.0',
 'openai>=1.30.1,<2.0.0',
 'pymupdf>=1.21.1,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-chatpdf',
    'version': '1.0.0',
    'description': 'A nonebot plugin for chatpdf',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-chatpdf\n\n</div>\n\n# 介绍\n\n- 本插件灵感来源于最近很火的 [chatpdf](https://www.chatpdf.com)。\n- 将需要分析的论文/阅读材料上传到群文件，机器人可以对其进行存储分析，然后你可以向其提问有关文章内容、文章概要、对于文章的思考等问题\n- 本插件参考和使用了项目 [Document_QA](https://github.com/fierceX/Document_QA) 中的核心代码\n- 本插件可选使用OneAPI格式的第三方中转站也可以使用OpenAI官方接口，但是在速率限制的情况下本插件可能无法使用。\n\n# 效果\n使用方法以最新说明为主\n\n![Alt](./img/img2.jpg)\n\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_chatpdf.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-chatpdf"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-chatgpt-chatpdf\n  ```\n\n# 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n\n```\noneapi_key = "sk-xxxxxxxxxx"  # （必填）OpenAI官方或者是支持OneAPI的大模型中转服务商提供的KEY\noneapi_url = "https://xxxxxxxxx"  # （可选）大模型中转服务商提供的中转地址,使用OpenAI官方服务不需要填写\noneapi_model = "gpt-4" # （可选）使用的语言大模型\n```\n\n\n# 使用方法\n\n如果设置了nonebot全局触发前缀，需要在下面的命令前加上设置的前缀。\n\n### 使用方式：上传需要分析的pdf文件到群文件中\n\n- 分析pdf (使用该命令以上传pdf文件的方式启动chatpdf文章分析功能)\n- 在一分钟内，上传需要分析的pdf文件到群文件中，分析完成后会返回成功信息\n- askpdf (文章分析完成后，使用该命令后面接需要提问的关于文章的问题，机器人会给出答案)\n- 删除所有pdf (删除所有缓存)\n- 删除我的pdf （删除用户在本群的缓存）\n\n\n# 注意事项\n\n- 每次调用```分析pdf```命令时，都会清除调用者以前的分析缓存\n\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@bupt.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
