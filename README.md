# Backend Setup Instructions

Before starting the backend development, follow these steps to set up and activate a virtual environment:

## 🔧 Setting up the Virtual Environment

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```

   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. ✅ Make sure to add the `venv` directory to your `.gitignore` file to avoid committing environment-specific files to version control.

## 📄 Example `.gitignore` entry:
```
venv/
```


## 🛠️ Log File Generation with Faker

To simulate log data for backend development, follow these steps:

### 📦 1. Install Faker

Make sure your virtual environment is activated, then run:

```bash
pip install faker
```

### 📄 2. Generate Log Files

Run the following script to extract/generate log files:

```bash
python extract/generator.py
```

This will create log files in the `/extract/raw_logs/` directory.

### 🚫 3. Update `.gitignore`

To avoid committing generated log files, add the following entry to your `.gitignore`:

```
/extract/raw_logs/
```

