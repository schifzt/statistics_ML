import subprocess

mzn = "min_ell_zero_norm.mzn"
dzn = "input.dzn"
solver = "CBC"
cmd = f"minizinc {mzn} -d {dzn} --solver {solver} -a"
subprocess.run(cmd)