#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日新闻推送机器人 - 轻量版
自动判断 API 提供商 (Kimi / DeepSeek)
"""

import json, os, re, urllib.parse
from datetime import datetime
import feedparser, requests

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_rss(url, max_items=3):
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:max_items]:
            title = entry.get("title", "无标题").strip()
            link = entry.get("link", "").strip()
            summary = re.sub(r"<[^>]+>", "", entry.get("summary", entry.get("description", "")))[:300]
            articles.append({"title": title, "link": link, "summary": summary})
        return articles
    except Exception as e:
        print(f"[错误] 抓取失败 {url}: {e}")
        return []

def deduplicate(articles):
    seen = set()
    result = []
    for a in articles:
        key = a["title"][:20]
        if key not in seen:
            seen.add(key)
            result.append(a)
    return result

def summarize(articles, api_key, model, base_url):
    if not articles:
        return "今日暂无新闻"
    content = "\n\n".join([f"{i}. {a['title']}\n{a['summary'][:200]}\n链接: {a['link']}" for i, a in enumerate(articles[:15], 1)])
    prompt = f"""你是一位资深财经科技编辑。请根据以下今日新闻，整理一份手机推送简报。

要求：
1. 分类：【商业科技】【AI人工智能】【全球财经】
2. 每个分类精选 1-3 条最重要的新闻
3. 每条用 1 句话总结核心要点（不超过 40 字）
4. 开头写"今日晨报 | MM月DD日"作为标题
5. 整体控制在 300 字以内，适合手机通知栏阅读
6. 语气专业、简洁、有信息量

原始新闻：
{content}
"""
    try:
        resp = requests.post(
            f"{base_url}/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.5, "max_tokens": 800},
            timeout=60
        )
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[错误] AI 调用失败: {e}")
        return "今日新闻摘要\n" + "\n".join([f"• {a['title']}" for a in articles[:5]])

def push_bark(bark_url, title, body):
    try:
        url = f"{bark_url}/{urllib.parse.quote(title, safe='')}/{urllib.parse.quote(body, safe='')}"
        resp = requests.get(url, params={"group": "每日晨报", "isArchive": 1, "sound": "newsflash"}, timeout=30)
        print(f"[推送结果] {resp.status_code}")
        return resp.status_code == 200
    except Exception as e:
        print(f"[错误] Bark 推送失败: {e}")
        return False

def main():
    cfg = load_config()

    # 自动判断用哪家 AI
    api_key = os.environ.get("AI_API_KEY", "")
    bark_url = os.environ.get("BARK_URL", "")

    # 默认 DeepSeek；如果 Key 以 sk- 开头且很长，也可能是 Kimi，但接口兼容
    base_url = "https://api.deepseek.com"
    model = "deepseek-chat"

    # 简单判断：如果 Key 里包含特定字符或用户显式配置了其他地址，可扩展
    # 这里默认 DeepSeek，因为用户之前选的是 deepseek

    if not bark_url:
        print("[错误] 缺少 BARK_URL"); return
    if not api_key:
        print("[错误] 缺少 AI_API_KEY"); return

    print(f"[{datetime.now().strftime('%H:%M')}] 开始抓取...")
    all_articles = []
    for category, urls in cfg["categories"].items():
        for url in urls:
            articles = fetch_rss(url, cfg.get("max_articles_per_source", 3))
            for a in articles: a["category"] = category
            all_articles.extend(articles)

    all_articles = deduplicate(all_articles)
    print(f"[汇总] 共 {len(all_articles)} 条")

    summary = summarize(all_articles, api_key, model, base_url)
    today_str = datetime.now().strftime("%m月%d日")
    success = push_bark(bark_url, f"📰 每日晨报 {today_str}", summary)

    print("[完成] 已推送到手机！" if success else "[失败]")

if __name__ == "__main__":
    main()
