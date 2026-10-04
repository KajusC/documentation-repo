Create a topic and path for a new documentation page based on the code change and existing documentation file tree.

## User's input

- User part contains a documentation tree where a code change does not fit in any of the files.
- A code change with a file name is attached.

## File tree structure

A documentation file tree is a structured component where a documentation is layered in:

- a root-level name (e.g. "documents)
  - service (e.g. "authentication service")
    - topic (e.g. "Authentication actions")
      - subtopic (e.g. "Login")

Path in a template of:

```
documents/<service>/<topic>/<subtopic>/index.md
```

If Path is pointing to a subtopic:

```
documents/<service>/<topic>/index.md
```

## Steps

1. Analyze the code change. Decide where it belongs and what it does.
2. Check the documentation file tree.
3. If the code change belongs to a service, topic, or subtopic, return the corresponding topic and path.
4. path must always end with and index.md file.

## Rules

1. File can exist in a service where documentation does exist/ does not yet exist.
2. If service does not exist, create structure up to the service level coming from the subtopic.

## Output in JSON format

- `topic`: The topic of the new documentation page.
  - If no good topic is found, return None.
- `structure_level`: The structure level of the new documentation page.
  - possible values: "service", "topic", "subtopic"
- `path`: The path to the new documentation page.
  - If no good path is found, return None.

## Json Structure example

```json
{
  "topic": "Authentication actions",
  "documentation": [
    {
      "structure_level": "service",
      "path": "documents/authentication/index.md"
    },
    {
      "structure_level": "topic",
      "path": "documents/authentication/authentication-actions/index.md"
    },
    {
      "structure_level": "subtopic",
      "path": "documents/authentication/authentication-actions/login/index.md"
    }
  ]
}
```
