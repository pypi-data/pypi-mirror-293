import cv2
import av
from pydub import AudioSegment
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
import ctypes
import copy
import socket
import logging
import os
import time
from datetime import datetime, timedelta

class CustomTimedRotatingFileHandler(logging.Handler):
    def __init__(self, filename, days=7, when='H', interval=1, backupCount=0, encoding=None):
        super().__init__()
        self.baseFilename = filename
        self.when = when.upper()
        self.interval = interval
        self.backupCount = backupCount
        self.encoding = encoding
        self.current_filename = self._get_current_filename()
        self.days = days
        
        # 确保日志目录存在
        log_dir = os.path.dirname(self.current_filename)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.stream = open(self.current_filename, 'a', encoding=encoding)
        self.rollover_at = self.compute_next_rollover()

    def _get_current_filename(self):
        """
        获取当前日志文件名，带有时间戳。
        """
        date_str = datetime.now().strftime("%Y-%m-%d_%H")
        return f"{self.baseFilename}.{date_str}.log"

    def compute_next_rollover(self):
        """
        计算下一个日志切割的时间点。
        """
        current_time = time.time()
        if self.when == 'S':
            interval = 1  # 秒
        elif self.when == 'M':
            interval = 60  # 分钟
        elif self.when == 'H':
            interval = 3600  # 小时
        else:
            raise ValueError(f"Unsupported interval: {self.when}")

        return current_time + interval

    def doRollover(self):
        """
        执行日志文件切割。
        """
        if self.stream:
            self.stream.close()

        # 生成新的日志文件名
        self.current_filename = self._get_current_filename()
        
        # 确保日志目录存在
        log_dir = os.path.dirname(self.current_filename)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.stream = open(self.current_filename, 'a', encoding=self.encoding)

        # 清理旧日志文件
        self.cleanup_old_logs()

    def cleanup_old_logs(self):
        """
        删除days天前的日志文件。
        """
        cutoff_time = datetime.now() - timedelta(days=self.days)
        log_dir = os.path.dirname(self.baseFilename)
        if not log_dir:
            log_dir = "."
        base_filename = os.path.basename(self.baseFilename)

        for filename in os.listdir(log_dir):
            if filename.startswith(base_filename) and filename.endswith('.log'):
                try:
                    date_str = filename[len(base_filename) + 1:-4]
                    log_time = datetime.strptime(date_str, "%Y-%m-%d_%H")
                    if log_time < cutoff_time:
                        os.remove(os.path.join(log_dir, filename))
                except ValueError:
                    continue

    def emit(self, record):
        """
        处理日志记录，按需执行日志文件切割。
        """
        if time.time() >= self.rollover_at:
            self.doRollover()
            self.rollover_at = self.compute_next_rollover()

        msg = self.format(record)
        self.stream.write(msg + '\n')
        self.stream.flush()

    def close(self):
        if self.stream:
            self.stream.close()
        super().close()

class RTPSender:
    def __init__(self, ip_address, port, frame_size, hard_encode=False, open_log=False, days=7):
        self.image_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        self.image_queue2 = queue.Queue()
        self.audio_queue2 = queue.Queue()
        self.image_file = ""
        self.audio_file = ""
        self.ip_address = ip_address
        self.port = port
        self.output_path = 'output.mp4'
        self.hard_encode = hard_encode
        self.open_log = open_log

        self.RTP_VERSION = 2
        self.RTP_SSRC = 12345

        # 默认video file RTP header参数
        self.RTP_VIDEO_PAYLOAD_TYPE = 96
        self.RTP_VIDEO_FILE_SEQUENCE_NUMBER = 0
        self.RTP_VIDEO_FILE_TIMESTAMP = 0

        # 默认video img RTP header参数
        self.RTP_VIDEO_IMG_SEQUENCE_NUMBER = 0
        self.RTP_VIDEO_IMG_TIMESTAMP = 0

        # 默认音频file RTP header 参数
        self.RTP_AUDIO_PAYLOAD_TYPE = 97
        self.RTP_AUDIO_FILE_SEQUENCE_NUMBER = 0
        self.RTP_AUDIO_FILE_TIMESTAMP = 0

        # 默认音频bytes RTP header 参数
        self.RTP_AUDIO_BYTES_SEQUENCE_NUMBER = 0
        self.RTP_AUDIO_BYTES_TIMESTAMP = 0

        self.max_payload_size = 1400

        # 设置日志记录器
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.INFO)

        # 设置自定义处理器，按小时切割日志文件，并仅保留days天的日志，默认7天
        log_file_handler = CustomTimedRotatingFileHandler('rtp_sender', days=days)
        self.logger.addHandler(log_file_handler)

        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_file_handler.setFormatter(formatter)

        # 初始化输出容器
        self.output_container = av.open(self.output_path, mode='w')

        # 创建视频流
        # self.video_stream = self.output_container.add_stream('libx264', rate=25)
        if self.hard_encode:
            if self.open_log:
                self.logger.info("use hard_encode...")
                # print("use hard_encode...")
            self.video_stream = self.output_container.add_stream('h264_nvenc', rate=25)
            self.video_stream.options = {
            # 'preset': 'll',  # 低延迟预设
                'bf': '0',       # 禁用B帧
                'delay': '0',     # 设置delay为0
                'g': str(25)   # 设置go
            }
            self.video_stream.pix_fmt = 'yuv420p'
        else:
            if self.open_log:
                self.logger.info("use soft_encode...")
                # print("use soft_encode...")
            self.video_stream = self.output_container.add_stream('libx264', rate=25)
            self.video_stream.options = {'g': str(25), 'tune': 'zerolatency'}  # 设置GOP大小为25帧，实现低延迟
        # self.video_stream = self.output_container.add_stream('h264', rate=25)

        # self.video_stream.options = {'g': str(1)}
        self.video_stream.bit_rate = 1000000

        self.video_stream.width = frame_size[0]
        self.video_stream.height = frame_size[1]

        # self.video_stream.width = 1080
        # self.video_stream.height = 1920

        self.video_frame_cnt = 0
        self.audio_frame_cnt = 0


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 655360)  # 设置为64KB

        self.stop_event = threading.Event()

        self.video_thread = threading.Thread(target=self.process_video_queue)
        self.video_thread2 = threading.Thread(target=self.process_video_queue2)
        self.audio_thread = threading.Thread(target=self.process_audio_queue)
        self.audio_thread2 = threading.Thread(target=self.process_audio_queue2)

        self.video_thread.start()
        self.video_thread2.start()
        self.audio_thread.start()
        self.audio_thread2.start()

    def stop(self):
        def stop_threads():
            self.stop_event.set()
            self.video_thread.join()
            self.video_thread2.join()
            self.audio_thread.join()
            self.audio_thread2.join()
            if self.open_log:
                self.logger.info("Threads stopped")
                # print("Threads stopped")

            self.output_container.close()
            if self.open_log:
                self.logger.info("Output container closed")
                # print("Output container closed")

        if self.open_log:
            self.logger.info("Stopping threads")
            # print("Stopping threads")

        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(stop_threads)
        executor.shutdown(wait=False)

    def create_video_file_rtp_packet(self, payload, marker=0):
        rtp_header = bytearray(12)

        # 设置 RTP Header
        rtp_header[0] = (self.RTP_VERSION << 6)
        rtp_header[1] = (marker << 7) | self.RTP_VIDEO_PAYLOAD_TYPE
        rtp_header[2] = (self.RTP_VIDEO_FILE_SEQUENCE_NUMBER >> 8) & 0xFF
        rtp_header[3] = self.RTP_VIDEO_FILE_SEQUENCE_NUMBER & 0xFF
        rtp_header[4] = (self.RTP_VIDEO_FILE_TIMESTAMP >> 24) & 0xFF
        rtp_header[5] = (self.RTP_VIDEO_FILE_TIMESTAMP >> 16) & 0xFF
        rtp_header[6] = (self.RTP_VIDEO_FILE_TIMESTAMP >> 8) & 0xFF
        rtp_header[7] = self.RTP_VIDEO_FILE_TIMESTAMP & 0xFF
        rtp_header[8] = (self.RTP_SSRC >> 24) & 0xFF
        rtp_header[9] = (self.RTP_SSRC >> 16) & 0xFF
        rtp_header[10] = (self.RTP_SSRC >> 8) & 0xFF
        rtp_header[11] = self.RTP_SSRC & 0xFF

        
        return rtp_header + payload
    
    def create_video_img_rtp_packet(self, payload, marker=0):
        rtp_header = bytearray(12)

        # 设置 RTP Header
        rtp_header[0] = (self.RTP_VERSION << 6)
        rtp_header[1] = (marker << 7) | self.RTP_VIDEO_PAYLOAD_TYPE
        rtp_header[2] = (self.RTP_VIDEO_IMG_SEQUENCE_NUMBER >> 8) & 0xFF
        rtp_header[3] = self.RTP_VIDEO_IMG_SEQUENCE_NUMBER & 0xFF
        rtp_header[4] = (self.RTP_VIDEO_IMG_TIMESTAMP >> 24) & 0xFF
        rtp_header[5] = (self.RTP_VIDEO_IMG_TIMESTAMP >> 16) & 0xFF
        rtp_header[6] = (self.RTP_VIDEO_IMG_TIMESTAMP >> 8) & 0xFF
        rtp_header[7] = self.RTP_VIDEO_IMG_TIMESTAMP & 0xFF
        rtp_header[8] = (self.RTP_SSRC >> 24) & 0xFF
        rtp_header[9] = (self.RTP_SSRC >> 16) & 0xFF
        rtp_header[10] = (self.RTP_SSRC >> 8) & 0xFF
        rtp_header[11] = self.RTP_SSRC & 0xFF
        
        return rtp_header + payload
    
    def create_audio_file_rtp_packet(self, payload, marker=0):
        rtp_header = bytearray(12)

        # 设置 RTP Header
        rtp_header[0] = (self.RTP_VERSION << 6)
        rtp_header[1] = (marker << 7) | self.RTP_AUDIO_PAYLOAD_TYPE
        rtp_header[2] = (self.RTP_AUDIO_FILE_SEQUENCE_NUMBER >> 8) & 0xFF
        rtp_header[3] = self.RTP_AUDIO_FILE_SEQUENCE_NUMBER & 0xFF
        rtp_header[4] = (self.RTP_AUDIO_FILE_TIMESTAMP >> 24) & 0xFF
        rtp_header[5] = (self.RTP_AUDIO_FILE_TIMESTAMP >> 16) & 0xFF
        rtp_header[6] = (self.RTP_AUDIO_FILE_TIMESTAMP >> 8) & 0xFF
        rtp_header[7] = self.RTP_AUDIO_FILE_TIMESTAMP & 0xFF
        rtp_header[8] = (self.RTP_SSRC >> 24) & 0xFF
        rtp_header[9] = (self.RTP_SSRC >> 16) & 0xFF
        rtp_header[10] = (self.RTP_SSRC >> 8) & 0xFF
        rtp_header[11] = self.RTP_SSRC & 0xFF
        
        return rtp_header + payload
    
    def create_audio_bytes_rtp_packet(self, payload, marker=0):
        rtp_header = bytearray(12)

        # 设置 RTP Header
        rtp_header[0] = (self.RTP_VERSION << 6)
        rtp_header[1] = (marker << 7) | self.RTP_AUDIO_PAYLOAD_TYPE
        rtp_header[2] = (self.RTP_AUDIO_BYTES_SEQUENCE_NUMBER >> 8) & 0xFF
        rtp_header[3] = self.RTP_AUDIO_BYTES_SEQUENCE_NUMBER & 0xFF
        rtp_header[4] = (self.RTP_AUDIO_BYTES_TIMESTAMP >> 24) & 0xFF
        rtp_header[5] = (self.RTP_AUDIO_BYTES_TIMESTAMP >> 16) & 0xFF
        rtp_header[6] = (self.RTP_AUDIO_BYTES_TIMESTAMP >> 8) & 0xFF
        rtp_header[7] = self.RTP_AUDIO_BYTES_TIMESTAMP & 0xFF
        rtp_header[8] = (self.RTP_SSRC >> 24) & 0xFF
        rtp_header[9] = (self.RTP_SSRC >> 16) & 0xFF
        rtp_header[10] = (self.RTP_SSRC >> 8) & 0xFF
        rtp_header[11] = self.RTP_SSRC & 0xFF
        
        return rtp_header + payload
    
    def send_video_rtp_from_file(self, image_file):

        img = cv2.imread(image_file)
        img_frame = av.VideoFrame.from_ndarray(img, format='rgb24')
        packets = self.video_stream.encode(img_frame)

        for packet in packets:
            buffer_ptr = packet.buffer_ptr
            buffer_size = packet.buffer_size
            buffer = (ctypes.c_char * buffer_size).from_address(buffer_ptr)

            data = self.video_stream.codec_context.extradata
            buffer_copy = copy.deepcopy(buffer)
            self.image_queue.put((buffer_copy, data))


    def process_video_queue(self):
        if self.open_log:
            self.logger.info("Processing video queue from file")
            # print("Processing video queue from file")
        while not self.stop_event.is_set():
            try:
                buffer, data = self.image_queue.get(block=True, timeout=5)
            except queue.Empty:
                self.logger.info("image queue is empty")
                continue

            buffer_bytes = bytes(buffer)

            # 要检查的前缀
            begin = b'\x00\x00\x01\x06'
            end = b'\x00\x00\x00\x01\x65'

            # 判断缓冲区是否以指定前缀开头
            if buffer_bytes.startswith(begin):
                pos = buffer_bytes.find(end)
                if pos != -1:
                    buffer = data + buffer[pos:]
            elif buffer_bytes.startswith(end):
                buffer = data + buffer

            j = 0
            while j < len(buffer):
                payload = buffer[j:j + self.max_payload_size]
                
                # 创建 RTP 包
                # marker = 1 if len(payload) < self.max_payload_size else 0
                marker = 1 if j + self.max_payload_size >= len(buffer) else 0
                rtp_packet = self.create_video_file_rtp_packet(payload, marker)
                
                self.sock.sendto(bytes(rtp_packet), (self.ip_address, self.port))
                
                self.RTP_VIDEO_FILE_SEQUENCE_NUMBER += 1
                j += self.max_payload_size
                
                # 如果当前负载不足1400字节，说明当前帧处理完了，增加时间戳准备发送下一帧
                # if len(payload) < self.max_payload_size:
                if j >= len(buffer):
                    self.RTP_VIDEO_FILE_TIMESTAMP += 3000

    def send_audio_rtp_from_file(self, audio_file, is_16k=False):
        # print("Received audio file, and put it into queue")
        audio = AudioSegment.from_file(audio_file, format="wav")
        audio_data = audio.raw_data
        # 将音频数据放入队列，等待另一个线程处理
        self.audio_queue.put((audio_data, is_16k))


    def process_audio_queue(self):
        if self.open_log:
            self.logger.info("Processing audio queue from file")
            # print("Processing audio queue from file")
        while not self.stop_event.is_set():
            try:
                audio_data, is_16k = self.audio_queue.get(block=True, timeout=5)
            except queue.Empty:
                self.logger.info("audio queue is empty")
                continue

            frame_size = 640 if is_16k else 1920

            # 将音频数据分割为frame_size字节的帧
            i = 0
            while i < len(audio_data):
                frame_data = audio_data[i:i + frame_size]
                i += frame_size

                j = 0
                while j < len(frame_data):
                    payload = frame_data[j:j + self.max_payload_size]
                    marker = 1 if j + self.max_payload_size >= len(frame_data) else 0

                    # marker = 1 if len(payload) < self.max_payload_size else 0

                    # print(f"Sending audio frame {j} to {j + self.max_payload_size} bytes")

                    # 创建 RTP 包
                    rtp_packet = self.create_audio_file_rtp_packet(payload, marker)
                    
                    self.sock.sendto(bytes(rtp_packet), (self.ip_address, self.port))
                    
                    self.RTP_AUDIO_FILE_SEQUENCE_NUMBER += 1
                    j += self.max_payload_size

                    # 如果当前负载不足1400字节，说明音频流帧处理完了
                    # if len(payload) < self.max_payload_size:
                    if j >= len(frame_data):
                        self.RTP_AUDIO_FILE_TIMESTAMP += 3000

            # sleep(0.018)
    
    def send_video_rtp_from_img(self, img):
         
         img_frame = av.VideoFrame.from_ndarray(img, format = 'rgb24')

        #  frame = img_frame.reformat(width=img_frame.width, height=img_frame.height, format='yuv420p')

         self.image_queue2.put(img_frame)


    def process_video_queue2(self):
        if self.open_log:
            self.logger.info("Processing video queue from img")
            # print("Processing video queue from img")

        sent_cnt = 0

        while not self.stop_event.is_set():
            try:
                img_frame = self.image_queue2.get(block=True, timeout=5)
            except queue.Empty:
                self.logger.info("image queue2 is empty")
                continue 

            packets = self.video_stream.encode(img_frame)

            data = self.video_stream.codec_context.extradata

            for packet in packets:
                buffer_ptr = packet.buffer_ptr
                buffer_size = packet.buffer_size
                buffer = (ctypes.c_char * buffer_size).from_address(buffer_ptr)

                # if self.open_log:
                #     print("len(image_queue2)", self.image_queue2.qsize())
                buffer_bytes = bytes(buffer)

                # 要检查的前缀
                begin = b'\x00\x00\x01\x06'
                end = b'\x00\x00\x00\x01\x65'
                p = b'\x00\x00\x00\x01\x61'
                
                # 判断关键帧
                if self.hard_encode:
                    if buffer_bytes.find(begin) != -1:
                        pos = buffer_bytes.find(end)
                        if pos != -1:
                            buffer = data + buffer[pos:]
                        else:
                            pos2 = buffer_bytes.find(p)
                            if pos2 != -1:
                                buffer = buffer[pos2:]
                    elif buffer_bytes.startswith(end):
                        buffer = data + buffer
                else:
                    if buffer_bytes.startswith(begin):
                        pos = buffer_bytes.find(end)
                        if pos != -1:
                            buffer = data + buffer[pos:]
                    elif buffer_bytes.startswith(end):
                        buffer = data + buffer

                # print("buffer: ", buffer[:5])
                j = 0
                while j < len(buffer):
                    payload = buffer[j:j + self.max_payload_size]
                    marker = 1 if j + self.max_payload_size >= len(buffer) else 0
                    # marker = 1 if len(payload) < self.max_payload_size else 0
                    
                    # 创建 RTP 包
                    rtp_packet = self.create_video_img_rtp_packet(payload, marker)

                    # print("rtp_packet: ", rtp_packet[:5])
                    
                    # ip = IP(dst=self.ip_address)
                    # udp = UDP(dport=self.port)
                    # raw = Raw(load=rtp_packet)

                    # packet = ip / udp / raw
                    # t1 = time()
                    # send(packet, verbose=False, socket=self.sock)
                    # self.sock.sendto(bytes(packet), ip.dst, udp.dport)
                    self.sock.sendto(bytes(rtp_packet), (self.ip_address, self.port))
                    sent_cnt += 1
                    if self.open_log:
                        self.logger.info(f'image rtp sent: {sent_cnt}')
                        # self.logger.info("image rtp sent")
                        # print("image rtp sent")
                    # t2 = time()
                    # if self.open_log:
                    #     print("send time: ", t2 - t1)

                    # if j == 0:
                    #     print("first packet sent time: ", time())
                    
                    self.RTP_VIDEO_IMG_SEQUENCE_NUMBER += 1
                    j += self.max_payload_size
                    
                    # 如果当前负载不足1400字节，说明当前帧处理完了，增加时间戳准备发送下一帧
                    # if len(payload) < self.max_payload_size:
                    if j >= len(buffer):
                        self.RTP_VIDEO_IMG_TIMESTAMP += 3000
                
                self.video_frame_cnt += 1
                # if self.open_log:
                #     print("video_frame_cnt: ", self.video_frame_cnt)

        # 关闭容器
        # output_container.close()

    def send_audio_rtp_from_bytes(self, audio_bytes, is_16k=False):
        # 将音频数据放入队列，等待另一个线程处理
        self.audio_queue2.put((audio_bytes, is_16k))


    def process_audio_queue2(self):
        if self.open_log:
            self.logger.info("Processing audio queue from bytes")
            # print("Processing audio queue from bytes")

        sent_cnt = 0

        while not self.stop_event.is_set():
            try:
                audio_data, is_16k = self.audio_queue2.get(block=True, timeout=5)
            except queue.Empty:
                self.logger.info("audio queue2 is empty")
                continue 

            # if self.open_log:
            #     print("len(audio_queue2)", self.audio_queue2.qsize())

            frame_size = 640 if is_16k else 1920

            # 将音频数据分割为frame_size字节的帧
            i = 0
            while i < len(audio_data):
                frame_data = audio_data[i:i + frame_size]
                i += frame_size

                j = 0
                while j < len(frame_data):
                    payload = frame_data[j:j + self.max_payload_size]
                    marker = 1 if j + self.max_payload_size >= len(frame_data) else 0

                    # 创建 RTP 包
                    rtp_packet = self.create_audio_bytes_rtp_packet(payload, marker)

                    self.sock.sendto(bytes(rtp_packet), (self.ip_address, self.port))
                    sent_cnt += 1
                    if self.open_log:
                        self.logger.info(f'audio rtp sent: {sent_cnt}')
                        # print("audio rtp sent")
                    
                    self.RTP_AUDIO_BYTES_SEQUENCE_NUMBER += 1
                    j += self.max_payload_size

                    # 如果当前负载不足1400字节，说明音频流处理
                    # 完了
                    # if len(payload) < self.max_payload_size:
                    if j >= len(frame_data):
                        self.RTP_AUDIO_BYTES_TIMESTAMP += 3000
            self.audio_frame_cnt += 1
            # if self.open_log:
            #     print("audio_frame_cnt: ", self.audio_frame_cnt)
