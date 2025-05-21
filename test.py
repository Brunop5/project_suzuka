import subprocess

result = subprocess.run(["firefox", "--version"], capture_output=True, text=True)
print("Firefox version:", result.stdout.strip())