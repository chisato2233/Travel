import heapq
from collections import Counter, defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    # 为了在优先队列中使用，定义比较方法
    def __lt__(self, other):
        return self.freq < other.freq

# 构建哈夫曼树
def build_huffman_tree(text):
    frequency = Counter(text)
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)
    return priority_queue[0] if priority_queue else None



def generate_codes(node, prefix="", code={}):
    if node is not None:
        if node.char is not None:
            code[node.char] = prefix
        generate_codes(node.left, prefix + "0", code)
        generate_codes(node.right, prefix + "1", code)
    return code



def huff_compress(text):
    root = build_huffman_tree(text)
    codes = generate_codes(root)
    # 将原始文本转换为哈夫曼编码字符串
    encoded_text = ''.join(codes[char] for char in text)
    # 将比特字符串转换为字节序列
    padded_encoded_text = encoded_text + '0' * ((8 - len(encoded_text) % 8) % 8)
    byte_array = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        byte_array.append(int(byte, 2))
    return bytes(byte_array), codes

def huff_decompress(encoded_bytes, codes):
    # 翻转codes字典，以便使用编码查找字符
    reversed_codes = {v: k for k, v in codes.items()}
    encoded_text = ''.join(format(byte, '08b') for byte in encoded_bytes)
    decoded_text = ''
    current_code = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in reversed_codes:
            decoded_text += reversed_codes[current_code]
            current_code = ''
    return decoded_text

