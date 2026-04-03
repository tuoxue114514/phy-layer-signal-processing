from gnuradio import gr
import numpy as np

class gold_sequence_insertion(gr.basic_block):
    """Gold序列插入模块
    在QPSK映射之后，每512长度的载荷数据前添加1024长度的Gold序列
    Gold序列格式：双极性序列（1和-1）
    帧结构：1024长度Gold序列 + 512长度载荷数据
    """
    
    def __init__(self):
        gr.basic_block.__init__(self,
            name="gold_sequence_insertion",
            in_sig=[np.complex64],
            out_sig=[np.complex64])
        
        # 提供的Gold序列（二进制）
        self.gold_sequence_binary = '0001111000101110100001011001110011101111111001011100000001111011001101001011011101101101110111100011010010110101010001001010010110010000110001110011010010111011010010000010000100100011011010010100001101001011000100010110010100101101100000100011110101001000011011111001111011010000110011001101010101011001111101110101011111011111000000010000011001010001001011101011101001110000101111000101101000001101011110111000011000011100101110110000111001000101110011001101110011001001110101100110101100110110001101101101111100101001000111010111111001011100001001101100000100110100011011110001001001001110001111001000110011011010110101001011111011110101101000111001011110011010000000001001011110110101000000101101010010110100101111100001101110100000011101010001000100011101001111101010111111111111000000110011011111001111001010101000001010010100100111110110010011110001000000000011000110100010001100111111001001010000111010000001100000011101001000111111111110000001011000101001011011000010111110110110000101101001001001111100010011111100'
        
        # 将二进制Gold序列转换为双极性序列（1和-1）
        self.gold_sequence = np.array([1 if bit == '1' else -1 for bit in self.gold_sequence_binary], dtype=np.complex64)
        
        # 验证Gold序列长度是否为1024
        if len(self.gold_sequence) != 1024:
            raise ValueError("Gold序列长度必须为1024")
        
        # 载荷数据长度
        self.payload_length = 512
        
        # 缓存数据
        self.buffer = []
    

    
    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        # 将输入数据添加到缓冲区
        self.buffer.extend(in0.tolist())
        
        # 计算可以处理的帧数
        nframes = len(self.buffer) // self.payload_length
        max_frames_out = len(out) // (len(self.gold_sequence) + self.payload_length)
        nframes_process = min(nframes, max_frames_out)
        
        if nframes_process == 0:
            return 0
        
        # 处理每帧数据
        for i in range(nframes_process):
            # 获取当前帧的载荷数据
            payload_start = i * self.payload_length
            payload_end = payload_start + self.payload_length
            payload = self.buffer[payload_start:payload_end]
            
            # 构建输出帧：Gold序列 + 载荷数据
            frame_start = i * (len(self.gold_sequence) + self.payload_length)
            frame_end = frame_start + len(self.gold_sequence) + self.payload_length
            
            # 复制Gold序列到输出
            out[frame_start:frame_start + len(self.gold_sequence)] = self.gold_sequence
            
            # 复制载荷数据到输出
            out[frame_start + len(self.gold_sequence):frame_end] = payload
        
        # 更新缓冲区，移除已处理的数据
        self.buffer = self.buffer[nframes_process * self.payload_length:]
        
        # 消耗的输入数据量
        self.consume(0, nframes_process * self.payload_length)
        
        # 产生的输出数据量
        return nframes_process * (len(self.gold_sequence) + self.payload_length)
