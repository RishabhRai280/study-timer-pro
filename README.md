# Study Timer Pro

## 🚀 Introduction
**Study Timer Pro** is an advanced **Pomodoro timer** with built-in productivity tools. It helps users **manage study sessions**, **block distractions**, and **track progress** with detailed analytics.  

---

## 📌 Features
✅ **Customizable Timer** – Adjustable focus & break durations  
✅ **App & Website Blocking** – Prevent distractions during study sessions  
✅ **Task Management** – Built-in to-do list with priority levels  
✅ **Session Analytics** – Track daily, weekly, and monthly study trends  
✅ **Motivation Features** – Streaks, quotes, and goal tracking  
✅ **Custom Themes & Sounds** – Personalize your study environment  

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

## 🛠 Installation

### **🔹 Prerequisites**
- **Python 3.8+**  
- **Tkinter** (Usually included with Python)  
- **Administrator Privileges** (For app & website blocking features)  

### **🔹 Development Environment Setup**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RishabhRai280/study-timer-pro
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

5. **Run the application:**
   ```shellscript
   python src/main.py
   ```

---

## 🎯 Usage Guide

### **Timer**
- Set **focus and break durations** in the **Timer Tab**  
- Click **Start Timer** to begin  
- **Session progress** is visually indicated  
- Notifications alert when a session ends  

### **Analytics**
- Track total **study hours**  
- View **progress graphs** (daily, weekly, monthly)  
- Maintain **streaks** and set **goals**  

### **Blocking Distractions**
- Add **apps & websites** to the **blocklist**  
- The blocker activates **automatically** during focus sessions  

---

## 🎹 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + N` | Start new session |
| `Ctrl + P` | Pause session |
| `Ctrl + S` | Stop timer |
| `Ctrl + A` | Open Analytics tab |
| `Ctrl + Shift + B` | Toggle blocker |

---

## 🧪 Running Tests
Ensure everything works correctly by running:
```shellscript
pytest tests/
```

---

## 💡 Contributing
1. **Fork the repository**  
2. **Create a feature branch**  
   ```bash
   git checkout -b feature-new-feature
   ```
3. **Commit and push your changes**  
   ```bash
   git commit -m "Added new feature"
   git push origin feature-new-feature
   ```
4. **Open a pull request**  

---

## 🛠 Support & Feedback
- **Report issues**: Open a GitHub issue  
- **Feature requests**: Submit an issue or PR  
- **Contributors**: All contributions are welcome! 🎉  

---