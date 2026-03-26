# Proactive Ideas

> What could I build RIGHT NOW that would make my human say "I didn't ask for that but it's amazing"?

## 2026-03-26

**Idea: AppleSite 自动健康检查器**

- **Problem:** AppleSite 可能因为域名失效、API挂掉等原因变成无效站点，但管理员无法实时知道。
- **Solution:** 创建一个后台定时任务（django-background-tasks），每天检查所有启用的 AppleSite 的 API 可达性。对连续失败 N 次的站点自动禁用，并在 Admin 首页显示警告，同时发送飞书消息通知。
- **Delight factor:** 零维护成本，系统自愈能力，防止无效资源站影响用户体验。
- **Implementation effort:** ~2 hours (add model for health tracking, periodic task, admin dashboard widget, feishu notification)
- **Potential extension:** 结合 Star Office 状态同步，在看板上显示站点健康指数。

**其他构想：**
- TVBox 配置一键导出（包含所有站点最新分类）
- 资源访问量统计仪表盘（基于 request logs）
- 自动封面图抓取（针对自定义 CMS）
