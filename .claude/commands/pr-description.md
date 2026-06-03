Write PR Description for: $ARGUMENTS

PR conventions:

- Prompt for branch if not provided as argument
- Use @PULL_REQUEST_TEMPLATE.md if found in .github/ or root
- Create description in markdown format so the user can copy it directly

Questions:

- Prompt which commits to use if there are more than 10 or the scope is unclear
- Validate the output is valid GitHub-flavored markdown before showing it