#!/usr/bin/env python
"""AWS Org Library command-line utility for administrative tasks."""
import os
import sys
from package_narendra_func_add import package


def main():
    """Run administrative tasks."""
    output=package.add_one(2)
    print(output)
    # print(f"sys.argv = {sys.argv}")


if __name__ == "__main__":
    main()
