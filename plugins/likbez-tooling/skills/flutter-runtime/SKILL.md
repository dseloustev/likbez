---
name: flutter-runtime
description: "Runtime debugging guide for Flutter apps using Dart MCP tools. Covers connection workflows (launch_app vs VS Code DTD), hot reload/restart, widget tree inspection, runtime error diagnosis, and app log reading."
allowed-tools: Read, Glob, Grep, mcp__dart__launch_app, mcp__dart__connect_dart_tooling_daemon, mcp__dart__get_app_logs, mcp__dart__get_runtime_errors, mcp__dart__get_widget_tree, mcp__dart__get_selected_widget, mcp__dart__set_widget_selection_mode, mcp__dart__hot_reload, mcp__dart__hot_restart, mcp__dart__stop_app, mcp__dart__hover, mcp__dart__list_running_apps, mcp__dart__list_devices
---

# Flutter Runtime Debugging

## Overview

Dart MCP provides 12 runtime debugging tools for Flutter apps. There are two connection workflows depending on whether Claude launches the app directly or connects to a user-launched session.

## Connection Workflows

### Workflow A — Direct Launch

For simple projects without custom launch arguments (e.g., `--dart-define-from-file`).

1. **List available devices:**
   ```
   mcp__dart__list_devices
   ```
2. **Launch the app:**
   ```
   mcp__dart__launch_app(root: "/path/to/project", device: "device-id")
   ```
   Returns a PID used for `get_app_logs` and `stop_app`.
3. **All 12 tools available**, including `get_app_logs(pid)` and `stop_app(pid)`.

### Workflow B — VS Code DTD

Projects launched with `--dart-define-from-file` (or other custom flags) can't use direct
`launch_app` — use the VS Code DTD workflow instead.

1. **User** launches app from VS Code (Run & Debug)
2. **User** copies DTD URI: VS Code → Command Palette → "Copy DTD Uri to clipboard"
3. **Claude** connects:
   ```
   mcp__dart__connect_dart_tooling_daemon(dtdUri: "ws://127.0.0.1:XXXXX/...")
   ```
4. **All tools except `get_app_logs` and `stop_app`** — these require a PID from `launch_app`.

## Tool Reference

| Tool | Purpose | Parameters | Workflow A | Workflow B |
|------|---------|------------|:----------:|:----------:|
| `list_devices` | List available target devices | — | Yes | Yes |
| `launch_app` | Launch Flutter app on device | `root`, `device` | Yes | N/A |
| `connect_dart_tooling_daemon` | Connect to running app via DTD URI | `dtdUri` | N/A | Yes |
| `list_running_apps` | List connected Flutter apps | — | Yes | Yes |
| `hot_reload` | Apply code changes without restart | — | Yes | Yes |
| `hot_restart` | Full restart preserving connection | — | Yes | Yes |
| `get_runtime_errors` | Get current runtime errors | — | Yes | Yes |
| `get_widget_tree` | Get full widget tree snapshot | — | Yes | Yes |
| `get_selected_widget` | Get details of selected widget | — | Yes | Yes |
| `set_widget_selection_mode` | Toggle widget selection mode | `enabled` | Yes | Yes |
| `get_app_logs` | Stream app logs (stdout/stderr) | `pid` | Yes | No |
| `stop_app` | Stop running app | `pid` | Yes | No |

**Key discovery:** `hot_reload`, `hot_restart`, `get_runtime_errors`, and `get_widget_tree` require only a DTD connection — no PID needed. Only `get_app_logs` and `stop_app` require the PID returned by `launch_app`.

## Debugging Scenarios

### 1. Runtime Error Diagnosis

```
# Connect (Workflow B)
mcp__dart__connect_dart_tooling_daemon(dtdUri: "ws://...")

# Check for errors
mcp__dart__get_runtime_errors

# Inspect widget tree around error location
mcp__dart__get_widget_tree
```

Common runtime errors: `RenderFlex overflowed`, `Null check operator used on a null value`, `setState() called after dispose()`.

### 2. Widget Layout Inspection

```
# Enable widget selection mode (user taps widget in app)
mcp__dart__set_widget_selection_mode(enabled: true)

# Get details of selected widget
mcp__dart__get_selected_widget

# Or get full tree
mcp__dart__get_widget_tree
```

Useful for diagnosing layout issues, checking widget hierarchy, verifying correct widget nesting.

### 3. Iterative Development Cycle

```
# Make code changes (Edit tool)
# Apply changes without losing state
mcp__dart__hot_reload

# If hot reload insufficient (e.g., changed initState, added fields)
mcp__dart__hot_restart

# Verify no new errors introduced
mcp__dart__get_runtime_errors
```

### 4. Type Inspection with Hover

```
# Get type info and documentation at a specific code position
mcp__dart__hover(filePath: "lib/feature/some_feature/view/screen.dart", line: 42, column: 10)
```

Works independently of app connection — useful for understanding types during debugging.

## Limitations and Troubleshooting

### DTD URI Expiry
The DTD URI is valid only while the app is running. If the app restarts (e.g., VS Code restart), the user must copy a new DTD URI.

### Hot Reload vs Hot Restart
- **Hot reload**: Applies code changes, preserves app state. Fast (~1s). Does NOT work for: changes to `initState`, new fields, changed constructors, modified `main()`.
- **Hot restart**: Full restart, loses app state. Slower (~3s). Works for all code changes.

### Widget Tree Size
`get_widget_tree` returns the full tree, which can be very large for complex screens. Focus on specific subtrees when possible by using `get_selected_widget` after the user taps on the area of interest.

### No Performance Profiling
Dart MCP tools do not include performance profiling. Use Dart DevTools separately for timeline, memory, and CPU profiling.

### No Visual UI Testing
Claude cannot observe the running app visually. Rely on `get_widget_tree`, `get_runtime_errors`, and user descriptions for UI verification.
