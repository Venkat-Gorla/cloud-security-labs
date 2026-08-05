# AWS Config Platform Governance

## Problem

Cloud environments change continuously. Without recording infrastructure changes, it is difficult to understand what resources exist, when they changed, and how their configuration evolved over time.

## Goal

Build Python tools to inspect AWS Config by exploring recorder status, operational metrics, discovered resources, and configuration history.

## Architecture

```text
AWS Resources
     │
     │ Configuration Changes
     ▼
AWS Config Recorder
     │
     │ Configuration Items
     ▼
AWS Config
     │
     ├── Resource Inventory
     ├── Configuration History
     └── CloudWatch Metrics
```

## Success Criteria

| Check                                                          | Status |
| -------------------------------------------------------------- | :----: |
| AWS Config successfully records supported resource changes     |   ✅   |
| Resource inventory can be queried through AWS Config           |   ✅   |
| Configuration Items capture the state of AWS resources         |   ✅   |
| Infrastructure changes create new Configuration Items          |   ✅   |
| Configuration history is accessible through the AWS Config API |   ✅   |

## Key Finding

The `ConfigurationItemsRecorded` CloudWatch metric matched the number of Configuration Items billed by AWS, confirming a direct relationship between service metrics and cost.
