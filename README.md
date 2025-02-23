# XinYu
XinYu -《新语》目标为尝试整理编辑自2000年以来中文文化圈、中文互联网上出现的汉语新词汇、新俗语、或本意被翻新后再次大规模流行的“成语”，流行词，汇集成典，以供读者参考，或做汉语言文字学研究材料用。比如人从众𠈌，喜大普奔，不明觉厉，十动然拒等新式“成语”，内卷，破防，灌水，真香，吃瓜群众，图样图森破，YYDS，凡尔赛，新质生产力等汉语新词汇。

# 最新版本
[《新语小辞典》v0.01.md](./辞典输出目录/《新语小辞典》v0.01.md)  
[《新语小辞典》v0.01.pdf](./辞典输出目录/《新语小辞典》v0.01.pdf)  
[《新语小辞典》v0.01.html](./辞典输出目录/《新语小辞典》v0.01.html)  

# 开发过程

## 基本命令
- 根据已分类好过的Markdown词条列表生成最终的辞典文件。切换到仓库根目录后执行以下Python命令，即可生成《新语小辞典》v0.01版本对应的单个文件，包含Markdown, HTML, PDF三种格式。
```python
# Pandoc PDF 文件格式生成尚有很多问题未能解决
# 脚本中临时跳过了生成PDF部分
# 采用VScode Markdown to PDF插件临时生成
python3 脚本文件/generate_the_dictionary.py
```

- 根据已整理过的模型输出文件，生成分类后的词条文件
```python
python3 脚本文件/llm_output_to_sorted_items.py
```
