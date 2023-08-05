# Segment Profile Action

After the flow is completed, a procedure called "Post Event Segmentation" is executed in Tracardi. This procedure
involves using predefined conditions to assign customer data to specific segment groups. It's important to note that
these conditions are defined outside of the workflow but need to be triggered by the workflow itself. However, there is
an exception to this rule.

If a profile is updated during the workflow, it will automatically trigger the user segmentation process. In such cases,
there is no need to manually trigger segmentation within the workflow.

If, for any reason, you still want to manually trigger segmentation, you can connect a node in the workflow to initiate
the process. This allows for flexibility in case you need to override the automatic triggering of segmentation and
manually control when it occurs.

## Configuration

This node needs no configuration. It does not require any input data and does not return data.

## Side effect

Segmentation does not have side effects.