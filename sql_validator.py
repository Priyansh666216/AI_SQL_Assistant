import re

# ============================================================
# FORBIDDEN SQL COMMANDS
# ============================================================
FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "RENAME",
    "CREATE",
    "GRANT",
    "REVOKE"
]


# ============================================================
# VALIDATE SQL
# ============================================================
def validate_sql(sql):
    if not sql:
        return False, "SQL query is empty."

    sql = sql.strip()

    # Remove markdown fences
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)
    sql = sql.strip()

    # Only SELECT queries allowed
    if not re.match(r"^SELECT\b", sql, flags=re.IGNORECASE):
        return False, "Only SELECT queries are allowed."

    # Check dangerous keywords
    upper_sql = sql.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf"\b{keyword}\b"
        if re.search(pattern, upper_sql):
            return False, f"Forbidden SQL keyword detected: {keyword}"

    return True, "SQL query is safe."
