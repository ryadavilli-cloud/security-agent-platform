# security-agent-platform
Project work for building a security agent for analyzing code base for security threats. 

## Local Development Setup

### Prerequisites
- Python 3.11 or 3.12
- Windows/Linux/Mac

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/security-agent-platform.git
cd security-agent-platform
```

2. Create virtual environment:
```bash
python -m venv .venv
```

3. Activate virtual environment:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Configure environment:
```bash
# Copy template
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env with your API keys
```

6. Run smoke test:
```bash
python tests/smoke_test.py
```

### Verified Working Environment
- Python 3.11+
- LangChain 0.3.13
- LangGraph 0.2.58
- CrewAI 0.203.1
- All dependencies tested on Windows 