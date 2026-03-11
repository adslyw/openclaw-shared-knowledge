# 本地私有配置（不进入同步）

此目录存放**敏感数据**和**本地状态**，不会被 `knowledge-sync.sh` 共享。

## 📁 结构

```
local/
├── .credentials/      # API keys, passwords (gitignored)
├── .env*              # 环境变量文件
├── state.json         # Star Office 完整状态（含密钥）
├── agents-state.json  # Agent 状态
├── runtime-config.json # 运行时配置
├── join-keys.json     # 加入密钥
└── memory/            # 临时文件
    └── working-buffer.md  # 危险区日志（不共享）
```

---

## ⚠️  安全提醒

- **永远不要**将 `local/` 内容手动复制到 `sync/`
- 确保 `sync/.gitignore` 已正确过滤这些文件
- 备份 `local/` 定期（但不共享）

---

## 🔐 与同步的边界

`knowledge-sync.sh` 会自动：
- ❌ 排除 `local/` 所有内容
- ❌ 脱敏 `memory/*.md` 中的敏感字段
- ❌ 删除 `state.json` 的密钥字段
- ✅ 仅同步 `sync/` 中已过滤的内容

---

**保持本地私有，共享知识价值** 🔒
