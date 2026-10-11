"""Expose build failures in GitHub's public check annotations."""
import subprocess
import sys


def main():
    result = subprocess.run([sys.executable, "scripts/build.py"], text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout)
    if result.returncode:
        escaped = result.stdout[-50000:].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print("::error title=Windows packaging failure::" + escaped)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
