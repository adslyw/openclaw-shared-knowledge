# Proactive Tracker

Track proactive behaviors and opportunities to surprise the human.

## Overdue Proactive Behaviors

*Check weekly: Any patterns that should be automated?*

- [ ] 检查是否有重复请求需要建立自动化
- [ ] 检查是否有重要的未完成事项需要跟进
- [ ] 检查是否有新工具/技能可以提升效率

## Opportunities Log

*What could I build RIGHT NOW that would make my human say "I didn't ask for that but it's amazing"?*

**2026-03-20**: Service Health Monitor
- Problem: M3U Player running 46+ hours without restart strategy; need visibility into service health
- Solution: Lightweight daemon that checks all critical services every 5 minutes, logs status, auto-restarts failures
- Benefits: Proactive self-healing, permanent uptime, single source of truth for system health
- Implementation: Simple shell script with curl checks + restart logic, structured JSON logging

**2026-03-20 (2)**: Backup Integrity Validator
- Problem: M3U Player has 7-day rotating backups, but no verification that backups are actually valid and restorable
- Solution: Automated weekly restore test that picks random backup, restores to temp DB, verifies schema/row counts/data accessibility, generates validation report
- Benefits: Confidence that backups will work when needed, catches corruption early
- Different focus: DATA RECOVERABILITY rather than service health

**2026-03-20 (3)**: Documentation Consistency Auditor
- Problem: Growing workspace (notes/, MEMORY.md, skills, AGENTS.md) accumulates broken links, orphaned files, formatting drift unnoticed
- Solution: Scan all markdown files for broken internal links, missing references, heading inconsistencies, orphaned files; generate `memory/docs-audit-YYYY-MM-DD.md` with categorized issues and suggested fixes
- Benefits: Maintains knowledge base health, prevents reference rot, ensures long-term maintainability
- Different focus: KNOWLEDGE QUALITY (docs/linking) vs. operational/system metrics

**2026-03-20 (4)**: Unified Log Dashboard
- Problem: Logs scattered across services (sync logs, star-office-daemon.log, Docker logs, backup logs) - no single view of system-wide health
- Solution: Daily consolidated log digest aggregating all service logs into `memory/daily-log-digest-YYYY-MM-DD.md` with categorized sections, error highlights, trend indicators; plus optional real-time HTML dashboard for streaming view
- Benefits: One-place observability, rapid troubleshooting, pattern recognition across services
- Different focus: CENTRALIZED OBSERVABILITY vs. individual service monitors

**2026-03-20 (5)**: Network Performance Baseline Tracker
- Problem: System performance is good but we have no baseline metrics for network latency (to localhost services), disk I/O speed (for database writes), and container startup times under load
- Solution: Benchmark script that runs every 6 hours, measures key metrics (curl response time, db write latency, docker start time), stores time-series data in `memory/performance-baseline-YYYY-MM.jsonl`
- Benefits: Early detection of performance degradation, capacity planning data, quantitative evidence for optimization efforts
- Different focus: PERFORMANCE QUANTIFICATION vs. health monitoring; establishes data-driven baselines

**2026-03-20 (6)**: Security Posture Scanner
- Problem: System runs reliably but lacks visibility into security exposure (open ports, file permissions, outdated packages, credential leakage)
- Solution: Weekly automated security audit that scans for world-writable files, Docker security issues (privileged mode), hardcoded secrets, exposed ports; generates `memory/security-audit-YYYY-MM-DD.md` with risk ratings and remediation steps
- Benefits: Proactive security hygiene, early misconfiguration detection, maintains trust
- Different focus: RISK PREVENTION (security) vs. reliability, quality, or performance monitoring

**2026-03-20 (7)**: Dependency License Compliance Scanner
- Problem: M3U Player uses npm packages; no visibility into license compliance (MIT, GPL, etc.) affecting distribution rights
- Solution: Monthly scan using `license-checker` to catalog dependencies, their licenses, flag conflicts, generate `memory/license-compliance-YYYY-MM.md`
- Benefits: Legal compliance awareness, avoids licensing issues, identifies problematic dependencies early
- Different focus: LEGAL/COMPLIANCE dimension, not technical or operational metrics

**2026-03-20 (8)**: Configuration Drift Detector
- Problem: Knowledge sync auto-manages core/memory/notes/skills; manual edits to these files could cause sync conflicts or unexpected overwrites
- Solution: Pre-sync and post-sync comparison to detect manual modifications, generate `memory/drift-report-YYYY-MM-DD.md` with file paths, diffs, conflict likelihood
- Benefits: Prevents accidental overwrites, increases sync transparency, gives owner confidence that automation respects manual work
- Different focus: CHANGE ORIGINS tracking (manual vs automated) vs. health, quality, or compliance

**2026-03-20 (9)**: Resource Usage Alert System
- Problem: System runs fine but lacks proactive alerts for resource exhaustion (disk >85%, memory pressure, container log volume) before it becomes critical
- Solution: Threshold-based monitor checking disk usage (/, /data, Docker volumes), memory utilization, container log sizes hourly; escalate via `memory/` logs and optional Star Office notification when thresholds exceeded
- Benefits: Prevents unexpected outages due to resource saturation, gives lead time for cleanup/expansion, maintains service continuity
- Different focus: RESOURCE CAPACITY MANAGEMENT vs. service liveness, performance baselines, or security

**2026-03-20 (10)**: Service Dependency Graph Generator
- Problem: Multiple services (knowledge sync, Star Office daemon, M3U Player) interact but we lack visibility into their dependencies and impact chains
- Solution: Static analysis tool that parses cron jobs, Docker compose files, shell scripts, config files to build a dependency graph in DOT/Graphviz format, outputs to `memory/service-dependencies-YYYY-MM-DD.dot`
- Benefits: Visualize system topology, identify single points of failure, understand cascading impacts before making changes
- Different focus: ARCHITECTURE VISUALIZATION vs. health/performance/compliance monitoring

---

## Ideas (Drip Feed)

Ideas for proactive improvements, filed for later:

- [ ] **Agent Health Monitor** - Based on Day 4 PM dereliction, build a system that:
  - Monitors agent heartbeat/last update timestamp
  - Auto-escalates if agent unresponsive >15 minutes
  - Attempts graceful restart of failed sessions
  - Sends alerts to owner with recovery suggestions
  - This would prevent future communication blackouts

- [ ] **Test Isolation Framework** - E2E test failures highlighted need for:
  - Auto-generated unique test IDs (no collisions)
  - Built-in database cleanup hooks
  - Standardized selector patterns with scoping
  - Could be packaged as a reusable skill for future projects

- [ ] **Pre-Deploy Validator** - Production config mismatch caused Day 3 crash:
  - Validate environment variables match code expectations
  - Check filesystem permissions for mounted volumes
  - Verify port availability before launch
  - Could integrate as CI/CD gate or pre-run script
