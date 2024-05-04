## VS Code

### Type checking

- `# type: ignore` - ignore a line

```json
// settings.json
  "python.analysis.diagnosticSeverityOverrides": {
    "reportUnusedVariable": "warning"
  }
```

```json
// pyrightconfig.json
{
  "typeCheckingMode": "strict",
  "reportUnusedVariable": "warning"
}
```

## Error Handling

### Ignore all errors on `sigint` when writing to `stdout`

This was difficult to find and it differs from how the official docs reccomend.
But this was the only variation that seems to work 100% of the time.

```python
try:
    while True:
        sys.stdout.buffer.write(bytes([0]))
except (BrokenPipeError, KeyboardInterrupt):
    sys.stdout = None
```
