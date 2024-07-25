import asyncio
import signal
from temporalio.client import Client
from temporalio.worker import Worker

from test.manual.temporalbatch_workflow import EventBatcherWorkflow, process_data_batch, EventBatchStorageWorkflow, \
    task_queue


# Function to gracefully shut down the worker
async def shutdown_worker(worker: Worker):
    print("Shutting down worker...")
    await worker.shutdown()
    print("Worker has been shut down gracefully.")

async def run_worker():
    client = await Client.connect("167.235.119.124:7233")

    worker = Worker(
        client,
        task_queue=task_queue,
        workflows=[EventBatcherWorkflow, EventBatchStorageWorkflow],
        activities=[process_data_batch],
    )
    print(worker.is_running)
    loop = asyncio.get_running_loop()

    # Register signal handlers for graceful shutdown
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown_worker(worker)))

    # Run the worker
    await worker.run()

# Run the worker in an asyncio event loop
if __name__ == "__main__":
    asyncio.run(run_worker())
