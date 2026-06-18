# Exercise 01: AI-Assisted Development Practice

## Overview

This exercise gives you hands-on practice with AI-assisted development workflows. You'll scaffold a project, debug errors, refactor code, and write tests — all using AI assistance.

**Time**: 3-4 hours
**Tools needed**: Any AI coding assistant (Claude, Gemini, Cursor, Copilot)

---

## Part 1: Project Scaffolding with AI (45 min)

### Task

Use AI to scaffold a complete Python project for a **Task Management API**.

### Requirements

Your API should:
- Use FastAPI with async endpoints
- Have SQLAlchemy 2.0 async ORM with SQLite
- Include Pydantic v2 models
- Support CRUD operations for tasks and projects
- Have JWT authentication
- Include pytest tests
- Have a Dockerfile and docker-compose.yml

### Steps

1. **Write a scaffolding prompt** that includes all requirements above
2. **Generate the project** using your AI assistant
3. **Review the generated structure** — is it clean? Logical?
4. **Run the project** — does it start without errors?
5. **Customize** — add or modify anything that doesn't fit your style

### Deliverables

- Working project directory with all files
- Scaffolding prompt you used (save to a notes file)
- Screenshot or output showing the server starts successfully

### Evaluation Criteria

- [ ] Project structure is logical and follows clean architecture
- [ ] All dependencies are listed in requirements.txt or pyproject.toml
- [ ] Server starts without import errors
- [ ] Database tables are created on startup
- [ ] Docker configuration works

---

## Part 2: Debugging with AI (45 min)

### Task

Debug 5 Python errors using AI assistance. For each error, practice the full debugging workflow.

### Error 1: Import Error

```python
# debug_me.py
from mymodule import MyClass
import sys
sys.path.append('/wrong/path')
obj = MyClass()
obj.do_something()
```

**Error output:**
```
ModuleNotFoundError: No module named 'mymodule'
```

**Your task**: Use AI to identify why this fails and fix it. Consider:
- Is sys.path manipulation the right approach?
- What are alternatives?
- How do you structure imports properly?

### Error 2: Type Error

```python
def calculate_average(numbers: list[int]) -> float:
    return sum(numbers) / len(numbers)

result = calculate_average("not a list")
print(result)
```

**Error output:**
```
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

**Your task**: Use AI to:
1. Explain why the error happens (trace through the execution)
2. Fix the function to handle invalid input
3. Write tests for the fixed function

### Error 3: Attribute Error

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

user = User("Alice", "alice@example.com")
print(user.username)
```

**Error output:**
```
AttributeError: 'User' object has no attribute 'username'
```

**Your task**: Use AI to suggest multiple approaches to fix this, including:
- Adding the missing attribute
- Using __getattr__ for flexibility
- Using Pydantic models

### Error 4: Concurrent Error

```python
import asyncio

async def fetch_data(url):
    import requests
    response = requests.get(url)
    return response.json()

async def main():
    urls = ["https://api.example.com/1", "https://api.example.com/2"]
    results = [await fetch_data(url) for url in urls]
    print(results)

asyncio.run(main())
```

**Error output:**
```
# This runs sequentially, not concurrently. No error, but it's slow.
```

**Your task**: Use AI to:
1. Identify the performance issue (not a bug, but a design flaw)
2. Refactor to use asyncio.gather() or aiohttp
3. Explain the difference

### Error 5: ML Error

```python
import torch

model = torch.nn.Linear(10, 5)
x = torch.randn(3, 10)
y = torch.randn(3, 5)

loss = torch.nn.MSELoss()
output = loss(x, y)
output.backward()  # This line fails
```

**Error output:**
```
RuntimeError: element 0 of tensors does not require grad and does not have a grad_fn
```

**Your task**: Use AI to:
1. Explain why gradients aren't computed
2. Fix the code
3. Explain when you'd want requires_grad=True vs False

### Deliverables

For each error:
- The AI prompt you used
- The AI's explanation
- The fixed code
- What you learned

---

## Part 3: Refactoring with AI (60 min)

### Task

Refactor a messy codebase using AI assistance.

### The Messy Code

Create a file called `messy_code.py`:

```python
import os
import sys
import json
import sqlite3
from datetime import datetime

# This is a "task manager" that needs serious refactoring

def connect():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks 
                 (id INTEGER PRIMARY KEY, title TEXT, done INTEGER, 
                  project TEXT, created TEXT, priority INTEGER)''')
    conn.commit()
    return conn

def add(title, project="default", priority=1):
    conn = connect()
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT INTO tasks (title, done, project, created, priority) VALUES (?, 0, ?, ?, ?)",
              (title, project, now, priority))
    conn.commit()
    conn.close()
    return "Task added!"

def list_tasks(project=None, show_done=True):
    conn = connect()
    c = conn.cursor()
    if project and show_done:
        c.execute("SELECT * FROM tasks WHERE project=?", (project,))
    elif project and not show_done:
        c.execute("SELECT * FROM tasks WHERE project=? AND done=0", (project,))
    elif not project and not show_done:
        c.execute("SELECT * FROM tasks WHERE done=0")
    else:
        c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    for t in tasks:
        status = "DONE" if t[2] else "TODO"
        print(f"[{status}] {t[1]} (project: {t[3]}, priority: {t[5]}, created: {t[4]})")

def complete(task_id):
    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
    conn.commit()
    affected = c.rowcount
    conn.close()
    if affected:
        return "Task completed!"
    else:
        return "Task not found!"

def delete(task_id):
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    affected = c.rowcount
    conn.close()
    if affected:
        return "Task deleted!"
    else:
        return "Task not found!"

def stats():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tasks")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE done=1")
    done = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tasks WHERE done=0")
    pending = c.fetchone()[0]
    conn.close()
    print(f"Total: {total}, Done: {done}, Pending: {pending}")

def search(query):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE title LIKE ?", (f"%{query}%",))
    tasks = c.fetchall()
    conn.close()
    for t in tasks:
        status = "DONE" if t[2] else "TODO"
        print(f"[{status}] {t[1]} (id: {t[0]})")

# CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python messy_code.py [add|list|complete|delete|stats|search] [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        title = sys.argv[2] if len(sys.argv) > 2 else "Untitled"
        project = sys.argv[3] if len(sys.argv) > 3 else "default"
        priority = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        print(add(title, project, priority))
    
    elif cmd == "list":
        project = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(project)
    
    elif cmd == "complete":
        task_id = int(sys.argv[2])
        print(complete(task_id))
    
    elif cmd == "delete":
        task_id = int(sys.argv[2])
        print(delete(task_id))
    
    elif cmd == "stats":
        stats()
    
    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        search(query)
    
    else:
        print(f"Unknown command: {cmd}")
```

### Refactoring Steps

1. **Analyze the code with AI** — ask for a code review identifying all issues
2. **Create a refactoring plan** — ask AI to propose a clean architecture
3. **Apply refactoring iteratively**:
   - Extract database operations into a repository class
   - Add type hints throughout
   - Create proper models (dataclasses or Pydantic)
   - Add error handling
   - Create a proper CLI with argparse or click
   - Add logging instead of print statements
4. **Verify behavior** — write tests to confirm the refactored code works the same
5. **Measure improvement** — ask AI to evaluate code quality before/after

### Deliverables

- Original `messy_code.py`
- Refactored version with proper architecture
- Test file that covers all functionality
- Summary of changes made and why

### Evaluation Criteria

- [ ] Code follows SOLID principles
- [ ] Proper separation of concerns (database, business logic, CLI)
- [ ] Type hints throughout
- [ ] Error handling for all operations
- [ ] Tests cover all functions
- [ ] No duplicate code
- [ ] Clear naming and documentation

---

## Part 4: Writing Tests with AI (45 min)

### Task

Given an existing codebase, use AI to generate comprehensive tests.

### The Code to Test

Create `weather_service.py`:

```python
import requests
from datetime import datetime, timedelta
from typing import Optional
import json
import os

class WeatherService:
    def __init__(self, api_key: str, cache_dir: str = ".weather_cache"):
        self.api_key = api_key
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_current_weather(self, city: str) -> dict:
        cache_file = os.path.join(self.cache_dir, f"{city}_current.json")
        
        if os.path.exists(cache_file):
            mtime = os.path.getmtime(cache_file)
            if datetime.now().timestamp() - mtime < 1800:  # 30 min cache
                with open(cache_file) as f:
                    return json.load(f)
        
        response = requests.get(
            f"https://api.weatherapi.com/v1/current.json",
            params={"key": self.api_key, "q": city}
        )
        response.raise_for_status()
        data = response.json()
        
        with open(cache_file, "w") as f:
            json.dump(data, f)
        
        return data
    
    def get_forecast(self, city: str, days: int = 3) -> dict:
        if days < 1 or days > 10:
            raise ValueError("Days must be between 1 and 10")
        
        response = requests.get(
            f"https://api.weatherapi.com/v1/forecast.json",
            params={"key": self.api_key, "q": city, "days": days}
        )
        response.raise_for_status()
        return response.json()
    
    def compare_cities(self, city1: str, city2: str) -> dict:
        weather1 = self.get_current_weather(city1)
        weather2 = self.get_current_weather(city2)
        
        temp1 = weather1["current"]["temp_c"]
        temp2 = weather2["current"]["temp_c"]
        
        return {
            "city1": {"name": city1, "temp_c": temp1},
            "city2": {"name": city2, "temp_c": temp2},
            "warmer": city1 if temp1 > temp2 else city2,
            "difference": abs(temp1 - temp2)
        }
    
    def is_rain_expected(self, city: str, hours: int = 24) -> bool:
        forecast = self.get_forecast(city, days=1)
        hourly = forecast["forecast"]["forecastday"][0]["hour"]
        
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)
        
        for hour_data in hourly:
            hour_time = datetime.strptime(hour_data["time"], "%Y-%m-%d %H:%M")
            if now <= hour_time <= cutoff:
                if hour_data["chance_of_rain"] > 50:
                    return True
        return False
```

### Testing Tasks

1. **Unit tests** — test each method in isolation (mock the API calls)
2. **Integration tests** — test the flow from request to response
3. **Edge cases** — empty city names, network failures, invalid API keys
4. **Cache tests** — verify caching works correctly
5. **Error handling tests** — verify proper exceptions are raised

### Deliverables

- `test_weather_service.py` with comprehensive tests
- Tests should be runnable with `pytest`
- Aim for >90% code coverage

---

## Bonus: Build a Complete App (60 min)

### Task

Build a **Markdown Note-Taking App** using an AI-assisted workflow.

### Features

- Create, read, update, delete notes
- Each note has: title, content (markdown), tags, created_at, updated_at
- Search notes by title or content
- Filter notes by tag
- Export notes to markdown files
- Local storage (SQLite or JSON file)

### Workflow

1. **Plan**: Ask AI to design the architecture (suggest file structure, classes, API)
2. **Scaffold**: Generate the project skeleton
3. **Implement core**: Build CRUD operations with AI assistance
4. **Add features**: Search, filter, export
5. **Test**: Write tests for all functionality
6. **Polish**: Add error handling, input validation, clean CLI

### Tech Stack Options

Choose one:
- **CLI app**: Python with Click/Typer + Rich for pretty output
- **Web app**: FastAPI + Jinja2 templates + HTMX
- **Desktop**: PyQt6 or Tkinter

### Deliverables

- Working application with all features
- README.md explaining how to use it
- Tests covering core functionality
- Brief write-up of how you used AI during development

---

## Submission Checklist

- [ ] Part 1: Scaffolded project runs successfully
- [ ] Part 2: All 5 errors debugged with documentation
- [ ] Part 3: Messy code refactored with tests
- [ ] Part 4: Weather service tests written and passing
- [ ] Bonus: Complete app built and functional (if attempted)

## Reflection Questions

After completing the exercise, answer these:

1. When was AI most helpful? When was it least helpful?
2. How did your prompting quality change during the exercise?
3. What would you do differently next time?
4. How do you balance speed (AI-generated) vs understanding (writing it yourself)?
5. What tasks are still better done manually?
