import subprocess
import os
import re
from idlelib.iomenu import encoding
from typing import Optional,List,Union
from pathlib import Path

def echarts_ssr(width, height, option_list:List[str])->Optional[List[str]]:
    """
    使用ECharts SSR（服务器端渲染）生成SVG图像的字符串。

    此函数通过调用Node.js脚本实现ECharts的服务器端渲染，该Node.js脚本是echarts-ssr库的一部分。
    它将指定的宽度、高度和选项传递给脚本，以生成SVG格式的图表。

    参数:
    - width: 图像的宽度。
    - height: 图像的高度。
    - options: ECharts的配置选项集合，传入的变量必须是一个可迭代的数组或者列表。

    返回:
    - 一个包含SVG图像字符串的列表，如果渲染过程中发生错误，则返回None。
    """

    # 获取当前文件的路径，用于定位Node.js脚本。
    file_path = Path(__file__)
    # 构建Node.js脚本的路径。
    script_path = file_path.parent.joinpath('echarts_ssr.mjs')
    # 获取脚本的绝对路径，以便在命令行中使用。
    mjs = script_path.absolute().__str__()

    # 调用Node.js脚本，传递宽度、高度和选项参数。
    # capture_output=True表示捕获脚本的输出，text=True确保以文本模式运行命令，encoding='utf8'指定字符编码。
    result = subprocess.run(['node', mjs, str(width), str(height), *option_list], capture_output=True, text=True, encoding='utf8')

    # 检查Node.js脚本是否成功执行。
    if result.returncode == 0:
        # 提取并清理脚本输出的SVG字符串。
        strs = result.stdout.strip()
        pattern = re.compile(r'<svg.*?</svg>',re.DOTALL)
        return pattern.findall(strs)
    else:
        # 如果脚本执行失败，打印错误信息并返回None。
        print("error:", result.stderr)
        return None
