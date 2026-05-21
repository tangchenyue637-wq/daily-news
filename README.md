# 📰 每日新闻推送 - 轻量版

**比 TrendRadar 简单 10 倍**，只干一件事：每天早上自动抓新闻 → AI 摘要 → 推送到你手机。

---

## 你需要什么

1. **Bark App**（已装）
2. **GitHub 账号**（已有）
3. **AI API Key**：DeepSeek 或 Kimi 都可以
   - DeepSeek：[platform.deepseek.com](https://platform.deepseek.com) 注册送 **10 元免费额度**
   - Kimi：[platform.moonshot.cn](https://platform.moonshot.cn) 注册送 **15 元免费额度**

---

## 部署步骤（5 分钟）

### 第 1 步：新建仓库
1. 打开 [github.com](https://github.com)
2. 右上角 **+** → **New repository**
3. 仓库名填 `daily-news` → 点 **Create repository**

### 第 2 步：上传文件
1. 在新仓库页面，点 **Add file** → **Upload files**
2. 把本压缩包解压后的 **所有文件和文件夹** 拖进去
3. 点 **Commit changes**

### 第 3 步：配 Secrets（就 2 个！）
1. 仓库顶部 **Settings** → 左侧 **Secrets and variables** → **Actions**
2. 点 **New repository secret**

| Name | Secret |
|------|--------|
| `BARK_URL` | 你的 Bark 地址，如 `https://api.day.app/ABCDEF123456` |
| `AI_API_KEY` | 你的 DeepSeek 或 Kimi API Key |

3. 点 **Add secret**

### 第 4 步：测试
1. 仓库顶部 **Actions** → 左侧 **每日新闻推送**
2. 右侧点 **Run workflow** → 再点 **Run workflow**
3. 等 1-2 分钟，看手机通知！

---

## 推送效果

> 📰 每日晨报 05月22日  
> 【商业科技】字节跳动 Q1 营收增长 40%...  
> 【AI人工智能】OpenAI 发布 GPT-5 预览版...  
> 【全球财经】美联储暗示年内降息两次...

---

## 常见问题

**Q: 没收到推送？**
- 检查 Bark App 通知权限开了吗
- 去 Actions 页面看运行记录是绿色 ✅ 还是红色 ❌

**Q: 想改时间？**
- 编辑 `.github/workflows/news.yml` 里的 `cron: '0 0 * * *'`
- `0 0` = 早 8 点，`0 22` = 早 6 点，`0 2` = 早 10 点

**Q: 想加新闻源？**
- 编辑 `config.json`，在对应分类里加 RSS 链接
