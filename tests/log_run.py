from datetime import datetime

with open("run_log.txt", "a") as f:
    f.write(f"Script ran at {datetime.utcnow()} UTC\n")

print("Logged run time.")