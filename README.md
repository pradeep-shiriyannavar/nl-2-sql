# 🌾 FoodQuery AI — Natural Language to SQL

> Ask your food management database in plain English.
> GPT-4o · FAISS · Multi-agent pipeline · Flask · Docker

![demo](assets/demo.gif)   ← record a GIF of you typing a question and getting results

## Architecture
User Question → Intent Agent → FAISS Semantic Search → 
Table Agent → Column Prune Agent → SQL Generation → MySQL

## Tech Stack
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-black)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![OpenAI](https://img.shields.io/badge/GPT--4o-Azure-green)
![FAISS](https://img.shields.io/badge/FAISS-Vector--Search-orange)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)

## What it does
- Converts plain English questions into SQL queries
- Multi-agent pipeline: Intent → Table → Column → SQL
- FAISS vector search for schema-aware table selection
- Supports 6 tables: donors, seekers, volunteers, transactions

## Example Queries
| Question | Generated SQL |
|---|---|
| How many donors are in Bengaluru? | SELECT COUNT(*) FROM m_donor WHERE... |
| Show all open transactions | SELECT * FROM m_food_trans WHERE ft_status='open'... |

## Quick Start
docker-compose up --build
# Visit http://localhost:5000
