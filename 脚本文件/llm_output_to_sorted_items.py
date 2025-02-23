import os
import re
import argparse

splitter = r"<!-- 作者 "


def split_markdown_by_entry(markdown_file_path, output_dir):
    """
    将 Markdown 文件按词条分割成多个文件，并按词条字数分类保存到子目录。

    Args:
        markdown_file_path (str): 输入 Markdown 文件的路径。
        output_dir (str): 输出文件存放的根目录。
    """

    try:
        with open(markdown_file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print(f"错误：文件未找到: {markdown_file_path}")
        return
    except Exception as e:
        print(f"读取文件时发生错误: {e}")
        return
    else:
        print(f"读取文件: {markdown_file_path} 成功")

    # 使用 '<!-- 作者 ' 分割 Markdown 内容
    entries = re.split(splitter, markdown_content)

    # 确保输出根目录存在，如果不存在则创建
    os.makedirs(output_dir, exist_ok=True)

    # 字数分类的子目录名称映射
    subdir_map = {
        1: "1 单字词",
        2: "2 双字词",
        3: "3 三字词",
        4: "4 四字词",
        5: "5 四字以上",  #  5 字及以上都归为 "5 字以上"
    }

    # 遍历分割后的词条内容 (跳过分割后的第一个空字符串)
    for entry_content in entries[1:]:
        if not entry_content.strip():  # Skip empty entries
            continue

        original_entry_content = splitter + entry_content
        
        # 提取词条名称作为文件名
        entry_lines = [r for r in original_entry_content.strip().split("\n") if r.strip()]
        if not entry_lines:
            continue

        #  使用更健壮的方式提取词条名
        entry_name = entry_lines[1].split('###')[1].strip()
        if not entry_name:
            print(f"警告: 无法从以下内容中提取词条名，已跳过:\n{entry_lines[1]}")
            continue

        # 计算词条名称的字数 (中文)
        entry_word_count = len(entry_name)

        # 确定子目录名称
        if entry_word_count <= 4:
            subdir_name = subdir_map.get(
                entry_word_count, "未知字数"
            )  # 理论上不会出现 "未知字数"
        else:
            subdir_name = subdir_map[5]  # 5 字及以上都归为 "5 字以上"

        #  创建子目录 (如果不存在)
        entry_subdir_path = os.path.join(output_dir, subdir_name)
        os.makedirs(entry_subdir_path, exist_ok=True)

        filename = f"{entry_name}.md"
        output_file_path = os.path.join(
            entry_subdir_path, filename
        )  #  文件保存到子目录中

        # 写入词条内容到单独的文件
        try:
            with open(output_file_path, "w", encoding="utf-8") as outfile:
                # "  \n" 换行前双空格触发Markdown紧凑换行效果
                outfile.write("  \n".join(entry_lines) + "  \n")  # 重新组织输出内容
            print(f"已创建文件: {output_file_path}")
        except Exception as e:
            print(f"写入文件时发生错误: {output_file_path} - {e}")


if __name__ == "__main__":
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(
        description="将 Markdown 文件按词条分割成多个文件，并按词条字数分类保存。"
    )

    # 添加命令行参数
    parser.add_argument(
        "-i", 
        "--input_path", 
        default="./基本工作目录/模型输出原始词条文件",
        help="输入 Markdown 文件路径，默认为原始词条文件目录下的文件 (回收站的文件会被忽略)"
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        default="./",
        help="输出文件存放的根目录，默认为当前目录",
    )

    # 解析命令行参数
    args = parser.parse_args()

    input_path = args.input_path  #  变量名改为 input_path 更通用
    output_directory = args.output_dir

    if os.path.isdir(input_path): # 判断输入路径是否为目录
        print(f"输入路径为目录: {input_path}\n")
        for root, _, files in os.walk(input_path): # 遍历目录及其子目录
            for file in files:
                if file.lower().endswith(".md"): # 检查文件是否为 Markdown 文件
                    markdown_file_path = os.path.join(root, file) # 构建完整的文件路径
                    if "回收站" in markdown_file_path: 
                        print(f"已跳过处理文件: {markdown_file_path}")
                        continue
                    else:
                        print(f"开始处理 Markdown 文件: {markdown_file_path}")
                    split_markdown_by_entry(markdown_file_path, output_directory) # 调用处理函数
                    print(f"处理 Markdown 文件成功: {markdown_file_path}\n")
    elif os.path.isfile(input_path): # 判断输入路径是否为文件
        print(f"输入路径为文件: {input_path}")
        split_markdown_by_entry(input_path, output_directory) # 直接处理单个文件
    else:
        print(f"错误：输入路径 '{input_path}' 不是有效的文件路径或目录。")

    print(f"\n分割完成，文件已按词条字数分类保存到 '{output_directory}' 目录中。")
