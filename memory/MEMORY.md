# 长期间记忆

## 系统与技能
- 部署了 Star Office UI（像素办公室看板）于 2026-03-08
- 服务地址：http://127.0.0.1:19000
- 技能列表：find-skills、openai-image-gen、openai-whisper-api、healthcheck、weather、skill-creator
- **Proactive Agent** 已激活（2026-03-11 完成 onboarding）

## 知识同步系统 🚀
**部署时间**: 2026-03-11  
**架构**: 云端 Git 双向同步 + 敏感内容过滤  
**同步频率**: 每 10 分钟（可配置）  
**同步内容**:
- ✅ Core: SOUL.md, USER.md, AGENTS.md, HEARTBEAT.md, ONBOARDING.md
- ✅ Memory: MEMORY.md + 每日笔记（自动脱敏）
- ✅ Notes: proactive-tracker, recurring-patterns, outcome-journal
- ✅ Skills: SKILL.md, README.md, scripts/
- ✅ State: Star Office 公开状态（移除密钥）
- ❌ 排除: local/ 私有数据、.env、credentials、working-buffer

**核心文件**:
- `scripts/knowledge-sync.sh` - 同步引擎（拉取→过滤→推送）
- `sync/` - 共享目录（挂载云端 Git）
- `sync/.gitignore` - 敏感模式过滤
- `sync/README.md` - 完整使用说明
- `sync/cron-job.json` - OpenClaw 定时任务配置

**安全策略**:
- 自动重写密码、API keys、tokens、credentials 为 `[REDACTED]`
- 仅同步脱敏后的副本，原始敏感数据保留在 `local/` 不共享
- Git commit 包含主机名和时间戳，便于追踪

**状态**: ⏳ 等待配置云端 Git remote 并首次推送

---

## Star Office 状态同步规则 ⚠️
**这是主人明确要求的强制流程，必须严格遵守：**

### 接到任务时
```bash
python3 set_state.py <状态> "<任务描述>"
```
然后才开始工作。

### 完成任务后
```bash
python3 set_state.py idle "待命中"
```
然后再回复主人。

### 常用状态
- `writing` - 写作/文档整理
- `researching` - 研究中
- `executing` - 执行任务
- `syncing` - 同步中
- `error` - 出错/排查中
- `idle` - 待命中

> 核心原则：让主人在看板上实时看到我的状态变化。

## 安全配置
- 侧边栏默认密码：`1234`（**必须改为强密码**）
- 长期运行需设置环境变量 `ASSET_DRAWER_PASS`
- Gemini API 可选（生图功能）：`GEMINI_API_KEY`、`GEMINI_MODEL`

## 部署细节
- 位置：`/home/lyw/.openclaw/workspace/Star-Office-UI`
- Python 依赖：Flask 3.0.2、Pillow 10.4.0
- 状态文件：`state.json`
- 启动命令：`cd backend && python3 app.py`
- 健康检查端点：`/health`

## 计划
- [ ] 配置公网访问（Cloudflare Tunnel）
- [ ] 设置 systemd 服务
- [ ] 邀请其他 OpenClaw 加入（join keys）
- [x] 智慧食堂系统数据抓取（完成于 2026-03-10，608 条员工信息，99 条公告）

## 智慧食堂系统（2026-03-10）
- **登录方式**：账号密码（sxsljttzjs）
- **数据抓取**：
  - 通知公告：99 条（本周食谱为主）
  - 员工信息：608 条（含姓名、部门、余额等）
- **技术要点**：
  - Chrome 需禁用 GPU 启动（`--disable-gpu` 等）
  - elevated 权限配置（sudo NOPASSWD）
  - 使用 JavaScript evaluate 提取表格数据

## 备注
- 系统显示总员工数 304，但 400 条/页设置抓取到 608 条（可能存在重复或虚拟滚动计数问题）
- 仅 1 条公告状态为"正常"（2026.3.9 本周食谱）

---
最后更新：2026-03-08
