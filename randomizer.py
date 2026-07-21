import random
import os
import time
import subprocess

def run_git_command(command):
    """Helper to run git commands and log output."""
    try:
        # We use shell=True to allow string commands, but be careful with inputs
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {command}")
        print(f"Stderr: {e.stderr}")

def multi_commit_randomizer(filename):
    # 1. Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    # 2. Human-like logic: 5% chance to skip the day entirely to look natural
    if random.random() < 0.05:
        print("Taking a rest day. No commits today.")
        return

    # 3. Determine number of commits (1 to 30)
    iterations = random.randint(1, 30)
    print(f"Today's Goal: {iterations} commits.")

    # Create file if it doesn't exist
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("Streak Start Log\n")

    for i in range(1, iterations + 1):
        # Read existing lines
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Add unique data so Git sees a change
        # Using a timestamp + random number to guarantee uniqueness
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        random_suffix = random.getrandbits(16)
        new_entry = f"Sequence {i}/{iterations} | {timestamp} | ID: {random_suffix}\n"
        lines.append(new_entry)
        
        # Shuffle for "random" file changes
        random.shuffle(lines)

        # Write back (keeping last 50 lines to prevent file bloat)
        with open(file_path, 'w') as file:
            file.writelines(lines[-50:])

        # 4. Commit inside the loop
        # [skip ci] prevents the action from triggering itself in a loop
        run_git_command(f'git add {filename}')
        run_git_command(f'git commit -m "update: activity sync {i}/{iterations} [skip ci]"')
        
        print(f"Step {i} committed.")
        time.sleep(1) # Small delay between commits

    # 5. Final Push
    print("Syncing with GitHub...")
    run_git_command('git push origin main')

if __name__ == "__main__":
    # Your repository details for local tracking
    # Name: avirajsalunkhe
    # Email: avirajsalunkhe1@gmail.com
    multi_commit_randomizer('data.txt')
