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
