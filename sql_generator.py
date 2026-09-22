import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# GROQ CLIENT
# ============================================================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-120b"


# ============================================================
# GENERATE SQL
# ============================================================
def generate_sql(question, schema, relationships):
    schema_text = ""
    for table, columns in schema.items():
        schema_text += f"\nTABLE: {table}\n"
        for column in columns:
            schema_text += f"- {column}\n"

    relationship_text = "\n".join(relationships)

    prompt = f"""
You are an expert MySQL developer.
Convert the user's natural-language question
into a valid MySQL SELECT query.

DATABASE SCHEMA:
{schema_text}

RELATIONSHIPS:
{relationship_text}

USER QUESTION:
{question}

RULES:
1. Generate only SELECT queries.
2. Never generate INSERT.
3. Never generate UPDATE.
4. Never generate DELETE.
5. Never generate DROP.
6. Never generate ALTER.
7. Never generate TRUNCATE.
8. Use only tables and columns present in the schema.
9. Use proper JOIN conditions.
10. Use MySQL syntax.
11. Return ONLY the SQL query.
12. Do not use markdown.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an expert SQL generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    sql = response.choices[0].message.content.strip()

    # Remove markdown fences if generated
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    return sql.strip()


# ============================================================
# EXPLAIN SQL
# ============================================================
def explain_sql(sql):
    prompt = f"""
Explain this MySQL query in simple language.

SQL:
{sql}

Explain:
1. Tables used
2. Joins
3. Filtering
4. Grouping
5. Sorting
6. Aggregation
7. Final result

Keep the explanation suitable for a beginner software engineer.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You explain SQL clearly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
