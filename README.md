# Multi-Agent System (MAS): A Hierarchical AI Agent Framework for Automated Software Development

## Abstract

This repository presents a production-grade multi-agent system (MAS) built on the PraisonAI Agents framework, implementing a hierarchical orchestration pattern for automated software development workflows. The system employs five specialized AI agents that collaborate through a structured decision-making process to transform high-level user requirements into fully functional, tested, and deployed software solutions. The architecture incorporates enterprise-grade features including caching, load balancing, monitoring, security, and optimization mechanisms, making it suitable for both research and production deployments.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [System Components](#system-components)
4. [Project Structure](#project-structure)
5. [Installation & Configuration](#installation--configuration)
6. [Usage](#usage)
7. [Technical Specifications](#technical-specifications)
8. [Research Contributions](#research-contributions)
9. [Performance & Optimization](#performance--optimization)
10. [Security](#security)
11. [Testing](#testing)
12. [Deployment](#deployment)
13. [Contributing](#contributing)
14. [License](#license)

---

## Overview

### System Purpose

The Multi-Agent System (MAS) is designed to automate the complete software development lifecycle through intelligent agent collaboration. The system accepts natural language requirements and orchestrates multiple specialized agents to produce production-ready code, comprehensive test suites, and deployment configurations.

### Key Capabilities

- **Requirement Elicitation**: Interactive conversation interface for gathering and refining user requirements
- **Automated Planning**: Generation of detailed implementation specifications in structured JSON format
- **Code Generation**: Production of executable Python code with proper structure and best practices
- **Automated Testing**: Comprehensive test suite generation and validation
- **Deployment Automation**: Containerized deployment configurations (Docker, Kubernetes)
- **Enterprise Features**: Caching, monitoring, load balancing, security, and cost optimization

### Target Audience

This system is designed for:
- **AI Researchers**: Studying multi-agent systems, hierarchical orchestration, and agent collaboration patterns
- **Software Engineers**: Implementing automated development workflows and CI/CD pipelines
- **DevOps Practitioners**: Deploying and managing AI-powered development tools
- **Academic Researchers**: Investigating agent-based software engineering methodologies

---

## Architecture

### Hierarchical Agent Orchestration

The system implements a **hierarchical process flow** where agents operate in a structured sequence with decision points for quality control and iterative refinement.

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Input (Natural Language)                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              InteractiveChatAgent (Loop Task)                    │
│  • Gathers requirements via conversational interface            │
│  • Uses internet_search_tool for research                       │
│  • Outputs structured requirement specification                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Decision Task (Quality Gate)                  │
│  Conditions: approve → planning_task                            │
│              revise → loop_interactive_task                      │
│              reject → loop_interactive_task                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PlannerAgent                                  │
│  • Analyzes requirements                                        │
│  • Researches implementation options                            │
│  • Generates JSON specification with:                           │
│    - Agent definitions                                          │
│    - Tool requirements                                          │
│    - Workflow steps                                             │
│    - Dependencies                                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CoderAgent                                    │
│  • Generates Python code from JSON specification                │
│  • Uses code_interpreter for safe execution                     │
│  • Implements: main.py, agents.py, tools.py, requirements.txt  │
│  • Tools: execute_code, analyze_code, format_code, lint_code    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    TesterAgent                                   │
│  • Performs static code analysis                                │
│  • Validates against original plan                              │
│  • Generates test report with confidence scores                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              Test Decision Task (Quality Gate)                   │
│  Conditions: approve → deployer_task                            │
│              revise → loop_interactive_task                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DeployerAgent                                 │
│  • Generates Docker/Docker Compose configurations               │
│  • Creates Kubernetes manifests (if needed)                     │
│  • Ensures localhost deployment                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Specifications

#### 1. InteractiveChatAgent
- **Role**: Conversational Interface Manager
- **Model**: `gpt-4o-mini` (configurable)
- **Tools**: 
  - `create_chat_interface()`: Interactive terminal-based chat
  - `internet_search_tool()`: Real-time information retrieval
- **Task Type**: Loop (iterative conversation)
- **Output**: Structured requirement specification with:
  - Programming language selection
  - Framework recommendations
  - Implementation type (API, Web App, Desktop, Mobile, CLI)
  - Deployment preferences

#### 2. PlannerAgent
- **Role**: Senior Project Manager / System Architect
- **Model**: `gpt-4o-mini` (configurable)
- **Reasoning Steps**: 3 (multi-step reasoning enabled)
- **Tools**: `internet_search_tool()`
- **Output**: JSON specification containing:
  ```json
  {
    "project_name": "string",
    "agents_to_create": [{"class_name": "...", "description": "..."}],
    "required_tools": [{"function_name": "...", "description": "..."}],
    "workflow": ["step 1", "step 2", ...],
    "dependencies": ["package1", "package2", ...]
  }
  ```

#### 3. CoderAgent
- **Role**: Senior Python Developer
- **Model**: `gpt-4o-mini` (configurable)
- **Tools**: 
  - `code_interpreter()`: E2B sandbox execution
  - `execute_code()`: Code execution utilities
  - `analyze_code()`: Static analysis
  - `format_code()`: Code formatting
  - `lint_code()`: Linting capabilities
  - `disassemble_code()`: Bytecode analysis
- **Output**: Complete Python project structure:
  - `main.py`: Orchestration logic
  - `agents.py`: Agent class definitions
  - `tools.py`: Tool implementations
  - `requirements.txt`: Dependencies

#### 4. TesterAgent
- **Role**: Senior QA Engineer
- **Model**: `gpt-4o-mini` (configurable)
- **Function**: Static code analysis and validation
- **Output**: Test report JSON:
  ```json
  {
    "success": boolean,
    "errors": ["error1", "error2", ...],
    "suggestions": ["suggestion1", ...],
    "confidence_score": float
  }
  ```

#### 5. DeployerAgent
- **Role**: DevOps Engineer / Localhost Deployer
- **Model**: `gpt-4o-mini` (configurable)
- **Tools**: `internet_search_tool()`
- **Output**: Deployment configurations:
  - Dockerfile
  - docker-compose.yml
  - Kubernetes manifests (optional)
  - Health check endpoints

---

## System Components

### Core Framework
- **PraisonAI Agents**: Multi-agent orchestration framework
- **Process Management**: Hierarchical workflow execution
- **Task Orchestration**: Sequential and parallel task execution

### Tools & Integrations

#### Internet Search Tool
- **Provider**: DuckDuckGo Search API
- **Function**: `internet_search_tool(query: str) -> List[Dict]`
- **Output Format**:
  ```python
  [
    {
      "title": "Result title",
      "url": "https://...",
      "snippet": "Result description"
    }
  ]
  ```
- **Max Results**: 5 per query
- **Use Cases**: Research, framework selection, best practices lookup

#### Code Interpreter Tool
- **Provider**: E2B Code Interpreter (sandboxed environment)
- **Function**: `code_interpreter(code: str) -> Dict`
- **Security**: Fully sandboxed execution environment
- **Output Format**:
  ```json
  {
    "results": ["output1", "output2", ...],
    "logs": {
      "stdout": ["log1", "log2", ...],
      "stderr": ["error1", ...]
    },
    "error": "error message (if any)"
  }
  ```
- **Capabilities**: Python code execution, package installation, file I/O

### Enterprise Features

#### Caching Layer (`cache/`)
- **Implementation**: Redis + in-memory LRU cache
- **Purpose**: Reduce API calls and improve response times
- **Cache Strategy**: MD5-based key generation, TTL-based expiration
- **Files**:
  - `cache/agent_cache.py`: AgentCache class with Redis integration

#### Load Balancing (`load_balancer/`)
- **Purpose**: Distribute agent workloads across multiple instances
- **Strategy**: Round-robin and least-connections algorithms
- **Files**:
  - `load_balancer/agent_balancer.py`: Agent load distribution logic

#### Monitoring (`monitoring/`)
- **Provider**: Prometheus metrics
- **Metrics Collected**:
  - Agent request counts (by agent, by status)
  - Request latency histograms
  - Active agent count (gauge)
  - Token usage (by model, by agent)
- **Files**:
  - `monitoring/metrics.py`: MetricsCollector class

#### Security (`security/`)
- **Components**:
  - **Key Management**: Encrypted API key storage (Fernet encryption)
  - **AWS Secrets Manager**: Integration for production key management
  - **Rate Limiting**: Per-agent request throttling
  - **Input Validation**: Sanitization and validation of user inputs
- **Files**:
  - `security/key_manager.py`: SecureKeyManager class
  - `security/rate_limiter.py`: Rate limiting implementation
  - `security/validator.py`: Input validation utilities

#### Optimization (`optimization/`)
- **Model Selection**: Cost-optimized model selection based on task requirements
- **Token Optimization**: Token counting and context window management
- **Files**:
  - `optimization/model_selector.py`: CostOptimizedModelSelector class
  - `optimization/token_optimizer.py`: Token usage optimization

#### Health Checks (`health/`)
- **Purpose**: System health monitoring and readiness checks
- **Files**:
  - `health/health_check.py`: Health check endpoints and logic

#### Utilities (`utils/`)
- **Connection Pooling**: Async HTTP connection management
- **Error Handling**: Production-grade error handling and logging
- **Files**:
  - `utils/connection_pooling.py`: Async connection pool
  - `utils/prod_error_handler.py`: Error handling decorators

#### Configuration (`config/`)
- **Environment-based Configuration**: Production settings management
- **Files**:
  - `config/production.py`: Production configuration

#### Logging (`logging_config.py`)
- **Format**: JSON-structured logging for production
- **Provider**: `pythonjsonlogger`
- **Features**: Structured logs, log levels, agent-specific logging

---

## Project Structure

```
mas/
├── main.py                          # Main entry point and agent definitions
├── prompts.py                       # Centralized prompt templates for agents
├── model_checker.py                 # Model capability detection and selection
├── context-engineering-workflow.py # Advanced context engineering workflow
├── logging_config.py                # Production logging configuration
├── Dockerfile                       # Production container definition
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── .gitignore                       # Git ignore patterns
│
├── cache/                           # Caching layer
│   └── agent_cache.py              # Redis + in-memory caching implementation
│
├── config/                          # Configuration management
│   └── production.py               # Production environment settings
│
├── deploy/                          # Deployment configurations
│   ├── docker-compose.yml          # Docker Compose for development
│   └── Dockerfile.dev              # Development container definition
│
├── health/                          # Health check system
│   └── health_check.py             # Health monitoring endpoints
│
├── load_balancer/                   # Load balancing
│   └── agent_balancer.py           # Agent workload distribution
│
├── monitoring/                      # Observability
│   └── metrics.py                  # Prometheus metrics collection
│
├── optimization/                    # Performance optimization
│   ├── model_selector.py           # Cost-optimized model selection
│   └── token_optimizer.py          # Token usage optimization
│
├── security/                        # Security features
│   ├── key_manager.py              # Secure API key management
│   ├── rate_limiter.py             # Request rate limiting
│   └── validator.py                # Input validation and sanitization
│
├── tests/                           # Test suite
│   ├── conftest.py                 # Pytest configuration and fixtures
│   ├── pytest.ini                  # Pytest settings
│   ├── capture_out_err.py          # Output capture utilities
│   ├── debug_utils.py              # Debugging helpers
│   ├── factories.py                # Test data factories (factory_boy)
│   ├── utils.py                    # Test utilities
│   │
│   ├── data/                       # Test data
│   │   └── test_cases.py          # Test case definitions
│   │
│   ├── integration/                # Integration tests
│   │   ├── test_multi_agent.py    # Multi-agent integration tests
│   │   └── test_tool_integration.py # Tool integration tests
│   │
│   ├── mock/                       # Mock objects
│   │   ├── llm_mock.py            # LLM API mocks
│   │   └── tool_mock.py           # Tool mocks
│   │
│   ├── performance/                # Performance tests
│   │   ├── test_load.py           # Load testing
│   │   └── test_memory.py         # Memory profiling
│   │
│   ├── unit/                       # Unit tests
│   │   ├── test_agents.py         # Agent unit tests
│   │   ├── test_tasks.py          # Task unit tests
│   │   └── test_tools.py          # Tool unit tests
│   │
│   ├── test_properties.py         # Property-based tests (Hypothesis)
│   └── test_snapshots.py          # Snapshot tests (Syrupy)
│
└── utils/                           # Utility modules
    ├── connection_pooling.py       # Async HTTP connection pooling
    └── prod_error_handler.py       # Production error handling
```

### Key Files Description

#### `main.py`
- **Purpose**: System entry point and agent orchestration
- **Contents**:
  - Agent definitions (InteractiveChatAgent, PlannerAgent, CoderAgent, TesterAgent, DeployerAgent)
  - Task definitions with workflow dependencies
  - Tool implementations (internet_search_tool, code_interpreter, create_chat_interface)
  - PraisonAIAgents team initialization
  - Process workflow configuration
  - Logging and error handling setup

#### `prompts.py`
- **Purpose**: Centralized prompt engineering
- **Contents**:
  - `PLANNER_PROMPT`: Instructions for JSON specification generation
  - `CODER_PROMPT`: Code generation instructions
  - `CODER_REFINEMENT_PROMPT`: Code correction instructions
  - `TESTER_PROMPT`: Testing and validation instructions
- **Design Pattern**: Template-based prompts with placeholders for dynamic content

#### `context-engineering-workflow.py`
- **Purpose**: Advanced context engineering demonstration
- **Features**:
  - ContextAgent integration
  - Codebase analysis
  - Context-enhanced agent prompts
  - Validation loops

#### `model_checker.py`
- **Purpose**: Model capability detection and selection
- **Features**:
  - Model capability analysis
  - Cost comparison
  - Task-specific model recommendations

---

## Installation & Configuration

### Prerequisites

- **Python**: 3.9 or higher (3.11 recommended)
- **OpenAI API Key**: For OpenAI-compatible models
- **E2B API Key**: For code interpreter sandbox
- **Redis** (optional): For distributed caching
- **Docker** (optional): For containerized deployment

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd mas
```

### Step 2: Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the project root:

```env
# Required: LLM API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1  # Update for compatible APIs

# Required: Code Interpreter
E2B_API_KEY=your_e2b_api_key_here

# Optional: Redis (for distributed caching)
REDIS_URL=redis://localhost:6379/0

# Optional: AWS Secrets Manager (for production key management)
AWS_REGION=us-east-1
USE_AWS_SECRETS=false

# Optional: Encryption (auto-generated if not provided)
ENCRYPTION_KEY=your_fernet_encryption_key_here

# Optional: Monitoring
PROMETHEUS_PORT=9090
```

**Note**: The `OPENAI_BASE_URL` should be updated according to your LLM provider:
- OpenAI: `https://api.openai.com/v1`
- Anthropic: `https://api.anthropic.com/v1`
- Custom providers: Check provider documentation

### Step 5: Verify Installation

```bash
python -c "import praisonaiagents; print('Installation successful')"
```

---

## Usage

### Basic Usage

#### Method 1: Direct Execution

   ```bash
   python main.py
   ```

This will:
1. Initialize all agents
2. Start the interactive chat interface
3. Execute the hierarchical workflow
4. Generate code, tests, and deployment configurations

#### Method 2: PraisonAI CLI

  ```bash
# Initialize a new multi-agent system
praisonai --init "Create a stock analysis system with research and reporting agents"

# Run with specific framework
praisonai --init "Your prompt" --framework crew
praisonai --init "Your prompt" --framework autogen

# Execute using agents.yaml
praisonai
```

### Advanced Usage

#### Custom Agent Configuration

Modify agent definitions in `main.py`:

```python
CustomAgent = Agent(
    name="CustomAgent",
    role="Custom Role",
    goal="Custom goal",
    backstory="Custom backstory",
    llm="gpt-4",  # Use different model
    api_key=api_key,
    reasoning_steps=5,  # Increase reasoning depth
    tools=[custom_tool],
    verbose=True
)
```

#### Custom Workflow

Create custom task sequences:

```python
custom_workflow = PraisonAIAgents(
    agents=[Agent1, Agent2, Agent3],
    tasks=[task1, task2, task3],
    process="sequential",  # or "hierarchical", "parallel"
    max_retries=5,
    manager_llm="gpt-4",
    verbose=True
)
```

#### Using Context Engineering

```python
from context_engineering_workflow import ContextEngineeringWorkflow

workflow = ContextEngineeringWorkflow(
    project_path="./my_project",
    llm="gpt-4o-mini"
)

result = workflow.execute("Create a REST API for user management")
```

---

## Technical Specifications

### Agent Communication Protocol

Agents communicate through:
1. **Task Context**: Shared context passed between tasks
2. **Output Files**: Structured markdown/JSON files
3. **Decision Tasks**: Conditional routing based on quality gates

### Task Types

1. **Standard Task**: Sequential execution with context passing
2. **Loop Task**: Iterative execution until condition met
3. **Decision Task**: Conditional routing based on output evaluation

### Output Formats

#### Planning Output (`Planning.md`)
```markdown
# Implementation Plan

## Project: [project_name]

## Agents
- [Agent descriptions]

## Tools
- [Tool specifications]

## Workflow
1. Step 1
2. Step 2
...

## Dependencies
- package1
- package2
```

#### Code Output (`Code.md`)
- Generated Python files
- Code explanations
- Execution instructions

#### Test Output (`Test.md`)
- Test results
- Confidence scores
- Error reports
- Suggestions

### API Integration

#### OpenAI-Compatible APIs

The system supports any OpenAI-compatible API by configuring `OPENAI_BASE_URL`:

```python
# Example: Using Anthropic Claude
OPENAI_BASE_URL=https://api.anthropic.com/v1

# Example: Using local LLM
OPENAI_BASE_URL=http://localhost:8000/v1
```

#### Model Selection

The system includes intelligent model selection:

```python
from model_checker import ModelCapabilities

capabilities = ModelCapabilities()
best_model = capabilities.recommend_model({
    "type": "code_generation",
    "complexity": "high",
    "context_needed": 8000
})
```

---

## Research Contributions

### Hierarchical Multi-Agent Orchestration

This system demonstrates a **hierarchical process flow** with quality gates, enabling:
- Iterative refinement through decision tasks
- Quality control at multiple stages
- Context preservation across agent boundaries

### Context Engineering Integration

The `context-engineering-workflow.py` demonstrates advanced context engineering:
- Codebase analysis for context generation
- Context-enhanced agent prompts
- Validation loops for quality assurance

### Enterprise-Grade Features

Production-ready features for research and deployment:
- **Caching**: Reduces API costs and improves latency
- **Monitoring**: Prometheus metrics for observability
- **Security**: Encrypted key management, rate limiting
- **Optimization**: Cost-aware model selection

### Testing Framework

Comprehensive test suite including:
- **Unit Tests**: Agent, task, and tool isolation
- **Integration Tests**: Multi-agent workflows
- **Performance Tests**: Load and memory profiling
- **Property-Based Tests**: Hypothesis-based testing
- **Snapshot Tests**: Regression testing with Syrupy

---

## Performance & Optimization

### Caching Strategy

- **Local Cache**: In-memory LRU cache for fast access
- **Redis Cache**: Distributed caching for multi-instance deployments
- **TTL**: Configurable time-to-live (default: 3600 seconds)
- **Cache Keys**: MD5 hash of agent name + input text

### Model Selection Optimization

The `CostOptimizedModelSelector` selects models based on:
- Task type requirements
- Cost constraints
- Capability matching

### Token Optimization

- Token counting using `tiktoken`
- Context window management
- Prompt optimization

### Load Balancing

- Round-robin distribution
- Least-connections algorithm
- Agent-specific routing

---

## Security

### API Key Management

- **Encryption**: Fernet symmetric encryption
- **AWS Secrets Manager**: Production-grade secret storage
- **Environment Variables**: Secure key storage

### Rate Limiting

- Per-agent request throttling
- Configurable rate limits
- Sliding window algorithm

### Input Validation

- Sanitization of user inputs
- SQL injection prevention
- XSS protection
- Command injection prevention

### Code Execution Security

- **E2B Sandbox**: Fully isolated execution environment
- **No Network Access**: Sandboxed network isolation
- **Resource Limits**: CPU and memory constraints

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test categories
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/performance/   # Performance tests

# Run with verbose output
pytest -v

# Run with specific markers
pytest -m "not slow"        # Skip slow tests
```

### Test Structure

- **Unit Tests**: Fast, isolated component tests
- **Integration Tests**: Multi-agent workflow tests
- **Performance Tests**: Load and memory tests
- **Property-Based Tests**: Hypothesis-generated test cases
- **Snapshot Tests**: Regression testing

### Test Utilities

- **Factories**: `factory_boy` for test data generation
- **Mocks**: LLM and tool mocks for isolated testing
- **Fixtures**: Reusable test configurations

---

## Deployment

### Docker Deployment

#### Production

```bash
docker build -t mas:latest .
docker run -p 8000:8000 --env-file .env mas:latest
```

#### Development

```bash
cd deploy
docker-compose up
```

### Kubernetes Deployment

The system can be deployed to Kubernetes with:
- ConfigMaps for configuration
- Secrets for API keys
- Deployments for agent instances
- Services for load balancing

### Health Checks

Health check endpoint: `http://localhost:8000/health`

Returns:
```json
{
  "status": "healthy",
  "agents": ["agent1", "agent2", ...],
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Monitoring

Prometheus metrics available at: `http://localhost:9090/metrics`

Key metrics:
- `agent_requests_total`: Total requests by agent and status
- `agent_request_duration_seconds`: Request latency
- `active_agents`: Number of active agents
- `token_usage_total`: Token usage by model and agent

---

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Install development dependencies: `pip install -r requirements.txt`
4. Run tests: `pytest`
5. Format code: `black .`
6. Lint code: `pylint *.py`
7. Commit changes: `git commit -m 'Add amazing feature'`
8. Push to branch: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Code Style

- **Formatter**: Black (line length: 88)
- **Linter**: Pylint
- **Type Hints**: Use type hints for all functions
- **Docstrings**: Google-style docstrings

### Testing Requirements

- All new features must include tests
- Maintain >80% code coverage
- All tests must pass before merging

---

## License

MIT License

Copyright (c) 2024 Mukundan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

---

## Acknowledgments

### Frameworks & Libraries

- **[PraisonAI Agents](https://github.com/MervinPraison/PraisonAI)**: Multi-agent orchestration framework
- **[OpenAI API](https://openai.com)**: Language model API
- **[E2B Code Interpreter](https://e2b.dev/)**: Sandboxed code execution
- **[DuckDuckGo Search](https://duckduckgo.com/)**: Internet search functionality

### Research & Development

This system was developed as part of research into:
- Multi-agent systems and orchestration
- Automated software development
- AI-powered code generation
- Hierarchical agent workflows

---

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/mukundan1/MAS4MAS/issues)
- **Author**: Mukundan
- **Repository**: [MAS4MAS](https://github.com/mukundan1/MAS4MAS)

---

**Made with ❤️ for the AI Research Community**
