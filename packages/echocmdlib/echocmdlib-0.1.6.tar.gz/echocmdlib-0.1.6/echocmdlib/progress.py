from rich.progress import Progress
import time


def show_progress(task_name, total):
    with Progress() as progress:
        task = progress.add_task(task_name, total=total)
        while not progress.finished:
            progress.update(task, advance=1)
            # 模拟处理时间
            time.sleep(0.1)
