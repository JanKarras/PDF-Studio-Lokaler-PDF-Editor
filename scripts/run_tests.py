"""Make failures inspectable through public check annotations as well as JUnit."""
import subprocess
import sys


def main():
    try:
        result = subprocess.run([sys.executable, "-u", "-m", "pytest", "-vv", "--junitxml=test-results.xml"],
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    except subprocess.TimeoutExpired as error:
        output = error.stdout or b""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="replace")
        result = subprocess.CompletedProcess(error.cmd, 1, output + "\nTest timeout after 180 seconds")
    print(result.stdout)
    if result.returncode:
        details = result.stdout.split("FAILURES", 1)[-1][-18000:]
        for index in range(0, len(details), 3000):
            escaped = details[index:index + 3000].replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
            print("::error title=PDF and GUI test failure " + str(index // 3000 + 1) + "::" + escaped)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
