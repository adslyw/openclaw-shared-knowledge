# 知识同步快速启动指南

## 🎯 目标

在 5 分钟内完成多 Agent 知识同步系统的部署。

---

## 📦 前提条件

- ✅ 两个 Agent 均为 OpenClaw + Proactive Agent
- ✅ 已有云端 Git 仓库（GitHub/Gitee 等）
- ✅ 有写权限（可创建仓库）
- ✅ Feishu 账号可选（ richer 协作）

---

## 🚀 5 分钟部署

### **Step 1: 创建云端仓库**

在 GitHub/Gitee 创建公开或私有仓库：
- 名称：`openclaw-shared-knowledge`
- 初始化：可选 README（或无）

获取 URL：
- SSH: `git@github.com:yourname/openclaw-shared-knowledge.git`
- HTTPS: `https://github.com/yourname/openclaw-shared-knowledge.git`

### **Step 2: 配置 Agent A（发起方）**

```bash
cd ~/.openclaw/workspace

# 运行设置脚本（提供你的仓库 URL）
./scripts/setup-sync-repo.sh git@github.com:yourname/openclaw-shared-knowledge.git

# 测试同步
./scripts/knowledge-sync.sh

# 查看状态
./scripts/sync-status.sh
```

### **Step 3: 配置 Agent B（加入方）**

```bash
cd ~/.openclaw/workspace

# 克隆共享仓库到 sync 目录
git clone <cloud-repo-url> sync

# 测试同步
./scripts/knowledge-sync.sh

# 验证
./scripts/sync-status.sh
```

### **Step 4: 设置定时任务**

**Agent A 和 B 分别执行：**

```bash
# OpenClaw Cron 方式（推荐）
openclaw cron add sync/cron-job-v2.json

# 或系统 crontab
crontab -e
# 添加：*/10 * * * * /home/lyw/.openclaw/workspace/scripts/knowledge-sync.sh >> /dev/null 2>&1
```

### **Step 5: 验证双向同步**

1. **Agent A 修改文件**：
   ```bash
   echo "Test from Agent A at $(date)" >> ~/.openclaw/workspace/MEMORY.md
   ./scripts/knowledge-sync.sh
   ```

2. **Agent B 检查**（等待 cron 或手动运行后）：
   ```bash
   git -C ~/.openclaw/workspace/sync pull origin main
   grep "Test from Agent A" ~/.openclaw/workspace/sync/memory/MEMORY.md
   ```

3. **反向测试**（Agent B → Agent A）

---

## 📁 目录结构说明

```
~/.openclaw/workspace/
├── scripts/
│   ├── knowledge-sync.sh    # 同步引擎（已创建）
│   ├── setup-sync-repo.sh   # 仓库初始化（已创建）
│   └── sync-status.sh       # 状态检查（已创建）
├── sync/                    # 共享目录（需 git clone 或 init）
│   ├── core/               # 核心配置
│   ├── memory/             # 记忆（脱敏）
│   ├── notes/areas/        # 学习笔记
│   ├── skills/             # 技能文档
│   ├── state/              # 公开状态
│   ├── .gitignore          # 过滤规则
│   ├── cron-job-v2.json    # 定时任务配置
│   └── README.md           # 本文件
├── local/                  # 私有数据（不共享）
│   └── README.md           # 说明
└── logs/
    └── sync-*.log          # 同步日志
```

---

## ⚠️ 重要提醒

### **不要做**：
- ❌ 手动修改 `sync/` 中的文件（除了冲突解决）
- ❌ 将 `sync/` 软链接到其他位置
- ❌ 在 `sync/` 中放置敏感信息
- ❌ 关闭自动过滤（sanitization）

### **要做**：
- ✅ 定期运行 `sync-status.sh` 检查健康
- ✅ 及时解决冲突（`git status` 查看）
- ✅ 将独立项目放在 `notes/areas/` 而非 `MEMORY.md`
- ✅ 更新 `SESSION-STATE.md` 后及时完成（避免累积）

---

## 🛠️ 故障排除

| 问题 | 解决方案 |
|------|----------|
| `git pull` 冲突 | 参考 `sync/CONFLICT_RESOLUTION.md` |
| 同步无变化 | 检查本地文件是否在排除列表中 |
| Push 失败 | 确认 remote URL 和权限 |
| 脱敏过度 | 调整 `knowledge-sync.sh` 中的 `SED_FILTERS` |
| 日志为空 | 确保 `logs/` 目录存在且可写 |

---

## 📊 监控指标

- **同步延迟**：`last-sync-state.json` 中的 `last_sync` 时间
- **冲突频率**：`git log --oneline | grep -i conflict`
- **磁盘占用**：`du -sh sync/`
- **健康状态**：`curl http://127.0.0.1:19000/health`（Star Office）

---

## 🎉 完成！

现在两个 Agent 应该能够：
- ✅ 自动交换知识（每 10 分钟）
- ✅ 保持核心配置一致
- ✅ 共享记忆和学习笔记
- ✅ 同步技能文档
- ✅ 安全过滤敏感信息

**下一步**：根据需要调整同步频率或内容粒度。如有问题，检查 `logs/sync-*.log`。

---

**版本**: 1.0 | **日期**: 2026-03-11
