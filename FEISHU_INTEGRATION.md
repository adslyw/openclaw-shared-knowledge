# Feishu 知识库集成配置

本文档描述如何将知识同步系统与 Feishu 文档/多维表格集成，实现 richer 的协作体验。

---

## 📋 可用 Feishu 工具

OpenClaw 提供以下 Feishu 相关工具：

- `feishu_doc` - 读写文档
- `feishu_bitable_*` - 多维表格 CRUD
- `feishu_wiki` - 知识库节点管理
- `feishu_drive` - 云盘文件操作

---

## 🎯 实际配置（主人）

### 用户标识
- **显示名称**: 用戶355798
- **open_id**: `ou_2a65393851d54096fb0e92453a6e8ef9`
- **常用群聊**: "我的大本营" (`oc_682d1227151859c20e4e7e7b28737770`)

### 常用操作示例
```bash
# 向主人发送个人消息
message action=send channel=feishu target=ou_2a65393851d54096fb0e92453a6e8ef9 message="任务已完成"

# 向大本营群发消息
message action=send channel=feishu target=oc_682d1227151859c20e4e7e7b28737770 message="同步完成"
```

### 权限检查
运行 `feishu_app_scopes` 查看当前应用权限。确保包含：
- `im:message` (读写消息)
- `im:chat:read` (读取聊天列表)
- `im:chat:create` (创建聊天)
- `im:message.send_as_bot` (机器人发送)

---

## 🗂️ 建议的 Feishu 结构

### **方案 A: 使用 Wiki（推荐）**

创建知识库空间：`OpenClaw 共享知识`

```
OpenClaw 共享知识/
├── 核心配置 (只读)
│   ├── SOUL.md (Agent 人格)
│   ├── USER.md (用户画像)
│   └── AGENTS.md (运行规则)
├── 记忆银行
│   ├── MEMORY.md (长期记忆)
│   ├── 2026-03-10/
│   └── 2026-03-11/
├── 学习笔记
│   ├── 主动追踪
│   ├── 重复模式
│   └── 结果日志
└── 技能库
    ├── proactive-agent/
    └── ...
```

**同步脚本增强**（在 `knowledge-sync.sh` 中添加）：

```bash
# 同步到 Feishu Wiki
sync_to_feishu_wiki() {
  local file="$1"
  local space_id="your-space-id"  # 从 feishu_wiki spaces 获取
  local node_name=$(basename "$file" .md)

  # 如果节点存在则更新，否则创建
  existing_node=$(feishu_wiki action=search space_id="$space_id" query="$node_name" 2>/dev/null | jq -r '.data.nodes[0].node_token')
  if [ -n "$existing_node" ]; then
    feishu_wiki action=write token="$existing_node" content="$(cat "$file")"
  else
    feishu_wiki action=create space_id="$space_id" title="$node_name" content="$(cat "$file")"
  fi
}
```

---

### **方案 B: 使用 Bitable（结构化查询）**

创建表格：`知识同步日志`

| 日期 | Agent | 类型 | 内容摘要 | 同步状态 | 链接 |
|------|-------|------|----------|----------|------|

**推送逻辑**：

```bash
# 在 sync 完成后，记录到 Bitable
log_sync_to_bitable() {
  local agent_name="AgentA"  # 区分不同助手
  local sync_time="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  local commit_msg=$(git -C "$SYNC_DIR" log -1 --pretty=%B)

  feishu_bitable_create_record \
    app_token="bitable-app-token" \
    table_id="table-id" \
    fields='{
      "日期": "'"$sync_time"'",
      "Agent": "'"$agent_name"'",
      "类型": "知识同步",
      "内容摘要": "'"$commit_msg"'",
      "同步状态": "成功"
    }'
}
```

---

## 🔐 敏感信息处理（Feishu 侧）

即使已经过本地脱敏，**切勿**将以下内容写入 Feishu：

- API keys / tokens
- 用户真实姓名/联系方式（除非明确同意）
- 内部网络信息
- 未加密的密钥

**建议**：在推送 Feishu 前再运行一次 `sanitize_file` 函数。

---

## ⚙️ 配置步骤

### **1. 获取 Feishu 权限**
- 确保 OpenClaw 应用有 `doc:write`, `bitable:create`, `wiki:write` 等权限
- 查看：`feishu_app_scopes`

### **2. 创建 Wiki 空间或 Bitable 表**
- Wiki: 创建空间，获取 `space_id`
- Bitable: 创建表，获取 `app_token` 和 `table_id`

### **3. 更新同步脚本**

在 `scripts/knowledge-sync.sh` 末尾添加：

```bash
# 可选：同步到 Feishu
if command -v feishu_wiki &>/dev/null; then
  log "Syncing to Feishu Wiki..."
  for file in "$SYNC_DIR"/core/*.md; do
    [ -f "$file" ] || continue
    sync_to_feishu_wiki "$file"
  done
fi
```

### **4. 测试**
```bash
./scripts/knowledge-sync.sh
# 检查 Feishu 页面是否更新
```

---

## 🔄 替代方案：仅 Git 同步（无 Feishu）

如果不需要 Web UI，只使用 Git 同步即可。所有变更通过 Git 历史追溯。

---

**需要我帮你生成具体的 Feishu API 调用代码（创建空间/表格）吗？** 只需提供你的 Feishu 应用信息。
