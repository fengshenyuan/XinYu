import os
import pypandoc


def get_markdown_files(root_dir):
    """
    递归获取指定目录下所有 Markdown 文件 (.md) 的路径。
    返回一个包含文件路径的列表。
    """
    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    return markdown_files


def combine_markdown_content(markdown_files, output_md_path):
    """
    读取并合并多个 Markdown 文件的内容。
    返回合并后的 Markdown 文本字符串。
    """
    combined_content = ""
    for filepath in markdown_files:
        with open(filepath, "r", encoding="utf-8") as f:
            combined_content += f.read()
            combined_content += "\n"

    with open(output_md_path, "w") as outf:
        outf.write(combined_content)
    return combined_content


def convert_markdown_to_html(markdown_content, output_html_path):
    """
    使用 Pandoc 将 Markdown 内容转换为 HTML 文件。
    """
    try:
        html_body = pypandoc.convert_text(markdown_content, "html", format="md")
        with \
            open("./脚本文件/resources/html_style_header.html") as hf, \
            open("./脚本文件/resources/html_style_footer.html") as ff, \
            open(output_html_path, "w") as html_out_file:
                html_output = "".join([hf.read(), html_body, ff.read()])
                html_out_file.write(html_output)
        print(f"HTML 文件已成功生成: {output_html_path} (使用 pypandoc)")
    except Exception as e_all:
        raise Exception(f"HTML 转换过程中发生错误: {e_all}") from e_all


def convert_markdown_to_pdf(markdown_content, output_pdf_path):
    """
    使用 Pandoc 将 Markdown 内容转换为 PDF 文件。
    """
    try:
        pypandoc.convert_text(markdown_content, "pdf", format="md", outputfile=output_pdf_path, extra_args=[
            "--pdf-engine", "xelatex", "--variable", 'mainfont="SFNS"'
        ])
        print(f"PDF 文件已成功生成: {output_pdf_path} (使用 pypandoc)")
    except Exception as e_all:
        raise Exception(f"PDF 转换过程中发生错误: {e_all}") from e_all


if __name__ == "__main__":
    root_directories = [
        "./1 单字词",
        "./2 双字词",
        "./3 三字词",
        "./4 四字词",
        "./5 四字以上",
    ]
    CURRENT_VERSION = "v0.01"
    output_md_file_path = f"./辞典输出目录/《新语小辞典》{CURRENT_VERSION}.md"
    output_pdf_file_path = f"./辞典输出目录/《新语小辞典》{CURRENT_VERSION}.pdf"
    output_html_file_path = f"./辞典输出目录/《新语小辞典》{CURRENT_VERSION}.html"

    try:
        print("开始查找 Markdown 文件...")
        all_md_files = []
        for root_dir in root_directories:
            markdown_files = sorted(get_markdown_files(root_dir))
            if not markdown_files:
                print("未找到任何 Markdown 文件。请检查目录结构。")
            else:
                all_md_files += markdown_files

        print(f"找到 {len(markdown_files)} 个 Markdown 文件。")
        print("开始合并 Markdown 文件内容...")
        combined_content = combine_markdown_content(all_md_files, output_md_file_path)
        print(f"所有操作完成。合并后的 Markdown 文件已保存为: {output_md_file_path}")
        print("开始将 Markdown 转换为 HTML...")
        convert_markdown_to_html(combined_content, output_html_file_path)
        print(f"所有操作完成。合并后的 HTML 文件已保存为: {output_html_file_path}")
        print("开始将 Markdown 转换为 PDF...")
        # Pandoc PDF 文件格式生成尚有很多问题未能解决，暂时跳过，采用VScode Markdown to PDF插件临时生成
        # convert_markdown_to_pdf(combined_content, output_pdf_file_path)
        print(f"所有操作完成。合并后的 PDF 文件已保存为: {output_pdf_file_path}")
    except Exception as e:
        print(f"发生错误: {e}")
        print("请检查错误信息并重试。确保 Pandoc 已安装并可在命令行中访问。")
