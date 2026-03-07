# Daily Bible Verse Generator

An automated pipeline that generates daily Bible verse images and stores them in a PostgreSQL database. It runs on a scheduled GitHub Actions workflow every day at 7:00 PM IST (1:30 PM UTC).

## How It Works

1. **Fetch Readings** – Scrapes tomorrow's Catholic daily readings from [USCCB](https://bible.usccb.org/).
2. **Select Verse** – Sends the readings to a Groq LLM (Llama 3.3 70B) which picks the most inspirational verse and returns it as JSON.
3. **Generate Images** – Calls the Freepik AI (Mystic) API to generate two images:
   - **Symbolic** – Represents the spiritual/symbolic meaning of the verse.
   - **Biblical** – Depicts a specific biblical story or character related to the verse.
4. **Add Text Overlay** – Uses Pillow to intelligently overlay the verse and reference on each image, choosing text placement and color based on the image's brightness and complexity.
5. **Save to Database** – Stores the images, prompts, verse text, and reference in PostgreSQL. Errors are also logged to the database.

## Architecture

```
main.py            # Orchestrates the pipeline
├── get_reading.py # Scrapes USCCB for tomorrow's readings
├── prompts.py     # LLM prompt templates and helper functions
├── llm.py         # Groq API wrapper
├── generate_image.py # Freepik AI image generation (with polling)
├── text_overlay.py   # Pillow-based text overlay logic
├── queries.py     # PostgreSQL schema and INSERT queries
└── db_conn.py     # Database connection helper
```

## Requirements

- Python 3.11+
- PostgreSQL database
- [Groq API key](https://console.groq.com/) (free tier available)
- [Freepik API key](https://www.freepik.com/api) (paid, required for image generation)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
DB_URI=postgresql://user:password@localhost:5432/your_database
llm_api_key=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
freepik_api_key=xxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Create the database table

```bash
python - <<'EOF'
from queries import schema
import db_conn, psycopg2
conn = db_conn.get_connection()
with conn.cursor() as cur:
    cur.execute(schema)
conn.commit()
conn.close()
print("Table created.")
EOF
```

### 4. Run the pipeline

```bash
python main.py
```

## GitHub Actions (Automated)

The workflow in `.github/workflows/daily-job.yml` triggers automatically every day at **7:00 PM IST**.

### Required Secrets

Configure these in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|--------|-------------|
| `DB_URI` | PostgreSQL connection string |
| `LLM_API_KEY` | Groq API key |
| `FREEPIK_API_KEY` | Freepik API key |

### Manual Trigger

You can also run the workflow on demand from the **Actions** tab by clicking **Run workflow**.

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS daily_verses (
    id              SERIAL PRIMARY KEY,
    day             DATE UNIQUE NOT NULL,
    reference       TEXT NOT NULL,
    verse           TEXT NOT NULL,
    prompt_general  TEXT,
    prompt_bible    TEXT,
    img1            BYTEA,
    img2            BYTEA,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status          TEXT,
    error_message   TEXT
);
```

## Fonts

The text overlay uses [EB Garamond](https://fonts.google.com/specimen/EB+Garamond) (`fonts/EBGaramond-VariableFont_wght.ttf`), which is included in the repository.
