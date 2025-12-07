import os
import django
import sqlite3
import psycopg2

# ---------------- INITIALIZE DJANGO SETTINGS ----------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_system.settings')  # CHANGE IF PROJECT NAME DIFFERENT
django.setup()
# ------------------------------------------------------------

from django.conf import settings

# ---------------- CONFIG ----------------
SQLITE_DB_PATH = os.path.join(settings.BASE_DIR, 'db.sqlite3')

POSTGRES = {
    'NAME': settings.DATABASES['default']['NAME'],
    'USER': settings.DATABASES['default']['USER'],
    'PASSWORD': settings.DATABASES['default']['PASSWORD'],
    'HOST': settings.DATABASES['default']['HOST'],
    'PORT': settings.DATABASES['default']['PORT'],
}
# -----------------------------------------


def get_sqlite_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]


def migrate_table(table, sq_cursor, pg_cursor, pg_conn):
    print(f"\n📦 Migrating table: {table}")

    sq_cursor.execute(f"SELECT * FROM {table}")
    rows = sq_cursor.fetchall()
    if not rows:
        print(f"⚠️ No rows in {table}, skipping...")
        return

    # Get column names
    sq_cursor.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in sq_cursor.fetchall()]

    reserved = {"user", "order", "group"}
    col_string = ",".join([f'"{c}"' if c.lower() in reserved else c for c in columns])
    placeholders = ",".join(["%s"] * len(columns))
    insert_query = f'INSERT INTO {table} ({col_string}) VALUES ({placeholders})'

    for row in rows:
        row = list(row)

        # ---- SPECIAL FIX FOR auth_user BOOLEAN FIELDS ----
        if table == "auth_user":
            bool_fields = ["is_superuser", "is_staff", "is_active"]
            for idx, col in enumerate(columns):
                if col in bool_fields and isinstance(row[idx], int):
                    row[idx] = bool(row[idx])  # Convert 0/1 → False/True

        try:
            pg_cursor.execute(insert_query, row)
        except Exception as e:
            print("\n❌ ERROR DETAILS:")
            print("Table :", table)
            print("Row   :", row)
            print("Error :", e)
            pg_conn.rollback()



def main():
    # Connect to SQLite
    sq_conn = sqlite3.connect(SQLITE_DB_PATH)
    sq_cursor = sq_conn.cursor()

    # Connect to PostgreSQL
    pg_conn = psycopg2.connect(
        dbname=POSTGRES['NAME'],
        user=POSTGRES['USER'],
        password=POSTGRES['PASSWORD'],
        host=POSTGRES['HOST'],
        port=POSTGRES['PORT']
    )
    pg_cursor = pg_conn.cursor()

    tables = get_sqlite_tables(sq_cursor)
    EXCLUDE = ['django_migrations']  # do not copy migration history

    for table in tables:
        if table in EXCLUDE:
            print(f"⏭ Skipped table: {table}")
            continue
        migrate_table(table, sq_cursor, pg_cursor, pg_conn)

    pg_conn.commit()
    pg_conn.close()
    sq_conn.close()
    print("\n🎉 Migration completed successfully!")


if __name__ == "__main__":
    main()
