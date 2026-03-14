# 🐵 ForkMonkey

> **Your digital pet that lives forever on GitHub and evolves with AI**

ForkMonkey is an autonomous, self-evolving digital collectible that combines:
- 🎮 **Tamagotchi-style** digital pets
- 🎨 **CryptoKitties** genetic breeding
- 🐵 **Bored Ape** collectible traits
- 🤖 **AI-powered** daily evolution

## What is ForkMonkey?

Each ForkMonkey is a unique digital creature that:
- **Lives on GitHub** as a repository
- **Evolves daily** through AI-powered mutations
- **Changes appearance** based on its DNA
- **Breeds through forks** - create new generations
- **Grows a family tree** across the GitHub network

### The Magic

1. **Your Monkey**: The owner of the GitHub repo owns the monkey
2. **Fork to Breed**: Fork the repo to create a child monkey with inherited + mutated traits
3. **AI Evolution**: Every day, an AI agent slightly modifies your monkey's appearance
4. **Secret DNA**: Monkey traits are stored as GitHub Secrets (only you can see them)
5. **Public Art**: The monkey's visual representation updates daily in the README
6. **Network Effect**: All monkeys form a family tree across GitHub

## How It Works

```
Day 1: 🐵 Born with random DNA
Day 2: 🐵 AI mutates color slightly
Day 3: 🐵 Grows a hat
Day 4: 🐵 Expression changes
...
Day 365: 🐵 Completely unique creature

Fork it: 👶 Child inherits 50% parent DNA + 50% random + daily mutations
```

## Features

### 🧬 Genetics System
- **DNA Traits**: Color, size, accessories, expressions, patterns
- **Inheritance**: Children inherit traits from parents with mutations
- **Rarity System**: Some traits are rarer than others
- **Generation Tracking**: Know your monkey's lineage

### ✨ Free AI Evolution
ForkMonkey now uses **GitHub Models** (gpt-4o) by default for **free** AI-powered evolution! No API key required.

(Optional: You can still use Claude by setting `ANTHROPIC_API_KEY` and `AI_PROVIDER=claude`)

- **Daily Mutations**: Claude AI subtly evolves your monkey
- **Smart Changes**: AI understands aesthetics and makes coherent changes
- **Personality Development**: Monkeys develop unique personalities over time

### 🎨 Visual System
- **SVG Generation**: Procedurally generated monkey art
- **Real-time Updates**: README shows current monkey state
- **History Tracking**: See how your monkey evolved over time

### 🌳 Network
- **Family Trees**: Visualize monkey genealogy
- **Rarity Rankings**: See the rarest monkeys in the network
- **Discovery**: Find and follow other monkeys

## Quick Start

### 1. Fork the Repository
Click the **"Fork"** button (top right) to create your own monkey repository.

### 2. Enable GitHub Actions
Go to the **Actions** tab in your new repository and click **"I understand my workflows, go ahead and enable them"**.

### 3. Run Genesis Workflow
1. Go to **Actions** tab
2. Select **"Initialize New Monkey"** from the left sidebar
3. Click **"Run workflow"** (blue button)
4. Wait for it to complete - your monkey is being born! 🐵

### 4. Enable Daily Evolution
1. In the **Actions** tab, select **"Daily Evolution"**
2. You'll see a banner saying "This workflow has a schedule that is disabled in forked repositories"
3. Click **"Enable workflow"** to let your monkey evolve every day!

### 5. Enable GitHub Pages
1. Go to **Settings** → **Pages**
2. Under "Build and deployment" > "Source", ensure **GitHub Actions** is selected
3. Your monkey will be live at `https://<username>.github.io/<repo-name>/`

### 6. (Optional) Configure AI
By default, ForkMonkey uses **GitHub Models (gpt-4o)** which is **FREE**!

If you prefer to use Claude:
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add a new secret: `ANTHROPIC_API_KEY`
3. Add a variable: `AI_PROVIDER` = `claude`

## Your Monkey

<!-- MONKEY_DISPLAY_START -->
<div align="center">

![Your Monkey](monkey_data/monkey.svg)

</div>
<!-- MONKEY_DISPLAY_END -->

## Monkey Stats

<!-- MONKEY_STATS_START -->
- **Generation**: 2
- **Age**: 119 days
- **Mutations**: 56
- **Rarity Score**: 31.7/100
<!-- MONKEY_STATS_END -->

## Family Tree

<!-- MONKEY_FAMILY_START -->
*Fork this repo to create children!*
<!-- MONKEY_FAMILY_END -->

## Development

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize your monkey
python src/cli.py init

# View in web interface
./start_web.sh

# Evolve monkey manually
python src/cli.py evolve --ai

# Show monkey stats
python src/cli.py show

# Run tests
pytest tests/
```

### Project Structure

```
forkMonkey/
├── .github/
│   └── workflows/
│       ├── daily-evolution.yml    # Daily AI evolution
│       ├── deploy-pages.yml       # Deploy to GitHub Pages
│       └── on-create.yml          # Initialize new monkey (template/fork)
├── src/
│   ├── genetics.py                # DNA and trait system
│   ├── evolution.py               # AI-powered evolution
│   ├── visualizer.py              # SVG monkey generator
│   ├── storage.py                 # Data persistence
│   └── cli.py                     # Command-line interface
├── web/
│   ├── index.html                 # Web interface
│   ├── style.css                  # Modern blocky design
│   ├── script.js                  # Interactive features
│   └── serve.py                   # Local web server
├── tests/                         # Comprehensive tests
├── monkey_data/
│   ├── dna.json                   # Monkey DNA
│   ├── history.json               # Evolution history
│   ├── stats.json                 # Monkey statistics
│   └── monkey.svg                 # Visual representation
└── README.md                      # This file (auto-updated)
```

## How to Breed

1. **Fork this repository** - Creates a child monkey
2. **Enable Actions** - Go to Actions tab and enable workflows
3. **Run Genesis** - Run "Initialize New Monkey" workflow
4. **Child inherits traits** - 50% from parent, 50% random
5. **Watch it grow** - Evolving daily with free AI!

## Rarity System

Traits have different rarity levels:
- **Common** (60%): Basic colors, simple patterns
- **Uncommon** (25%): Special colors, accessories
- **Rare** (10%): Unique patterns, special features
- **Legendary** (5%): Ultra-rare combinations

## Network Stats

<!-- NETWORK_STATS_START -->
- **Total Monkeys**: Calculating...
- **Generations**: Calculating...
- **Rarest Trait**: Calculating...
<!-- NETWORK_STATS_END -->

## API

### View Your Monkey's DNA
```bash
# DNA is stored in GitHub Secrets (private)
# Only the owner can see the full DNA
```

### Get Monkey Stats
```bash
curl https://api.github.com/repos/{owner}/forkMonkey/contents/monkey_data/stats.json
```

### View Family Tree
```bash
python src/cli.py family-tree
```

## Contributing

Want to improve ForkMonkey?
1. Fork this repo
2. Create a feature branch
3. Make your changes
4. Submit a PR to the main ForkMonkey repo

## Inspiration

- 🎮 **Tamagotchi**: Virtual pets that need care
- 🐱 **CryptoKitties**: Genetic breeding on blockchain
- 🐵 **Bored Ape Yacht Club**: Collectible traits
- 🌱 **SeedGPT**: AI-powered autonomous growth

## License

MIT License - Fork, breed, and evolve freely!

---

**Your monkey is unique. Your monkey is alive. Your monkey is forever on GitHub.** 🐵✨
