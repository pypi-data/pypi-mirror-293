import logging

from quesadilla.connectors.in_memory import ThreadSafeInMemoryConnector
from quesadilla.runners import MultithreadingRunner, RunnerConfig
from quesadilla.shortcuts import QueuedTask, TaskNamespace, async_task, sync_task

logging.basicConfig(level=logging.INFO)

namespace = TaskNamespace(
    "quesadilla.examples.simple",
    connector=ThreadSafeInMemoryConnector(),
)
queue = namespace.new("queue")


@sync_task(queue)
def simple_task(i: int) -> bool:
    return i == 0


@async_task(queue)
async def simple_atask(i: int) -> bool:
    return i == 0


tasks: list[QueuedTask[[int], bool]] = []


# queue is preloaded with 200 tasks
for _ in range(100):
    tasks.append(simple_task.queue(0))
    tasks.append(simple_atask.queue(1))


if __name__ == "__main__":
    runner = MultithreadingRunner(queue, config=RunnerConfig(brokers=2, workers=5))
    with runner:
        for task in tasks:
            task.wait_for()

    # runner will automatically shut down and clean up when all tasks are done
