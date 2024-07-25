from asyncio import sleep

from temporalio import activity, workflow
from datetime import timedelta

task_queue = 'event-batcher-queue'


@activity.defn
async def process_data_batch(data_batch):
    print(f"Processing batch: {data_batch}")


@workflow.defn
class EventBatchStorageWorkflow:
    @workflow.run
    async def run(self, data_batch):
        await workflow.execute_activity(
            process_data_batch,
            data_batch,
            start_to_close_timeout=timedelta(seconds=30)
        )


@workflow.defn
class EventBatcherWorkflow:
    def __init__(self):
        self.data_buffer = []
        self.buffer_timeout = 5
        self.should_exit = False
        self.total = 0
        self.max_events_per_flow = 100

    @workflow.signal
    async def add_data(self, data):
        info = workflow.info()
        print("Adding to buffer", data, len(self.data_buffer), info.workflow_id)
        self.data_buffer.append(data)
        self.total += 1
        if len(self.data_buffer) >= 10:
            await self.start_child_workflow()

    @workflow.signal
    def shutdown(self):
        print("Shutdown signal received. Stopping worker...")
        self.should_exit = True

    def should_run(self) -> bool:
        return not self.should_exit

    @workflow.run
    async def run(self):
        info = workflow.info()
        print('starts', info.workflow_id, not self.should_exit)
        while self.should_run():
            print("sleeps", self.buffer_timeout, self.total)
            await sleep(self.buffer_timeout)
            if self.data_buffer:
                await self.start_child_workflow()

            if self.total > self.max_events_per_flow:
                break
            print("runs", info.workflow_id, not self.should_exit)

        print("stops", info.workflow_id, not self.should_exit)

    async def start_child_workflow(self):
        data_batch = self.data_buffer[:]
        self.data_buffer.clear()
        try:
            await workflow.execute_child_workflow(
                EventBatchStorageWorkflow.run,
                data_batch,
                id=f"storage-{workflow.info().workflow_id}-{workflow.now()}"
            )
        except Exception as e:
            print(f"Child workflow failed: {e}")
            self.data_buffer.extend(data_batch)
            print("buffer", len(self.data_buffer))
