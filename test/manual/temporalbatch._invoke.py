from random import randint

from temporalio.client import Client

from test.manual.temporalbatch_workflow import EventBatcherWorkflow, task_queue
from temporalio.exceptions import WorkflowAlreadyStartedError

number_of_workers = 3


# Import your workflow definition

async def send_data():
    client = await Client.connect("167.235.119.124:7233")
    for _ in range(0, 1):

        # Start the parent workflow
        workflow_id = str(f"wf-{randint(0, number_of_workers)}")
        print(workflow_id)
        try:
            handle = await client.start_workflow(
                EventBatcherWorkflow.run,
                id=workflow_id,
                task_queue=task_queue
            )
        except WorkflowAlreadyStartedError:
            handle = client.get_workflow_handle(workflow_id=workflow_id)

        # Send data via signals

        for i in range(14):
            print(f"data-{i}")
            await handle.signal(EventBatcherWorkflow.add_data, f"data-{i}")
        await handle.signal(EventBatcherWorkflow.shutdown)
    # Optionally, wait for the workflow to complete
    # await handle.result()


if __name__ == "__main__":
    import asyncio

    asyncio.run(send_data())
