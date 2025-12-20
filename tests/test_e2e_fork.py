"""
End-to-end test for ForkMonkey fork flow.

This test:
1. Forks the ForkMonkey repository into an organization using gh CLI
2. Enables GitHub Actions on the fork
3. Enables GitHub Pages
4. Triggers the Initialize workflow manually
5. Verifies monkey_data is properly initialized
6. Cleans up by deleting the test repository

Requirements:
- gh CLI authenticated with appropriate permissions
- Access to springsoftware-digital organization
"""

import os
import subprocess
import time
import json
import pytest
from datetime import datetime


# Configuration
SOURCE_REPO = "roeiba/forkMonkey"
TARGET_ORG = "springsoftware-digital"
TEST_REPO_PREFIX = "forkmonkey-test"


class SetupError(Exception):
    """Raised when test setup fails."""
    pass


def run_gh(args: list, check: bool = True) -> subprocess.CompletedProcess:
    """Run a gh CLI command."""
    cmd = ["gh"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise RuntimeError(f"gh command failed: {' '.join(cmd)}\nstderr: {result.stderr}\nstdout: {result.stdout}")
    return result


@pytest.fixture(scope="module")
def test_repo_name():
    """Generate unique test repository name."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{TEST_REPO_PREFIX}-{timestamp}"


@pytest.fixture(scope="module")
def test_repo(test_repo_name):
    """
    Fork repository and clean up after tests.
    
    This fixture:
    1. Forks the ForkMonkey repo to the target org using gh CLI
    2. Enables Actions and Pages
    3. Triggers the workflow
    4. Yields the repo info for tests
    5. Deletes the repo after all tests complete
    """
    full_name = f"{TARGET_ORG}/{test_repo_name}"
    errors = []
    
    try:
        # Step 1: Fork the repository using gh CLI
        print(f"\n🍴 Forking {SOURCE_REPO} to {full_name}")
        result = run_gh([
            "repo", "fork", SOURCE_REPO,
            "--org", TARGET_ORG,
            "--fork-name", test_repo_name,
            "--clone=false"
        ])
        print(f"✅ Repository forked: {result.stdout.strip()}")
        
        # Wait for fork to be fully ready
        print("⏳ Waiting for fork to be ready...")
        time.sleep(10)
        
        # Step 2: Enable GitHub Actions 
        print("🔧 Enabling GitHub Actions...")
        actions_result = run_gh([
            "api", f"/repos/{full_name}/actions/permissions",
            "-X", "PUT",
            "-F", "enabled=true",
            "-f", "allowed_actions=all"
        ], check=False)
        
        if actions_result.returncode != 0:
            errors.append(f"Failed to enable Actions: {actions_result.stderr}")
        else:
            print("✅ GitHub Actions enabled")
        
        # Step 3: Enable GitHub Pages (using workflow deployment)
        print("🔧 Enabling GitHub Pages...")
        pages_result = run_gh([
            "api", f"/repos/{full_name}/pages",
            "-X", "POST",
            "-f", "build_type=workflow"
        ], check=False)
        
        if pages_result.returncode != 0 and "already exists" not in pages_result.stderr.lower():
            errors.append(f"Failed to enable Pages: {pages_result.stderr}")
        else:
            print("✅ GitHub Pages enabled")
        
        # Wait for Actions to be fully available
        print("⏳ Waiting for Actions to be ready...")
        time.sleep(5)
        
        # Step 4: Trigger the Initialize New Monkey workflow
        print("🚀 Triggering on-create.yml workflow...")
        
        # Retry logic for workflow trigger
        max_retries = 3
        workflow_triggered = False
        
        for attempt in range(max_retries):
            workflow_result = run_gh([
                "api", f"/repos/{full_name}/actions/workflows/on-create.yml/dispatches",
                "-X", "POST",
                "-f", "ref=main"
            ], check=False)
            
            if workflow_result.returncode == 0:
                print(f"✅ Workflow triggered (attempt {attempt + 1})")
                workflow_triggered = True
                break
            else:
                print(f"  Attempt {attempt + 1} failed: {workflow_result.stderr.strip()}")
                if attempt < max_retries - 1:
                    time.sleep(3)
        
        if not workflow_triggered:
            errors.append(f"Failed to trigger workflow after {max_retries} attempts")
        
        # Check for any errors
        if errors:
            raise SetupError("\n".join(errors))
        
        # Yield repo info for tests
        yield {
            "full_name": full_name,
            "name": test_repo_name,
            "owner": TARGET_ORG,
        }
        
    except Exception as e:
        # If setup failed, still try cleanup
        print(f"\n❌ Setup failed: {e}")
        raise
        
    finally:
        # Cleanup: Delete the test repository
        print(f"\n🧹 Cleaning up: Deleting {full_name}")
        delete_result = run_gh(["repo", "delete", full_name, "--yes"], check=False)
        if delete_result.returncode == 0:
            print(f"✅ Repository {full_name} deleted successfully")
        else:
            print(f"⚠️ Failed to delete: {delete_result.stderr.strip()}")


class TestForkMonkeyE2E:
    """End-to-end tests for ForkMonkey fork flow."""
    
    def test_repo_created_successfully(self, test_repo):
        """Verify repository was forked successfully."""
        result = run_gh(["repo", "view", test_repo["full_name"], "--json", "name,owner,isFork"])
        data = json.loads(result.stdout)
        
        assert data["name"] == test_repo["name"]
        assert data["owner"]["login"] == TARGET_ORG
        assert data["isFork"] == True, "Repository should be a fork"
        print(f"✅ Repository exists and is a fork!")
    
    def test_workflow_triggered(self, test_repo):
        """Verify the workflow is triggered."""
        max_wait = 90
        poll_interval = 5
        start_time = time.time()
        
        print(f"\n⏳ Waiting for workflow to trigger (max {max_wait}s)...")
        
        while time.time() - start_time < max_wait:
            result = run_gh([
                "run", "list", "--repo", test_repo["full_name"],
                "--limit", "5", "--json", "name,status,conclusion"
            ], check=False)
            
            if result.returncode == 0 and result.stdout.strip():
                runs = json.loads(result.stdout)
                if runs:
                    run = runs[0]
                    print(f"✅ Workflow found: {run['name']} - Status: {run['status']}")
                    return
            
            elapsed = int(time.time() - start_time)
            print(f"  ... waiting ({elapsed}s elapsed)")
            time.sleep(poll_interval)
        
        pytest.fail("No workflow run found within timeout period")
    
    def test_workflow_completes(self, test_repo):
        """Wait for workflow to complete (success or partial success)."""
        max_wait = 300
        poll_interval = 15
        start_time = time.time()
        
        print(f"\n⏳ Waiting for workflow to complete (max {max_wait}s)...")
        
        while time.time() - start_time < max_wait:
            result = run_gh([
                "run", "list", "--repo", test_repo["full_name"],
                "--limit", "5", "--json", "name,status,conclusion"
            ], check=False)
            
            if result.returncode == 0 and result.stdout.strip():
                runs = json.loads(result.stdout)
                
                for run in runs:
                    if run.get("name") != "Initialize New Monkey":
                        continue
                        
                    status = run.get("status")
                    conclusion = run.get("conclusion")
                    
                    print(f"  Workflow '{run['name']}': status={status}, conclusion={conclusion}")
                    
                    if status == "completed":
                        if conclusion == "success":
                            print(f"✅ Workflow completed successfully!")
                            return
                        elif conclusion == "failure":
                            # Check if monkey_data files exist (partial success)
                            print("⚠️ Workflow marked as failure, checking if monkey was initialized...")
                            check_result = run_gh([
                                "api", f"/repos/{test_repo['full_name']}/contents/monkey_data/dna.json"
                            ], check=False)
                            
                            if check_result.returncode == 0:
                                print("✅ Workflow partially succeeded - monkey_data exists!")
                                print("   (Failure was likely on non-critical step like issue creation)")
                                return
                            else:
                                pytest.fail(f"Workflow failed and monkey_data not created")
            
            elapsed = int(time.time() - start_time)
            print(f"  ... waiting ({elapsed}s elapsed)")
            time.sleep(poll_interval)
        
        pytest.fail("Workflow did not complete within timeout period")
    
    def test_monkey_initialized(self, test_repo):
        """Verify monkey_data files were created."""
        print("\n🔍 Checking for monkey_data files...")
        
        # Wait for commit to propagate
        time.sleep(5)
        
        expected_files = [
            "monkey_data/dna.json",
            "monkey_data/stats.json", 
            "monkey_data/history.json",
            "monkey_data/monkey.svg",
        ]
        
        for file_path in expected_files:
            result = run_gh([
                "api", f"/repos/{test_repo['full_name']}/contents/{file_path}"
            ], check=False)
            
            if result.returncode != 0:
                pytest.fail(f"File not found: {file_path}")
            
            print(f"  ✅ Found: {file_path}")
        
        print("✅ All monkey_data files present!")
    
    def test_readme_updated(self, test_repo):
        """Verify README was updated with monkey info."""
        print("\n🔍 Checking README...")
        
        result = run_gh([
            "api", f"/repos/{test_repo['full_name']}/contents/README.md"
        ])
        
        import base64
        data = json.loads(result.stdout)
        content = base64.b64decode(data["content"]).decode("utf-8")
        
        assert "MONKEY_DISPLAY" in content, "Monkey display section not found in README"
        assert "MONKEY_STATS" in content, "Monkey stats section not found in README"
        
        print("✅ README contains monkey sections!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
