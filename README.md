# 知识同步目录结构

```
sync/
├── core/               # 核心配置（SOUL, USER, AGENTS, HEARTBEAT）
│   ├── SOUL.md
│   ├── USER.md
│   ├── AGENTS.md
│   ├── HEARTBEAT.md
│   └── ONBOARDING.md
├── memory/             # 长期记忆（MEMORY + 每日笔记，自动脱敏）
│   ├── MEMORY.md
│   ├── 2026-03-10.md
│   └── 2026-03-11.md
├── notes/areas/        # 学习笔记与模式跟踪
│   ├── proactive-tracker.md
│   ├── recurring-patterns.md
│   └── outcome-journal.md
├── skills/             # 技能文档与脚本（版本化）
│   ├── proactive-agent/
│   │   ├── SKILL.md
│   │   ├── README.md
│   │   └── scripts/
│   └── ...
├── state/              # 公开运行状态
│   └── star-office-state.json
├── last-sync-state.json # 同步状态记录（自动生成）
└── README.md           # 本文件
```

---

## 🔄 同步机制

### **双向实时同步**
- 每 10 分钟自动执行 `scripts/knowledge-sync.sh`
- 先拉取（pull）远程变更，再推送（push）本地更新
- 冲突时自动 stash，需人工介入

### **敏感过滤**
- **自动排除**：`.env*`, `*.key`, `*.pem`, `credentials/`, `working-buffer.md`
- **内容脱敏**：`MEMORY.md` 和每日笔记中的密码、API keys、tokens 自动替换为 `[REDACTED]`
- **状态文件**：`state.json` 仅同步公开字段，密钥字段删除

---

## 🚀 快速开始

### **1. 配置 Git Remote**

在每个工作区执行（替换为你的云端仓库 URL）：

```bash
cd ~/.openclaw/workspace
git remote add origin <your-cloud-repo-url>
git push -u origin main
```

### **2. 初始化共享目录**

首次运行会自动创建目录结构。手动触发一次：

```bash
./scripts/knowledge-sync.sh
```

### **3. 设置定时任务（推荐）**

**OpenClaw Cron**（隔离运行）：

```json
{
  "name": "knowledge-sync",
  "schedule": { "kind": "every", "everyMs": 600000 },
  "payload": {
    "kind": "agentTurn",
    "message": "AUTONOMOUS: Run ~/.openclaw/workspace/scripts/knowledge-sync.sh"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

**或系统 cron**：

```bash
crontab -e
*/10 * * * * /home/lyw/.openclaw/workspace/scripts/knowledge-sync.sh >> /dev/null 2>&1
```

---

## ⚠️ **注意事项**

- **不要**将 `sync/` 目录软链接到多个位置（会破坏 Git 历史）
- **不要**手动修改 `sync/` 中的文件（除了冲突解决）
- **冲突处理**：当 `git pull` 冲突时，检查 `*.orig` 文件，手动合并后 `git add` 并 `git push`
- **日志**：查看 `logs/sync-YYYY-MM-DD.log` 了解同步历史

---

## 🛡️ **安全策略**

- `sync/` 仅包含**可共享**内容，不含任何密钥
- 私有数据保留在 `local/` 或未跟踪文件
- 脱敏脚本可能误伤，如有重要信息丢失请检查日志并调整 `sed` 规则

---

## 📊 **监控**

- 健康检查：`curl http://127.0.0.1:19000/health`（如果 Star Office 运行）
- 同步日志：`tail -f logs/sync-*.log`
- Git 状态：`git -C sync status`

---

**版本**: 1.0 | **最后更新**: 2026-03-11
