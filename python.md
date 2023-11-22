## VS Code

### Type checking

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


