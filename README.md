<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">
 <h1>🐕 Milo Enterprise</h1>
 <p align="center">
 <strong>8 AI agents. 1 Mac mini. 24/7 automation.</strong>
 <br />
 An autonomous agent system that handles calendar, email, groceries, health tracking, coding, and more.
 <br />
 <br />
 <a href="https://milo-enterprise.netlify.app"><strong>View Landing Page »</strong></a>
 <br />
 <br />
 <a href="https://drive.google.com/file/d/1cIjpqDmtla8WeDMmx1yDZv4tQP2Sw8Hm/view">View Presentation</a>
 ·
 <a href="https://github.com/wherewereu/milo-enterprise/issues/new?labels=bug">Report Bug</a>
 ·
 <a href="https://github.com/wherewereu/milo-enterprise/issues/new?labels=enhancement">Request Feature</a>
 </p>
</div>

<details>
 <summary>Table of Contents</summary>
 <ol>
 <li><a href="#about-the-project">About The Project</a></li>
 <li><a href="#the-team">The Team</a></li>
 <li><a href="#architecture">Architecture</a></li>
 <li><a href="#discord-channels">Discord Channels</a></li>
 <li><a href="#skills">Skills</a></li>
 <li><a href="#getting-started">Getting Started</a></li>
 <li><a href="#usage">Usage</a></li>
 <li><a href="#roadmap">Roadmap</a></li>
 <li><a href="#contact">Contact</a></li>
 <li><a href="#acknowledgments">Acknowledgments</a></li>
 </ol>
</details>

---

## About The Project

Milo Enterprise is a multi-agent AI system running on a dedicated Mac mini. One orchestrator (Milo) coordinates seven specialist sub-agents to handle the chaos of daily life — from scheduling meetings to ordering groceries to reviewing code.

Key Principles:
- 🎯 Specialization over generalization — Each agent does one thing exceptionally well
- 🔄 Review loops — Code goes through Heph → Theo review cycle before shipping
- 👤 Human-in-the-loop — Some tasks need human input; the system knows when to ask
- 📱 Multi-channel — iMessage, Discord, Telegram, Email — all unified through Milo

### Built With

* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
* ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
* ![OpenClaw](https://img.shields.io/badge/OpenClaw-FF6B35?style=for-the-badge)
* ![Claude](https://img.shields.io/badge/Claude-8B5CF6?style=for-the-badge&logo=anthropic&logoColor=white)
* ![MiniMax](https://img.shields.io/badge/MiniMax-00D4AA?style=for-the-badge)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## The Team

| Agent | Name | Role | Specialty |
|:-----:|------|------|-----------|
| 🐕 | Milo Blake | Orchestrator & CEO | Decision layer — everything flows through Milo |
| 📚 | Archimedes (Archie) | Research Agent | Web search, fact-checking, deep dives |
| 📅 | Atropos (Atro) | Calendar & Time | Scheduling, reminders, time management |
| 🛒 | Eris | Procurement Agent | Instacart, Amazon, DoorDash orders |
| ⚒️ | Hephaestus (Heph) | Coding Agent | Writes code, builds features, iterates |
| 💪 | Heracles (Herc) | Health & Wellness | Water tracking, sleep, fitness goals |
| 📧 | Mercury (Merc) | Communications Agent | Email management, drafts, LinkedIn posts |
| ⚖️ | Themis (Theo) | Code Reviewer | Reviews all code before shipping |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ JUSTINE                                                       │
│ (The Human™)                                                  │
└─────────────────────┬───────────────────────────────────────┘
                     │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ 🐕 MILO                                                        │
│ Orchestrator & CEO                                            │
│ iMessage • Discord • Telegram                                  │
└─────────────────────┬───────────────────────────────────────┘
                     │
     ┌───────────────┼────────────────┐
     ▼               ▼                ▼
┌───────────┐  ┌───────────┐  ┌───────────┐
│ Archie    │  │ Atro      │  │ Eris      │
│ Research  │  │ Calendar  │  │ Shopping  │
└───────────┘  └───────────┘  └───────────┘
     ▼               ▼                ▼
┌───────────┐  ┌───────────┐  ┌───────────┐
│ Merc      │  │ Herc      │  │ Heph→Theo │
│ Comms     │  │ Health    │  │Code Review│
└───────────┘  └───────────┘  └───────────┘

┌─────────────────────────────────────────────────────────────┐
│ DISCORD                                                        │
│ Command Center • Round-Table • Break Room                     │
│ (per-agent output/logs/memory channels)                       │
└─────────────────────────────────────────────────────────────┘
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Discord Channels

Discord is the **Command Center** — every agent posts delegation events, task completions, and errors to dedicated channels.

| Channel | ID | Purpose | Logs/Memory |
|---------|-----|---------|-------------|
| 🎯 Command Center | [INSERT DISCORD CHANNEL ID] | Strategic planning, delegation, results | No |
| 🗣️ Round-Table | [INSERT DISCORD CHANNEL ID] | Open team discussion | No |
| 💬 Break Room | [INSERT DISCORD CHANNEL ID] | Agent casual chat | No |
| 🔍 Research Output | [INSERT DISCORD CHANNEL ID] | Archie results | Yes |
| 📧 Comms Output | [INSERT DISCORD CHANNEL ID] | Merc results | Yes |
| 🛒 Procurement Output | [INSERT DISCORD CHANNEL ID] | Eris results | Yes |
| 📅 Temporal Output | [INSERT DISCORD CHANNEL ID] | Atro results | Yes |
| 💪 Wellness Output | [INSERT DISCORD CHANNEL ID] | Herc results | Yes |
| ⚒️ Code Output | [INSERT DISCORD CHANNEL ID] | Heph results | No |
| ⚖️ Review Output | [INSERT DISCORD CHANNEL ID] | Theo results | No |

**Round-Table and Break Room have NO logs/memory channels** — they're casual collaboration spaces.

Full bot/token setup in `~/.openclaw/agent-bot-tokens.json`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Skills

| Skill | Description |
|-------|-------------|
| agent-browser | Headless browser automation with accessibility tree |
| archimedes | Research agent — web search, fact-checking, deep dives |
| atropos | Calendar agent — scheduling, reminders, time management |
| eris | Procurement agent — orders, Instacart, Amazon |
| heracles | Health agent — water, sleep, fitness tracking |
| hephaestus | Code agent — writes and iterates on code |
| merc-linkedin-daily | Daily LinkedIn post workflow |
| mercury | Communications agent — email, drafts, LinkedIn |
| themis | Code review — reviews all Hephaestus output |
| diet-tracker | Calorie counting and nutrition tracking |
| expense-tracker | Budget management and spending insights |
| proactive-agent | Memory architecture, self-healing, reverse prompting |
| instacart | Grocery ordering automation |
| image-collector | Image search and collection |

<p align="right">(<a href="#readme-top">back to top)</a></p>

---

## Getting Started

### Prerequisites

* Mac mini (or any always-on computer)
* [OpenClaw](https://openclaw.ai) installed
* Claude Pro subscription ($20/mo)
* MiniMax API ($200/year plan)
* Discord server with bot tokens per agent

### Installation

1. Clone the repo

 ```bash
 git clone https://github.com/wherewereu/milo-enterprise.git
 ```

2. Copy environment template

 ```bash
 cp .env.example .env
 ```

3. Set up Discord bots (see `agent-delegation-system-readme.md` in workspace for full Discord setup)

4. Configure agent tokens

 ```bash
 nano ~/.openclaw/agent-bot-tokens.json
 ```

5. Install OpenClaw

 ```bash
 npm install -g openclaw

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Usage

### Discord Posting
```bash
# Post to round-table (default)
python3 discord-post.py Milo "Hello from Milo!"

# Post to specific channel
python3 discord-post.py Milo "Hello" --channel 1483891285822537740

# Reply to a message
python3 discord-post.py Archie "Research complete" --reply-to 1234567890
```

### Backup to iCloud
```bash
./backup.sh
```

### Twitch Monitoring
```bash
python twitch-poller.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Roadmap

- [x] 8-agent team setup
- [x] Discord integration (Command Center, Round-Table, Break Room)
- [x] Code review pipeline (Heph → Theo)
- [ ] Voice interface via Alexa
- [ ] Multi-user support
- [ ] Mobile app for agent management

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Contact

Justine Delano - AI Engineer | Incident Manager @ Amazon

- 💼 [LinkedIn](https://www.linkedin.com/in/justineadelano/)
- 🎮 [Discord](https://discord.com/users/931741302079492107)
- 📧 justine.delano26@gmail.com
- 🌐 [milo-enterprise.netlify.app](https://milo-enterprise.netlify.app)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Acknowledgments

* [OpenClaw](https://openclaw.ai) — The agent framework powering everything
* [Anthropic Claude](https://anthropic.com) — The brain behind the agents
* [MiniMax](https://minimax.io) — Cost-effective daily operations

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/wherewereu/milo-enterprise.svg?style=for-the-badge
[contributors-url]: https://github.com/wherewereu/milo-enterprise/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/wherewereu/milo-enterprise.svg?style=for-the-badge
[forks-url]: https://github.com/wherewereu/milo-enterprise/network/members
[stars-shield]: https://img.shields.io/github/stars/wherewereu/milo-enterprise.svg?style=for-the-badge
[stars-url]: https://github.com/wherewereu/milo-enterprise/stargazers
[issues-shield]: https://img.shields.io/github/issues/wherewereu/milo-enterprise.svg?style=for-the-badge
[issues-url]: https://github.com/wherewereu/milo-enterprise/issues
[license-shield]: https://img.shields.io/github/license/wherewereu/milo-enterprise.svg?style=for-the-badge
[license-url]: https://github.com/wherewereu/milo-enterprise/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/justineadelano
