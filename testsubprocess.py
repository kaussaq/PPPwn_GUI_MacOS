import subprocess
chosen_int = ("en0")
subprocess.run(["python3", "pppwn.py", "--interface="+ chosen_int , "--fw=1100"])