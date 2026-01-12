import json
import re
import requests
import os

# 下载 domain_regex.json 文件
def download_domain_regex(url, local_file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，抛出异常
        with open(local_file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"下载成功: {local_file_path}")
    except Exception as e:
        print(f"下载失败: {e}")

# 修复 domain_regex.json 文件的主程序
def fix_domain_regex(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 遍历所有的 domain_regex 规则
        for rule in data.get("rules", []):
            if "domain_regex" in rule:
                rule["domain_regex"] = [
                    clean_regex(regex) for regex in rule["domain_regex"]
                ]
        
        # 保存修复后的 json 数据到原文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("修复完成，domain_regex.json 已更新！")
    
    except Exception as e:
        print(f"错误：{e}")

# 清理每条正则表达式
def clean_regex(regex):
    # 删除所有不必要的空格
    regex = regex.strip()

    # 修复可能存在的转义字符问题，确保所有反斜杠都正确
    regex = re.sub(r"\\", "\\\\", regex)
    
    # 其他自定义修复规则
    # 例如：添加缺失的 ^ 和 $ 来确保正则表达式的起始和结束匹配
    if not regex.startswith("^"):
        regex = "^" + regex
    if not regex.endswith("$"):
        regex = regex + "$"
    
    return regex

# 主执行程序
if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/jackszb/domain_regex/main/domain_regex.json"  # domain_regex.json 文件链接
    local_file_path = "domain_regex.json"  # 假设文件保存在当前目录

    # 下载文件
    download_domain_regex(url, local_file_path)

    # 修复文件
    if os.path.exists(local_file_path):
        fix_domain_regex(local_file_path)
    else:
        print(f"错误：找不到文件 {local_file_path}")
