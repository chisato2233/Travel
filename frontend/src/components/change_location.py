# 读取文本文件
file_path = 'frontend/src/components/locations.js'  # 替换为你的文件路径
import os;
print(os.getcwd());
# 打开文件并处理每一行
with open(file_path, 'r') as file:
    lines = file.readlines()

# 在每一行加上单引号
quoted_lines = ["\"" + line.strip() + "\"," for line in lines]

# 将处理后的内容写回文件
output_path = 'output_file.js'  # 保存处理后的文件路径
with open(output_path, 'w') as output_file:
    output_file.write('\n'.join(quoted_lines))
