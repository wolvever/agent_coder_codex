# Agent Coder Codex

This project contains a minimal framework for building coding agents.

## Components

- **Planner**: Stateless component that produces the next `PlannerStep` given
  the current `PlanningContext`. The planner can instruct the agent to display
  messages, trigger tool use, or finish the task.
- **Agent**: Executes a loop using a planner. It keeps chat history in a
  `Session` and processes actions like `FinishAction`. Agents hold the set of
  available `Tool` instances.
- **Scheduler**: Manages multiple sessions and dispatches tasks to agents.
- **Tools**: Simple asynchronous helpers for running commands such as Git or
  test suites.
- **Sandbox**: Each session owns a sandbox directory that tools operate in.
- **UserInput**: Represents user queries and uploaded files for multi-modal interaction.

## Example

A basic echo agent is located in `examples/simple_agent.py`:

```bash
python examples/simple_agent.py
```

This will run the agent once and print the result using the new `UserInput`
abstraction.
