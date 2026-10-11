"""Expose build failures in GitHub's public check annotations."""
import subprocess
import sys


def main():
    result = subprocess.run([sys.executable, "scripts/build.py"], text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout)
    if result.returncode:
        details = result.stdout.split("FAILURES", 1)[-1][-18000:]
        for index in range(0, len(details), 3000):
            escaped = details[index:index + 3000].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print("::error title=Windows packaging failure " + str(index // 3000 + 1) + "::" + escaped)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
