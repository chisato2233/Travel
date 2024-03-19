def lz77_compress(text, window_size=4096, lookahead_buffer_size=16):
    i = 0
    result = []
    
    while i < len(text):
        # 初始化最长匹配长度和位置
        max_length = 0
        max_distance = 0
        buffer_end = min(i + lookahead_buffer_size, len(text))
        
        # 搜索窗口
        for j in range(max(0, i - window_size), i):
            length = 0
            while i + length < buffer_end and text[j + length] == text[i + length]:
                length += 1
                if length > max_length:
                    max_length = length
                    max_distance = i - j
        
        # 如果找到匹配，添加到结果
        if max_length > 0:
            result.append((max_distance, max_length, text[i + max_length]))
            i += max_length + 1
        else:
            result.append((0, 0, text[i]))
            i += 1
    
    return result




from collections import Counter, defaultdict
from heapq import heappush, heappop, heapify

def build_huffman_tree(text):
    # 统计字符出现频率
    frequency = Counter(text)
    # 使用频率创建优先队列（最小堆）
    heap = [[weight, [symbol, ""]] for symbol, weight in frequency.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

def huffman_decode(encoded_text, huffman_codes):
    # 反转霍夫曼编码表，从编码到字符
    reverse_huffman_codes = {v: k for k, v in huffman_codes.items()}
    decoded = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_huffman_codes:
            decoded += reverse_huffman_codes[current_code]
            current_code = ""
    return decoded

def lz77_decompress(lz77_encoded):
    decompressed = ""
    i = 0
    while i < len(lz77_encoded):
        # 由于简化示例中使用了字符编码，这里直接转换回整数
        distance = ord(lz77_encoded[i])
        length = ord(lz77_encoded[i + 1])
        next_char = lz77_encoded[i + 2]
        i += 3

        # 如果distance为0，表示没有重复字符串，直接添加next_char
        if distance == 0:
            decompressed += next_char
        else:
            # 否则，从已解压缩的文本中复制字符串
            start = len(decompressed) - distance
            decompressed += decompressed[start:start+length]
            decompressed += next_char

    return decompressed


def deflate_compress(text):
    lz77_result = lz77_compress(text)
    flat_lz77_result = ''.join([chr(distance) + chr(length) + next_char for distance, length, next_char in lz77_result])
    huffman_tree = build_huffman_tree(flat_lz77_result)
    huffman_codes = {char: code for char, code in huffman_tree}
    encoded_text = ''.join(huffman_codes[char] for char in flat_lz77_result)
    return encoded_text, huffman_codes

def deflate_decompress(encoded_text, huffman_codes):
    # 首先进行霍夫曼解码
    lz77_encoded = huffman_decode(encoded_text, huffman_codes)
    # 然后进行LZ77解码
    decompressed_text = lz77_decompress(lz77_encoded)
    return decompressed_text

