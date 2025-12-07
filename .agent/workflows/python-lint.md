---
description: python-lint
---

{
  "description": "Automatically format Python files after any Edit operation using black formatter. This hook runs 'black' on any .py file that Claude modifies, ensuring consistent Python code formatting. Requires black to be installed ('pip install black').",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then if command -v black >/dev/null 2>&1; then black \"$CLAUDE_TOOL_FILE_PATH\"; else echo \"Warning: black formatter not installed.\" >&2; fi; fi"
          }
        ]
      }
    ]
  }
}
