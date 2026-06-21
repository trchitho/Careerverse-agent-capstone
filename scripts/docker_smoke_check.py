"""Docker smoke check script using Python stdlib."""

from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

IMAGE_NAME = "careerverse-agent-api:smoke"
CONTAINER_NAME = "careerverse-agent-api-smoke"
PORT = 18000
URL = f"http://127.0.0.1:{PORT}"

DEMO_PROFILE = {
    "name": "Docker Demo User",
    "education": "Final-year IT student",
    "interests": ["AI", "web development"],
    "skills": ["Python", "React", "SQL"],
    "career_goal": "Become an AI full-stack developer",
    "preferred_learning_style": "project_based",
    "language": "en",
    "experience_level": "university",
    "time_budget_hours_per_week": 8
}


def check_docker() -> bool:
    """Verify Docker binary exists and Docker daemon is running."""
    try:
        res = subprocess.run(["docker", "--version"], capture_output=True, text=True, check=True)
        print(f"Docker version: {res.stdout.strip()}")
        subprocess.run(["docker", "info"], capture_output=True, check=True)
        return True
    except Exception as e:
        print(f"Docker check failed (is Docker daemon running?): {e}", file=sys.stderr)
        return False


def run_cmd(cmd: list[str]) -> bool:
    """Run a system command and return True on success."""
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}", file=sys.stderr)
        return False


def test_get_endpoints() -> bool:
    """Verify standard GET endpoints return HTTP 200."""
    endpoints = [
        ("GET /", ""),
        ("GET /metadata", "/metadata"),
        ("GET /tools", "/tools"),
    ]
    for label, path in endpoints:
        try:
            req = urllib.request.Request(f"{URL}{path}")
            with urllib.request.urlopen(req) as resp:
                if resp.status != 200:
                    print(f"FAIL: {label} returned status {resp.status}")
                    return False
                print(f"PASS: {label}")
        except Exception as e:
            print(f"FAIL: {label} raised exception: {e}")
            return False
    return True


def test_post_recommend() -> bool:
    """Verify POST /recommend returns HTTP 200 with top_recommendations."""
    try:
        data = json.dumps(DEMO_PROFILE).encode("utf-8")
        req = urllib.request.Request(
            f"{URL}/recommend",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            if resp.status != 200:
                print(f"FAIL: POST /recommend returned status {resp.status}")
                return False
            res_data = json.loads(resp.read().decode("utf-8"))
            if "top_recommendations" not in res_data:
                print("FAIL: POST /recommend response missing recommendations key")
                return False
            print("PASS: POST /recommend")
    except Exception as e:
        print(f"FAIL: POST /recommend raised exception: {e}")
        return False
    return True


def main() -> int:
    """Run full Docker build and endpoint validation cycle."""
    if not check_docker():
        print("FAIL: Docker environments are not set up or running.", file=sys.stderr)
        return 1

    subprocess.run(["docker", "stop", CONTAINER_NAME], capture_output=True)

    print("Building Docker image...")
    if not run_cmd(["docker", "build", "-t", IMAGE_NAME, "."]):
        print("FAIL: Docker image build failed.")
        return 1

    print("Starting container...")
    start_cmd = [
        "docker", "run", "--rm", "-d",
        "-p", f"{PORT}:8000",
        "--name", CONTAINER_NAME,
        IMAGE_NAME
    ]
    if not run_cmd(start_cmd):
        print("FAIL: Docker container run failed.")
        return 1

    print("Waiting for API to start...")
    ready = False
    for _ in range(30):
        try:
            req = urllib.request.Request(URL)
            with urllib.request.urlopen(req) as resp:
                if resp.status == 200:
                    ready = True
                    break
        except Exception:
            time.sleep(1)
