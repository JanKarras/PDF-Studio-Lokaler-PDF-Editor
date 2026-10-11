"""Make failures inspectable through public check annotations as well as JUnit."""
import subprocess
import sys


def main():
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", "--junitxml=test-results.xml"],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout)
    if result.returncode:
        escaped = result.stdout[-50000:].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print("::error title=PDF and GUI test failure::" + escaped)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
