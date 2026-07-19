from pathlib import Path
from datetime import datetime
from typing import Tuple
import cv2
from cv2.typing import MatLike

class Recorder:
    def __init__(self, framerate: int, record_dir: str, base_name: str = "pygame_sandbox"):
        self.framerate = framerate
        self.record_dir = record_dir
        self.codec = 'MJPG' # 'XVID'
        self.base_name = base_name
        self.video_writer = None

    def init_record(self, shape: Tuple[int, int]):
        width, height = shape
        dir_path = Path(self.record_dir)
        dir_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filepath = str(dir_path / f"{self.base_name}-{timestamp}.avi")
        fourcc = cv2.VideoWriter_fourcc(*self.codec)
        self.video_writer = cv2.VideoWriter(filepath, fourcc, float(self.framerate), (width, height))

    def set_framerate(self, framerate: int):
        self.framerate = framerate

    def record_frame(self, frame: MatLike):
        if self.video_writer:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  
            self.video_writer.write(frame)

    def release(self):
        if self.video_writer:
            self.video_writer.release()
