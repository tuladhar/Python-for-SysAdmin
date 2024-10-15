import subprocess

# Execute a shell command
result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE)
print(result.stdout.decode())

# Capture output from a command
output = subprocess.check_output(['uname', '-r'])
print("Kernel version:", output.decode().strip())
