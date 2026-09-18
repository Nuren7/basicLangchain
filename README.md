# Simple LangChain Tool-Calling Agent

A small terminal chatbot using Python, LangChain, and Groq. It has three tools: a calculator, a current date/time tool, and a tool that calls the JSONPlaceholder API.

## How This Differs From the Previous Chatbot

The previous chatbot sent every user message directly to the language model and printed the response. This version gives the model tools. When a question needs a calculation or the current date/time, the model can ask the program to run the matching tool before writing its answer.

## Important Ideas

### What is a tool?

A tool is a normal Python function with a name and description that the language model can use. This project has `calculator`, `current_date_time`, and `placeholder_todo` tools. The third tool makes a real HTTP request to JSONPlaceholder.

### What is a tool call?

A tool call is the model's structured request to use one of the available tools. It includes the tool name and the arguments it needs, such as `12 * (3 + 4)` for the calculator.

### What is the agent loop?

The basic graph in this project follows this loop:

```text
User message
    -> LLM decides whether a tool is needed
    -> Python executes the requested tool
    -> Tool result is sent back to the LLM
    -> LLM writes the final answer
```

The loop repeats until the model returns a normal answer without another tool call.

## Prerequisites

- Python 3.9 or newer.
- A [Groq API key](https://console.groq.com/keys).

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

2. Activate it.

   macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

   Windows PowerShell:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Copy `env.example` to `.env` and put your key in `.env`:

   ```env
   GROQ_API_KEY=your-groq-api-key-here
   ```

## Run

```bash
python chatbot.py
```

Type `exit`, `quit`, or `bye` to end the chat.

## Try These Prompts

1. `What is 25 * 4 + 10?` - requires the calculator.
2. `What is the current date and time?` - requires the date/time tool.
3. `What is 18 / 3, and what time is it right now?` - requires both tools.
4. `Explain in one sentence what LangChain is.` - does not require a tool.
5. `Remember that my favorite color is green. What is my favorite color?` - uses conversation history.
6. `Can you check todo item 1 from the placeholder API?` - requires the external API tool.

## Project Structure

```text
.
├── agent.py          # The LangGraph agent loop
├── tools.py          # The calculator and date/time tools
├── chatbot.py        # The terminal chat interface
├── requirements.txt  # Python dependencies
├── env.example       # Environment variable template
└── README.md         # This file
```

## File-by-File Implementation

### `tools.py`

Defines the three Python functions decorated with LangChain's `@tool`. The decorator gives each function a name and description that can be provided to the model. `placeholder_todo` calls `https://jsonplaceholder.typicode.com/todos/1`, and `TOOLS` contains all three tools made available to ChatGroq.

### `agent.py`

`create_agent` creates ChatGroq, binds the two tools, and builds a small LangGraph. The `agent` node calls the model, `should_continue` checks whether the response contains tool calls, and the `tools` node executes them. The graph then sends the tool results back to the `agent` node. `run_agent` invokes the graph and updates the conversation history.

### `chatbot.py`

Keeps the existing terminal interface and the full `messages` list. The list contains the system message, user messages, model responses, and tool results, so the conversation history remains available on every turn.
