import threading
import time
import traceback
from enum import Enum, auto


class JobStatus(Enum):
    """任务状态枚举"""
    IDLE = auto()  # 空闲
    RUNNING = auto()  # 运行中
    PAUSED = auto()  # 已暂停
    STOPPED = auto()  # 已停止


class JobTemplate:
    def __init__(self):
        self._status = JobStatus.IDLE
        self._lock = threading.RLock()
        self._thread = None
        self._pause_event = threading.Event()
        self._stop_event = threading.Event()

    def _run_task(self):
        """任务核心逻辑（子类需重写此方法）"""
        while not self._stop_event.is_set():
            if self._status == JobStatus.PAUSED:
                self._pause_event.wait()  # 阻塞直到取消暂停
                continue

            # 模拟任务执行（替换为实际逻辑）
            print(f"Job is running... (Status: {self._status.name})")
            time.sleep(1)

    def _run(self):
        try:
            self._run_task()
        except Exception as e:
            traceback.print_exc()
        self.stop()

    def start(self):
        """启动任务"""
        with self._lock:
            if self._status == JobStatus.RUNNING:
                print("Job is already running!")
                return

            self._status = JobStatus.RUNNING
            self._pause_event.set()  # 确保暂停标志已清除
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
            print("Job started.")

    def pause(self):
        """暂停任务"""
        with self._lock:
            if self._status != JobStatus.RUNNING:
                print("Job is not running!")
                return

            self._status = JobStatus.PAUSED
            self._pause_event.clear()  # 设置阻塞
            print("Job paused.")

    def resume(self):
        """恢复任务"""
        with self._lock:
            if self._status != JobStatus.PAUSED:
                print("Job is not paused!")
                return

            self._status = JobStatus.RUNNING
            self._pause_event.set()  # 解除阻塞
            print("Job resumed.")

    def pause_or_resume(self):
        with self._lock:
            if self._status == JobStatus.PAUSED:
                self.resume()
            elif self._status == JobStatus.RUNNING:
                self.pause()

    def stop(self):
        """停止任务"""
        with self._lock:
            if self._status == JobStatus.STOPPED:
                print("Job is already stopped!")
                return

            self._status = JobStatus.STOPPED
            self._stop_event.set()
            self._pause_event.set()  # 确保线程能退出阻塞
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=1)  # 等待线程结束
            print("Job stopped.")

    @property
    def status(self):
        """获取当前状态"""
        return self._status

    def reset(self):
        with self._lock:
            self._status = JobStatus.IDLE
            self._thread = None
            self._pause_event = threading.Event()
            self._stop_event = threading.Event()

    def join(self):
        if self._thread and self._thread.is_alive():
            self._thread.join()

# ----------------------------
# 使用示例
if __name__ == "__main__":
    job = JobTemplate()

    # 模拟控制流程
    job.start()  # 启动
    time.sleep(2)
    job.pause()  # 暂停
    time.sleep(2)
    job.resume()  # 恢复
    time.sleep(2)
    job.stop()  # 停止