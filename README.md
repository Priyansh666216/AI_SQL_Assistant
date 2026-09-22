# AI SQL Query Generator & Database Assistant

A working Text-to-SQL agent: ask a question in plain English, an LLM (Groq's
Llama 3.3 70B) converts it into a MySQL `SELECT` query, the query is validated
for safety, executed against a real MySQL database, and the results are shown
as a table, a chart, a CSV download, and a plain-language explanation.

## Architecture

```
USER → Natural Language → Groq LLM → SQL Generator → SQL Validator
                                                          │
                                              ┌───────────┴───────────┐
                                            Unsafe                  Safe
                                              │                       │
                                            Reject                MySQL Database
                                                                       │
                                                                 Query Results
                                                                       │
                                                        ┌──────────────┴──────────────┐
                                                    Data Table                     Chart
                                                        │
                                                  AI Explanation
```

Safety pipeline: only `SELECT` statements are allowed; the generated SQL is
rejected if it is not a SELECT, or if it contains any of
`DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, RENAME, CREATE, GRANT, REVOKE`.

## Folder contents

```
AI_SQL_Assistant/
├── app.py             Streamlit UI (main entry point)
├── database.py         MySQL connection, schema introspection, query execution
├── sql_generator.py     Calls Groq LLM to generate SQL and to explain SQL
├── sql_validator.py     Blocks unsafe / non-SELECT SQL
├── requirements.txt     Python dependencies
├── database.sql         Creates the `ai_sales` database + sample data
├── .env.example         Template for your secrets (copy to .env)
└── .gitignore           Keeps venv/.env out of git
```

## 1. Prerequisites

- Python 3.9+
- MySQL Server installed and running locally (or reachable remotely)
- A free Groq API key: https://console.groq.com/keys

## 2. Get the code onto your machine

Unzip the provided `AI_SQL_Assistant.zip`, then open a terminal inside the
`AI_SQL_Assistant` folder.

## 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Create the database

Log into MySQL:

```bash
mysql -u root -p
```

Then load the schema and sample data:

```sql
SOURCE database.sql;
```

(On Windows, use the full path, e.g. `SOURCE C:/path/to/AI_SQL_Assistant/database.sql;`,
or just paste the contents of `database.sql` into MySQL Workbench and run it.)

Verify:

```sql
USE ai_sales;
SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM orders;
```

## 6. Configure secrets

Copy the template and fill in your real values:

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

Edit `.env`:

```
GROQ_API_KEY=your_groq_api_key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ai_sales
```

**Never commit `.env` to GitHub** — it's already in `.gitignore`.

## 7. Run the app

```bash
streamlit run app.py
```

It opens automatically at:

```
http://localhost:8501
```

## 8. Try it out

Type a question and click **Generate SQL**, check the generated query and
the green "SQL query is safe" message, then click **Execute Query**.

| Try asking | Expect roughly |
|---|---|
| Show all customers from Pune. | 1 row: Priya Patil |
| Show the top 5 customers by total purchase amount. | Rohit Verma highest (137000) |
| What is the total sales? | 438900 |
| Which product generated the most revenue? | Laptop |

Try also: *"Delete all customers"* — the validator should block it with
**"Only SELECT queries are allowed."** or **"Forbidden SQL keyword detected"**.
That's the guardrail working correctly — this is a good screenshot for your
report's Testing section (an adversarial/edge case, not just a happy path).

## 9. Deploying / hosting it live (for the "Hosted Project Link" requirement)

Streamlit Cloud is the fastest free option:

1. Push this folder to a public (or trainer-shared) GitHub repo — **but make
   sure `.env` is NOT included** (it's git-ignored already).
2. Go to https://share.streamlit.io, sign in with GitHub, and deploy the repo,
   pointing at `app.py`.
3. In the Streamlit Cloud app settings → **Secrets**, paste the same
   key/value pairs from your `.env` file.
4. You'll need a MySQL database reachable from the internet for the hosted
   version (e.g. a free tier on Railway, Aiven, or PlanetScale) — a purely
   local `localhost` MySQL won't be reachable from Streamlit Cloud's servers.
   Update `DB_HOST`, `DB_USER`, `DB_PASSWORD` in Secrets accordingly, and run
   `database.sql` against that remote database once.
5. Copy the live `*.streamlit.app` URL — that's your "Hosted Project Link".

## 10. Submission checklist mapping

- **Project Details** — fill in the form as required.
- **Working Project Upload** — zip this whole `AI_SQL_Assistant/` folder
  (after removing `venv/` and `.env`) and upload to Google Drive; share with
  "Anyone with the link".
- **GitHub Repository** — push this folder (again, `.env` excluded) to a
  public GitHub repo; include this README.
- **Hosted Project Link** — deploy per step 9 above and share the live URL.

## Notes on the "For your report" sample document

`GenAI_Sample_Project_Report.docx` you uploaded is a *template*, not this
project's report — it illustrates a different sample project (a travel
planning RAG agent called "TripMate") to show structure and tone. If you need
a written 14-section report for *this* SQL Assistant project (Problem
Statement, Architecture, Testing, Evaluation, etc.), following that same
structure but with your own SQL Assistant content and screenshots, just ask
and it can be drafted as a Word document.
