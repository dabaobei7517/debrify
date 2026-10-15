import os
import glob
from openai import OpenAI

# 使用兼容 OpenAI 接口的 API（如 DeepSeek / OpenAI / 各类 API 网关）
client = OpenAI(
    api_key=os.environ.get("API_KEY"),
    base_url=os.environ.get("BASE_URL", "https://api.openai.com/v1")
)

def translate_dart_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    prompt = """你是一个精通 Flutter/Dart 的本地化专家。
请将以下 Dart 代码中所有面向用户的英文 UI 字符串（包括 title, subtitle, label, Text, hintText, SnackBar, Dialog 等提示语）全部翻译为自然、准确的简体中文。
严格遵守以下规则：
1. 绝对不要修改任何变量名、函数名、类名、Key、路由名称或逻辑代码。
2. 保持原有的引号格式和字符串插值（如 $variable 或 ${expr}）完全不变。
3. 专有名词如 Real-Debrid, TorBox, AllDebrid, Trakt, Stremio, WebDAV, API Key 等保持英文或合理保留。
4. 只输出完整的、可直接编译的 Dart 源码，不要包含 ```dart 标记或任何解释文字。"""

    response = client.chat.completions.create(
        model=os.environ.get("MODEL_NAME", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ],
        temperature=0.1
    )
    
    translated = response.choices[0].message.content.strip()
    # 清理可能残留的 markdown 代码块标记
    if translated.startswith("```"):
        translated = "\n".join(translated.split("\n")[1:])
    if translated.endswith("```"):
        translated = "\n".join(translated.split("\n")[:-1])

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(translated)
    print(f"Translated: {filepath}")

# 扫描所有设置相关文件
files = glob.glob("lib/**/*setting*.dart", recursive=True) + glob.glob("lib/**/settings/**/*.dart", recursive=True)
for file in set(files):
    translate_dart_file(file)
