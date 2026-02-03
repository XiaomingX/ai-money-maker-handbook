# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is **AI Money Maker Handbook (兼职赚钱方案博物馆)** - a Chinese-language content repository focused on AI-powered side hustles and entrepreneurship guidance for programmers and early-stage founders.

### Content Structure

The repository contains two main content directories:

1. **程序员的副业赚钱宝典** (Programmer's Side Hustle Handbook)
   - 425 chapters (ch0001.md - ch0425.md)
   - Practical guides for programmers to monetize their technical skills
   - Focus on actionable business strategies, financial calculations, and Chinese market specifics

2. **创业者早期的烦恼树洞** (Early-Stage Founder's Q&A)
   - 39 chapters covering startup fundamentals
   - Topics include: PMF, funding rounds, equity, compliance, metrics (MAU, ARR, LTV/CAC)
   - Q&A format with user questions and detailed responses

## Content Writing Philosophy

### Agent Configuration (.prompt/ directory)

The repository uses a specialized content generation framework defined in:

- **.prompt/agent.md** - Defines the "Side Hustle Architect" persona
  - Role: Technical entrepreneur with 10 years experience
  - Mission: Transform "technical thinking" into "business thinking"
  - Tone: Direct, data-driven, structured (no fluff or motivational language)

- **.prompt/skill.md** - Five content generation skills:
  1. `generate_business_ledger` - Financial calculations (startup costs, CAC, margins, ROI)
  2. `define_mvp_strategy` - Minimum viable product guidance
  3. `china_local_traffic_hacking` - Chinese platform marketing (WeChat, Douyin, Xiaohongshu, Xianyu)
  4. `risk_assessment` - Legal, platform, and delivery risks
  5. `case_study_simulation` - Realistic programmer success stories

### Content Requirements

When creating or updating chapters in 程序员的副业赚钱宝典:

1. **Financial Specificity**
   - Include concrete numbers: pricing (¥), costs, profit margins, payback periods
   - Calculate: CAC (Customer Acquisition Cost), LTV (Lifetime Value), ROI
   - Provide monthly revenue estimates for individual and team scenarios

2. **Chinese Market Focus**
   - Reference platforms: 微信, 抖音, 快手, 小红书, 闲鱼, 淘宝, 1688, 知识星球
   - Avoid generic international advice
   - Consider Chinese regulations and compliance

3. **Actionable SOP Format**
   - Step-by-step instructions (like code documentation)
   - Avoid vague advice like "improve yourself" or "broaden horizons"
   - Focus on: money, traffic, conversion, delivery

4. **Business Metrics**
   - Include: 定价 (pricing), 投入成本 (investment), 回本周期 (payback period)
   - 利润率 (profit margin), 毛利率 (gross margin)
   - 北极星指标 (North Star Metric), KPI, OKR where relevant

5. **Compliance**
   - Only legal side hustles
   - Flag gray-area activities (web scraping personal data, game cheats)
   - Highlight regulatory red lines

## Automation

### GitHub Actions

- **Workflow**: `.github/workflows/task.yml`
  - Runs daily at 23:30 UTC (cron: "30 23 * * *")
  - Updates `DATA_UPDATE.md` with current timestamp
  - Auto-commits and pushes to main branch

## Git Workflow

- **Main branch**: `main`
- **Current status**: Modified `.gitignore`
- **Commit style**: Descriptive messages in Chinese or English

## File Naming Conventions

- Chapter files: `ch####.md` (zero-padded 4 digits)
- Range: ch0001.md to ch0425.md (程序员的副业赚钱宝典)
- Range: ch0001.md to ch0039.md (创业者早期的烦恼树洞)

## Content Update Workflow

When updating chapters (as mentioned in mm-README.md):

1. Read `.prompt/agent.md` and `.prompt/skill.md` for persona and skills
2. Target chapters: ch0374.md onwards
3. Enhance with:
   - More operational details
   - Chinese market context
   - Specific metrics (pricing, costs, cycles, margins, KPIs)
   - Realistic, non-exaggerated content
4. Apply all five skills from skill.md to each chapter

## Repository Purpose

This is a **content contribution platform** where users can:
- Submit AI money-making case studies via GitHub issues
- Share articles, websites, blogs, tweets about AI monetization
- Access curated resources for indie hackers and developers

Related resources linked in README:
- 跨境出海技术栈 (Cross-border tech stack)
- AI搞钱原则手册 (AI money-making principles)
- 构建你自己的X (Build your own X)
- 1000个中国独立开发者项目 (1000 Chinese indie developer projects)
