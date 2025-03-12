# User Guide - Study Timer Pro  

## 📌 Table of Contents  
1. [Introduction](#introduction)  
2. [Installation](#installation)  
3. [Launching the Application](#launching-the-application)  
4. [Using the Application](#using-the-application)  
   - [Timer Tab](#timer-tab)  
   - [Analytics Tab](#analytics-tab)  
   - [Settings Tab](#settings-tab)  
   - [Blocking Distractions](#blocking-distractions)  
5. [Keyboard Shortcuts](#keyboard-shortcuts)  
6. [Troubleshooting](#troubleshooting)  
7. [Frequently Asked Questions](#frequently-asked-questions)  
8. [Support & Feedback](#support--feedback)  

---

## 🚀 Introduction  
**Study Timer Pro** is a **Pomodoro-based** productivity application designed to **enhance focus and eliminate distractions**.  

This guide explains **how to install, configure, and use** the app effectively.  

---

## 🛠 Installation  

### **🔹 Prerequisites**  
- **Python 3.8+**  
- **Tkinter** (Usually included with Python)  
- **Administrator Privileges** (For app & website blocking features)  

### **🔹 Steps to Install**  
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

## ▶️ Launching the Application  
To start **Study Timer Pro**, run:  
```shellscript
python src/main.py
```

---

## 🎯 Using the Application  

### 🔹 Timer Tab  
1. **Set the session duration** (Default: 25 minutes).  
2. Click **Start Timer** to begin.  
3. A **progress bar** shows the remaining time.  
4. A **notification** alerts you when the session ends.  
5. Click **Stop** to manually end the session.  

---

### 🔹 Analytics Tab  
The **Analytics** tab helps track your study sessions:  
- **Total Focus Time** – Time spent in focus mode.  
- **Session Count** – Number of completed sessions.  
- **Daily/Weekly Trends** – Graphs displaying study performance.  

---

### 🔹 Settings Tab  
Customize **Study Timer Pro** through the **Settings** tab:  
- **Work Duration** – Adjust focus session length.  
- **Break Duration** – Set short/long break times.  
- **Notification Sounds** – Enable or disable sound alerts.  
- **Themes** – Choose a color theme.  

---

### 🔹 Blocking Distractions  
Stay focused by **blocking distracting apps & websites**.  

#### **🔸 App Blocker**  
1. Click **App Blocker** in Settings.  
2. Add applications to the blocklist.  
3. Blocked apps will **close automatically** when a session starts.  

#### **🔸 Website Blocker**  
1. Enter **website URLs** in the blocker section.  
2. Click **Enable Blocking**.  
3. Websites remain blocked **until the session ends**.  

> **⚠ Note:** **Website blocking requires administrator permissions.**  

---

## 🎹 Keyboard Shortcuts  

| Shortcut | Action |  
|----------|--------|  
| `Ctrl + N` | Start a new timer session |  
| `Ctrl + P` | Pause the current session |  
| `Ctrl + S` | Stop the timer |  
| `Ctrl + A` | Open Analytics tab |  
| `Ctrl + T` | Open Timer tab |  
| `Ctrl + Shift + B` | Enable/Disable Blocking |  

---

## 🛠 Troubleshooting  

| Issue | Solution |  
|-------|----------|  
| **App won’t start** | Ensure Python is installed and dependencies are installed (`pip install -r requirements.txt`). |  
| **Timer isn’t working** | Restart the app and check the terminal for errors. |  
| **Website blocking isn’t working** | Ensure you have **admin privileges** when running the app. |  
| **No sound notifications** | Check if sound is **enabled in Settings**. |  

---

## ❓ Frequently Asked Questions  

### **1. Can I customize the timer durations?**  
Yes! You can set custom focus and break durations in the **Settings tab**.  

### **2. Will the app block websites in all browsers?**  
The website blocker modifies the system **hosts file**. Some browsers may require **cache clearing** for changes to apply.  

### **3. Can I export my study data?**  
Currently, **data export is not supported**. This feature may be added in future updates.  

---

## 💬 Support & Feedback  
If you encounter issues or have suggestions, please **open an issue** on our **[GitHub repository](https://github.com/RishabhRai280/study-timer-pro)**.  

---