import os

# Correct path since you are inside CRM
tests_folder = "tests"

# Files to create
files = [
    "__init__.py",
    "conftest.py",
    "test_users.py",
    "test_clients.py",
    "test_tasks.py",
    "test_payments.py"
]

# Ensure tests folder exists
os.makedirs(tests_folder, exist_ok=True)

# Create files
for file in files:
    file_path = os.path.join(tests_folder, file)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            if file == "__init__.py":
                f.write("# Makes tests a Python package\n")
            elif file == "conftest.py":
                f.write("# DB + FastAPI TestClient setup will go here\n")
            else:
                f.write(f"# Tests for {file.replace('test_','').replace('.py','').title()} module\n")
        print(f"Created: {file_path}")
    else:
        print(f"Skipped (already exists): {file_path}")

print("\n✅ All test files are ready in tests/")
