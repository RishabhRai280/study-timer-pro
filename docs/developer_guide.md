# Developer Guide - Study Timer Pro

## 📌 Table of Contents
1. [Introduction](#introduction)  
2. [Project Structure](#project-structure)  
3. [Setting Up the Development Environment](#setting-up-the-development-environment)  
4. [Running the Application](#running-the-application)  
5. [Understanding the Core Modules](#understanding-the-core-modules)  
6. [Adding New Features](#adding-new-features)  
7. [Code Style Guidelines](#code-style-guidelines)  
8. [Testing the Application](#testing-the-application)  
9. [Debugging & Logging](#debugging--logging)  
10. [Contribution Guidelines](#contribution-guidelines)  

---

## 🚀 Introduction  
Welcome to the **Study Timer Pro** Developer Guide.  

This document provides an in-depth explanation of the **project structure**, **core functionality**, **development workflow**, and **best practices** for contributing.  

**Prerequisites:**  
- **Python 3.8+**  
- **Basic knowledge of Git, Tkinter (or PyQt), and OOP**  

---

## 📂 Project Structure

```plaintext
study-timer-pro/
├── src/
│   ├── main.py                   # Main application entry point
│   ├── ui/                        # User interface components
│   │   ├── main_window.py         # Main window implementation
│   │   ├── timer_tab.py           # Timer tab UI
│   │   ├── analytics_tab.py       # Analytics tab UI
│   │   ├── settings_tab.py        # Settings tab UI
│   │   └── components/            # Reusable UI components
│   ├── core/                      # Core functionality
│   │   ├── timer.py               # Timer logic
│   │   ├── app_blocker.py         # App blocking functionality
│   │   ├── website_blocker.py     # Website blocking functionality
│   │   └── statistics.py          # Statistics tracking
│   ├── utils/                     # Utility modules
│   │   ├── settings.py            # Settings management
│   │   ├── notifications.py       # Notification system
│   │   └── sound_manager.py       # Sound management
│   └── resources/                 # Static resources
│       ├── sounds/                # Sound files
│       ├── images/                # Image resources
│       └── themes/                # Theme definitions
├── docs/                          # Documentation files
│   ├── user_guide.md              # User documentation
│   ├── developer_guide.md         # Developer documentation
│   └── screenshots/               # UI screenshots
├── tests/                         # Unit tests
├── requirements.txt               # Dependencies list
├── setup.py                       # Installation script
└── README.md                      # Project overview
```

---

## 🛠 Setting Up the Development Environment

### **🔹 Steps to Setup**
1. **Clone the repository:**
   ```bash
   git clone https://github.com/RishabhRai280/study-timer-pro.git
   cd study-timer-pro
   ```

2. **Create a virtual environment:**
   ```shellscript
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **Windows:** `venv\Scripts\activate`
   - **macOS/Linux:** `source venv/bin/activate`

4. **Install dependencies:**
   ```shellscript
   pip install -e .
   ```

---

## ▶️ Running the Application
After setting up, run the app with:
```shellscript
python src/main.py
```

---

## 🏗 Understanding the Core Modules  

### **🔹 `core/timer.py`**
Handles **Pomodoro timer logic**.  
```python
class Timer:
    """Handles Pomodoro timer logic."""
    
    def __init__(self, duration):
        self.duration = duration
    
    def start(self):
        """Starts the timer countdown."""
        pass
```

### **🔹 `core/app_blocker.py`**
Blocks distracting applications during study sessions.

### **🔹 `core/website_blocker.py`**
Manages website blocking functionality.

### **🔹 `core/statistics.py`**
Stores **study session data** and generates **analytics**.

---

## 🎯 Adding New Features
To add a **new feature**:
1. **Create a new branch:**
   ```bash
   git checkout -b feature-new-feature
   ```
2. **Implement your changes inside `src/`.**
3. **Add necessary unit tests** in `tests/`.
4. **Run tests using:**
   ```shellscript
   pytest tests/
   ```
5. **Commit changes:**
   ```bash
   git commit -m "Added new feature"
   ```
6. **Push and create a pull request.**

---

## ✨ Code Style Guidelines
- Follow **PEP 8** standards.  
- Use **meaningful variable names**.  
- Keep functions **short & modular**.  
- Document functions with **docstrings**:
  ```python
  def example_function(param1: int) -> str:
      """
      Brief description of function.

      :param param1: Description of parameter
      :return: Description of return value
      """
      pass
  ```

---

## 🧪 Testing the Application  
We use **pytest** for testing.  

### **Running Tests**
```shellscript
pytest tests/
```

### **Writing New Tests**
1. **Create a test file** in `tests/`, e.g., `test_timer.py`.
2. **Write test cases** using `pytest`:
   ```python
   import pytest
   from src.core.timer import Timer

   def test_timer_initialization():
       timer = Timer(25)
       assert timer.duration == 25
   ```
3. **Run the test:**
   ```shellscript
   pytest tests/test_timer.py
   ```

---

## 🛠 Debugging & Logging
We use the **built-in `logging` module**.

### **Adding Logging**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Timer started")
```

---

## 📜 Contribution Guidelines
- **Fork the repository**.  
- Use **feature branches** for new functionality.  
- Ensure all code is **well-documented**.  
- Write **unit tests** before submitting a PR.  
- Follow **code formatting standards**.  
- **Submit a pull request** and request a review.

---

## 🔥 What's Improved?  
✔ Updated **installation** steps with `venv`  
✔ Clear **activation steps** for **Windows/macOS/Linux**  
✔ Used `pip install -e .` for development mode installation  
✔ **Improved structure & readability**  
✔ **Enhanced logging, testing, and debugging sections**  

---