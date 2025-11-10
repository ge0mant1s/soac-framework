# Example Detection Rule: Brute Force Authentication

## CQL Query

```cql
#event.category = authentication
event.outcome = failure
groupBy([user.name, source.ip], function=count(as="failures"))
failures >= 10
sort(field=failures, order=desc, limit=100)
```

## Description
Detects potential brute force attacks by identifying accounts with 10 or more failed authentication attempts from the same source IP.

## MITRE ATT&CK
- Tactic: Credential Access
- Technique: T1110 (Brute Force)

## Severity
High

## Response Actions
1. Investigate the source IP
2. Check if account was compromised
3. Consider blocking the source IP
4. Reset user credentials if needed
5. Enable MFA for affected accounts

## Platform Translations

### Splunk
```spl
search event.category=authentication event.outcome=failure
| stats count as failures by user.name, source.ip
| where failures >= 10
| sort -failures
| head 100
```

### Azure Sentinel
```kql
SigninLogs
| where ResultType != 0
| summarize failures=count() by UserPrincipalName, IPAddress
| where failures >= 10
| sort by failures desc
| take 100
```

### Elastic
```json
{
  "query": {
    "bool": {
      "must": [
        {"term": {"event.category": "authentication"}},
        {"term": {"event.outcome": "failure"}}
      ]
    }
  },
  "aggs": {
    "by_user_ip": {
      "terms": {"field": "user.name"},
      "aggs": {
        "by_ip": {
          "terms": {"field": "source.ip"}
        }
      }
    }
  }
}
```
