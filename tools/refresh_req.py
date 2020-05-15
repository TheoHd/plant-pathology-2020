"""
Delete and create a new requirements.txt files from the installed packages in the current environment
"""

import os

if __name__ == "__main__":
    if os.path.isfile("requirements.txt"):
        os.system("del /f requirements.txt")
        print("Deleting pre-existing requirements.txt file...")
    os.system("conda list -e > requirements.txt")
    print("Successfully refreshed requirements.txt!")