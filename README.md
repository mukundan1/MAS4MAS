# Multi-Agent System with PraisonAI

A multi-agent AI system built with PraisonAI Agents framework that enables interactive chat, planning, coding, testing, and deployment capabilities using specialized AI agents.

---

## 🌟 Overview

This application implements a hierarchical multi-agent system using the PraisonAI Agents framework. The system consists of five specialized agents that work together to create comprehensive solutions:

1. **InteractiveChatAgent** - Handles user interaction and conversation flow
2. **PlannerAgent** - Creates detailed plans and specifications
3. **CoderAgent** - Generates and executes Python code
4. **TesterAgent** - Validates and tests generated code
5. **DeployerAgent** - Handles deployment and system setup

---

## 🏗️ Architecture

### System Flow

```
User Input → InteractiveChatAgent → PlannerAgent → CoderAgent → TesterAgent → DeployerAgent
     ↓              ↓                    ↓              ↓              ↓
Internet Search  Internet Search    Code Execution  Testing      Deployment
```

### Agent Capabilities

#### InteractiveChatAgent
- **Purpose**: Manages user conversations and interactions
- **Tools**: 
  - `create_chat_interface()` - Creates interactive chat interface
  - `internet_search_tool()` - Searches the internet for information
- **Model**: GPT-4o-mini
- **Function**: Collects user requirements and provides initial responses

#### PlannerAgent
- **Purpose**: Creates detailed plans and specifications
- **Tools**: 
  - `internet_search_tool()` - Researches implementation options
- **Model**: GPT-4o-mini
- **Output**: JSON specification of the multi-agent system

#### CoderAgent
- **Purpose**: Writes and executes Python code
- **Tools**: 
  - `code_interpreter()` - Executes Python code in a sandboxed environment
- **Model**: GPT-4o-mini
- **Function**: Generates code based on plans and executes it safely

#### TesterAgent
- **Purpose**: Validates generated code and ensures quality
- **Model**: GPT-4o-mini
- **Function**: Tests code against specifications

#### DeployerAgent
- **Purpose**: Handles deployment and system setup
- **Tools**: 
  - `internet_search_tool()` - Researches deployment options
- **Model**: GPT-4o-mini
- **Function**: Deploys the final system

---

## 🛠️ Tools

### Internet Search Tool
Searches the internet using DuckDuckGo to find relevant information:
- **Input**: Search query string
- **Output**: List of search results with title, URL, and snippet
- **Max Results**: 5 results per query

### Code Interpreter Tool
Executes Python code in a secure sandboxed environment using E2B:
- **Input**: Python code string
- **Output**: JSON string with execution results, stdout, and stderr
- **Error Handling**: Returns error information if execution fails
- **Sandbox**: Uses E2B Code Interpreter for safe code execution

---

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key (for GPT-4o-mini)
- E2B API key (for code interpreter sandbox)

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd mas
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
E2B_API_KEY=your_e2b_api_key_here
```

**Note**: Make sure to add `.env` to your `.gitignore` file to prevent committing API keys.

### Step 5: Run the Application
```bash
python main.py
```

---

## 📁 Project Structure

```
mas/
├── main.py              # Main entry point with agent definitions
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

---

## 🔧 Configuration

### API Keys

The application requires the following API keys (stored in `.env`):

- **OPENAI_API_KEY**: Required for all agents using GPT-4o-mini
  - Get your key from: https://platform.openai.com/api-keys

- **E2B_API_KEY**: Required for code interpreter sandbox
  - Get your key from: https://e2b.dev/

### Model Configuration

All agents currently use `gpt-4o-mini` model. You can modify the `llm` parameter in each agent definition to use a different model.

---

## 💡 Usage

### Basic Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. The system will start and execute the multi-agent workflow

3. Agents will work together in a hierarchical process to:
   - Interact with user requirements
   - Create detailed plans
   - Generate and execute code
   - Test the generated code
   - Deploy the final system

### or else

1. Activate your python virtual environment 

2. Run the following command with your prompt for MAS as:
  ```bash
  praisonai --init <YOUR_PROMPT_FOR_MAS>
  ```
  (Optional) Specify the framework using ```--framework (crew | autogen)```

3. Using the agents.yaml, run the command praisonai

### Task Configuration

The application supports different task types:

- **Planning Task**: Creates detailed plans in JSON format
- **Coding Task**: Generates and executes code based on plans
- **Interactive Loop Task**: Handles iterative user interactions

---

## 🎯 Key Features

- **Multi-Agent Collaboration**: Five specialized agents working together
- **Internet Search**: Real-time information retrieval using DuckDuckGo
- **Code Execution**: Safe code execution in sandboxed environment
- **Hierarchical Process**: Coordinated workflow between agents
- **Interactive Chat**: User-friendly conversation interface
- **Async Execution**: Support for asynchronous task execution

---

## 📝 Code Structure

### Agent Definition Example

```python
Agent(
    name="AgentName",
    instructions="Agent instructions and behavior",
    llm="gpt-4o-mini",
    api_key=api_key,
    tools=[tool1, tool2]
)
```

### Task Definition Example

```python
Task(
    name="task_name",
    description="Task description",
    expected_output="Expected output format",
    agent=AgentInstance,
    tools=[tool1],
    output_file="output.md",
    async_execution=True
)
```

---

## ⚠️ Known Issues

1. **Missing JSON Import**: The `code_interpreter()` function uses `json.dumps()` but `json` is not imported. Add `import json` at the top of the file.

2. **Syntax Errors**: There are some syntax errors in the code (missing commas in agent/task definitions). These should be fixed for the code to run properly.

3. **Tool Function Calls**: Some task definitions call tools incorrectly (e.g., `tools=[internet_search_tool()]` should be `tools=[internet_search_tool]` without parentheses).

---

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your `.env` file is in the project root
   - Verify API keys are correctly set
   - Check that the `.env` file is being loaded correctly

2. **Import Errors**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`
   - Verify you're using the correct Python version (3.9+)

3. **Code Execution Errors**
   - Check E2B API key is valid
   - Ensure internet connection for DuckDuckGo searches
   - Verify code syntax before execution

---

## 📚 Dependencies

See `requirements.txt` for the complete list of dependencies. Key packages include:

- `praisonaiagents` - Multi-agent framework
- `python-dotenv` - Environment variable management
- `duckduckgo-search` - Internet search functionality
- `e2b-code-interpreter` - Sandboxed code execution

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All functionality is tested
- Documentation is updated
- No API keys are committed to the repository

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

Built with:
- [PraisonAI Agents](https://github.com/praisonai/praisonai-agents) - Multi-agent framework
- [OpenAI API Compatible Models](https://openai.com) - Language model
- [E2B Code Interpreter](https://e2b.dev/) - Sandboxed code execution
- [DuckDuckGo](https://duckduckgo.com/) - Internet search

---

## 📧 Support

For issues, questions, or contributions, please [create an issue](<repository-url>/issues) or contact the maintainers.

---

**Made with ❤️ by Mukundan**
