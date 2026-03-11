# 知识同步冲突解决指南

当两个助手同时修改同一文件时，Git 会产生冲突。本文档说明如何快速解决。

---

## 🚨 冲突识别

同步脚本会输出：
```
WARNING: Pull failed (conflict or offline)
```

或在日志中看到：
```
Auto-merging MEMORY.md
CONFLICT (content): Merge conflict in MEMORY.md
```

---

## 🔧 解决步骤

### **1. 检查冲突文件**

```bash
cd ~/.openclaw/workspace/sync
git status
```

输出示例：
```
Unmerged paths:
  (use "git add <file>..." to mark resolution)
  both modified:   memory/MEMORY.md
  both modified:   notes/areas/proactive-tracker.md
```

### **2. 查看冲突内容**

```bash
# 查看冲突标记（<<<<<<<）
cat memory/MEMORY.md | grep -A 5 -B 5 '<<<<<<<'
```

冲突标记格式：
```
<<<<<<< HEAD
本地版本的内容
=======
远程版本的内容
>>>>>>> feature/sync
```

### **3. 决策策略**

根据文件类型选择合并方式：

| 文件类型 | 策略 | 操作 |
|---------|------|------|
| **MEMORY.md** | 追加式合并 | 保留双方新增段落，删除冲突标记 |
| **每日笔记** | 保留双方 | 两文件都保留（不同日期自动区分） |
| **proactive-tracker.md** | 表格合并 | 手动合并表格行，保留最新状态 |
| **core 文件** | 取最新版本 | 以时间戳最新者为准，或人工协商 |

### **4. 手动合并示例**

**场景**：双方都更新了 `MEMORY.md` 的不同段落

```bash
# 编辑文件，移除冲突标记，保留双方内容
nano memory/MEMORY.md
```

合并后：
```
## 2026-03-11
### Agent A 添加
- 完成了 Star Office 修复

### Agent B 添加
- 配置了知识同步系统
```

**保存并标记为已解决**：
```bash
git add memory/MEMORY.md
```

### **5. 完成同步**

```bash
# 继续解决其他冲突文件...
git add <已解决的文件>

# 提交合并结果
git commit -m "Merge sync conflict on $(date '+%Y-%m-%d %H:%M')"

# 推送
git push origin main
```

---

## ⚠️ **紧急处理：放弃本地/远程变更**

如果冲突太复杂，可以：

**放弃本地，采用远程：**
```bash
git reset --hard origin/main
# 然后从本地备份恢复未同步的独立文件
```

**放弃远程，采用本地：**
```bash
git push -f origin main  # 强制覆盖（需协调，避免覆盖对方）
```

---

## 🛡️ **预防措施**

1. **频繁同步**：当前每 10 分钟一次，可缩短间隔
2. **分区修改**：不同 Agent 主攻不同文件（如 A 改 MEMORY，B 改 notes）
3. **原子提交**：每次同步只提交一个逻辑变更，便于追溯
4. **时间戳检查**：合并时查看 `last-sync-state.json` 了解更新顺序

---

## 📊 **冲突频率监控**

在 `sync-status.sh` 中查看：
```
git -C sync log --oneline --since="1 day ago" | grep -i conflict
```

如果冲突频繁（>3次/天），考虑：
- 调整同步频率
- 拆分大文件为更细粒度
- 改用 Feishu 实时协作（减少 Git 冲突）

---

**记住：Git 冲突是正常的，关键是快速识别和协商解决。** 🤝
