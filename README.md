# Agent Coder Codex

This project contains a minimal framework for building coding agents.

## Components

- **Planner**: Stateless component that produces the next `PlannerStep` given
  the current `PlanningContext`. A planner can instruct the agent to display
  messages, trigger tool use, or finish the task. The repository ships with a
  trivial `EchoPlanner` and a `ToolPlanner` example.
- **Agent**: Executes a loop using a planner. It keeps chat history in a
  `Session` and processes actions like `FinishAction`. Agents hold the set of
  available `Tool` instances.
- **Scheduler**: Manages multiple sessions and dispatches tasks to agents.
- **Tools**: Simple asynchronous helpers for running commands such as Git,
  running tests or echoing text. Tools operate within the session's sandbox
  directory.
- **Sandbox**: Each session owns a sandbox directory that tools operate in.
- **UserInput**: Represents user queries and uploaded files for multi-modal interaction.


## Example

A basic echo agent is located in `examples/simple_agent.py`:

```bash
python examples/simple_agent.py
```

This will run the agent once and print the result using the new `UserInput`
abstraction.

The `ToolPlanner` demonstrates calling a tool before finishing. Running

```bash
python examples/simple_agent.py use-tool
```

will execute the `echo` tool and return its output.

## Sandbox Daemon

A small Go service is provided in `sandboxd/` that exposes an HTTP API for running
commands and manipulating files inside a sandbox directory. The daemon can be
started with:

```bash
go run ./sandboxd -root ./sandbox -addr :8080
```

Endpoints:

- `POST /run` with JSON `{ "command": "echo hi" }` runs a shell command.
- `POST /write` with JSON `{ "path": "file.txt", "data": "..." }` writes a
  base64 encoded file.
- `GET /read?path=foo` returns the file's base64 encoded contents.
- `GET /list` lists all files relative to the sandbox root.

This daemon is optional and is intended for scenarios where sandbox operations
should be isolated in a separate process.

