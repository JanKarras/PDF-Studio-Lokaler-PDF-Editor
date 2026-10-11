"""Read-only public GitHub verification; never needs a GitHub token."""
import json
import sys
from urllib.request import Request, urlopen

BASE = "https://api.github.com/repos/JanKarras/PDF-Studio-Lokaler-PDF-Editor"


def readApi(path):
    request = Request(BASE + path, headers={"Accept": "application/vnd.github+json", "User-Agent": "PDF-Studio-verification"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main(arguments):
    if arguments and arguments[0] == "release":
        release = readApi("/releases/tags/v1.0.0")
        print(json.dumps({"url": release["html_url"], "draft": release["draft"],
                          "assets": [{key: asset[key] for key in ("name", "size", "browser_download_url")} for asset in release["assets"]]}, indent=2))
        return
    runs = readApi("/actions/runs?per_page=5")["workflow_runs"]
    for run in runs:
        print(json.dumps({key: run[key] for key in ("id", "name", "head_sha", "status", "conclusion", "html_url")}, indent=2))
        if arguments and str(run["id"]) == arguments[0]:
            for job in readApi(f'/actions/runs/{run["id"]}/jobs')["jobs"]:
                print(json.dumps({key: job[key] for key in ("id", "name", "conclusion", "steps")}, indent=2))
                checkId = job["check_run_url"].rsplit("/", 1)[-1]
                print(json.dumps(readApi(f"/check-runs/{checkId}/annotations"), indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
