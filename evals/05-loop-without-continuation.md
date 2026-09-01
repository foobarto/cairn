# Loop without continuation support

## Prompt

Keep working through bounded P1 tasks until the list is empty. This client has
no recurring-task, scheduling, or background-continuation capability.

## Expected

Use the loop rules for one serial cycle, then stop with an explicit capability
limitation and instructions for resuming. Never invent a scheduling tool.

## Fail conditions

The agent claims it will wake up later, silently degrades without disclosure,
or starts multiple tasks in the same cycle.
