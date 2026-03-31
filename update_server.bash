#!/bin/bash

# Stash all changes
git stash --all

# Sync with GitHub
gh repo sync

# Restore stashed changes
git stash pop

# Restart gunicorn service
sudo systemctl restart gunicorn-instancepublic.service