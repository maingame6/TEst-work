#!/bin/sh
# systemd LoadCredential path only. Never log token.
set -eu
case "$1" in
  *Username*) printf '%s\n' 'x-access-token' ;;
  *Password*)
    test -n "$CREDENTIALS_DIRECTORY" || exit 1
    exec cat "$CREDENTIALS_DIRECTORY/github_token"
    ;;
  *) exit 1 ;;
esac
