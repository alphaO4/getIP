import subprocess
import re


def get_latest_tag():
    try:
        result = subprocess.run(
            ["git", "describe", "--tags"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        # Handle the case where no tags exist
        return None


def parse_tag(tag):
    # Use regex to extract the version part (vMAJOR.MINOR.PATCH)
    match = re.match(r"^(v\d+\.\d+\.\d+)", tag)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Invalid tag format: {tag}")


def get_next_version():
    latest_tag = get_latest_tag()
    if latest_tag is None:
        # No tags found, initialize versioning
        return "v0.0.1"
    else:
        try:
            # Extract the version part from the tag
            version = parse_tag(latest_tag)
            major, minor, patch = map(int, version.lstrip("v").split("."))
            patch += 1
            return f"v{major}.{minor}.{patch}"
        except ValueError:
            raise ValueError(f"Invalid tag format: {latest_tag}")


def create_new_tag(version):
    try:
        subprocess.run(["git", "tag", version], check=True)
        subprocess.run(["git", "push", "origin", version], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to create or push tag: {e}")


if __name__ == "__main__":
    new_version = get_next_version()
    print(f"Creating new version: {new_version}")
    create_new_tag(new_version)
