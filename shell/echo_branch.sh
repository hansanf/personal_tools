#!/bin/bash
# 列出当前各个目录的repo分支
# Loop through each directory in the current directory
for dir in (ls -1); do
  # Check if the directory is a git repository
  if [ -d "$dir/.git" ]; then
    # Change into the directory and get the version number
    cd "$dir"
    #version=$(git describe --tags)
    version=$(git status |sed -n '1p')
    # Print the directory name and version number
    echo "$dir: 
         $version"
    # Change back to the original directory
    cd ..
  fi
done
