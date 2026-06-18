# Database Audit — <Database / Source Name>

| Field        | Value                                   |
|--------------|-----------------------------------------|
| Status       | Draft \| In Review \| Final              |
| Auditor      | Sergio Tortolero (+ Claude)             |
| Engine       | SQL Server \| Azure SQL \| PostgreSQL \| ... |
| Scope        | <schemas / stored procedures / views>   |
| Date         | YYYY-MM-DD                              |
| Related PRD  | <link>                                  |

## 1. Inventory
What exists in the database.

| Object type      | Count | Notes                          |
|------------------|-------|--------------------------------|
| Tables           |       |                                |
| Views            |       |                                |
| Stored Procedures|       |                                |
| Functions        |       |                                |
| Triggers         |       |                                |

## 2. Stored Procedure Catalog
| SP Name | Purpose (inferred) | Inputs | Outputs | Reads | Writes | Risk |
|---------|--------------------|--------|---------|-------|--------|------|
|         |                    |        |         |       |        |      |

## 3. Findings
For each finding: severity (Critical/High/Medium/Low), evidence, impact, recommendation.

### 3.1 Security
- Dynamic SQL / injection surface, permissions, secrets in code, `xp_cmdshell`, etc.

### 3.2 Performance
- Missing indexes, scans, cursors, non-SARGable predicates, `SELECT *`, N+1 patterns.

### 3.3 Maintainability
- Dead code, duplicated logic, naming, magic numbers, lack of `SET NOCOUNT ON`, error handling.

### 3.4 Data Integrity
- Missing constraints/FKs, transaction scope, nullability, orphan handling.

## 4. "White-Level" Deliverable
> Define exactly what this means for this project (see ADR). Examples:
> sanitized/anonymized copy, schema-only export, documentation-grade rewrite,
> or a vendor-neutral (white-label) version with proprietary logic abstracted out.

- Approach:
- What is removed / masked / abstracted:
- What is preserved:

## 5. Prioritized Action Plan
| # | Action | Owner | Severity | Effort | Status |
|---|--------|-------|----------|--------|--------|
| 1 |        |       |          |        |        |

## Appendix
Raw queries used, connection method, and any scripts.
