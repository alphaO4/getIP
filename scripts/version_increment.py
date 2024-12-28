import subprocess


def get_next_version():
    # Fetch the latest tag
    result = subprocess.run(
        ["git", "describe", "--tags"], capture_output=True, text=True
    )
    latest_tag = result.stdout.strip()

    # Increment the patch version
    major, minor, patch = map(int, latest_tag.lstrip("v").split("."))
    patch += 1
    return f"v{major}.{minor}.{patch}"


def create_new_tag(version):
    subprocess.run(["git", "tag", version])
    subprocess.run(["git", "push", "origin", version])


if __name__ == "__main__":
    new_version = get_next_version()
    create_new_tag(new_version)
