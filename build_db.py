# -*- coding: utf-8 -*-
"""
build_db.py
Convierte el volcado MariaDB (data/galpon_avicola.sql) en la base SQLite
data/galpon_avicola.db que usa el dashboard.

Uso:  python build_db.py
No modifica ningun dato: solo traduce la sintaxis de MariaDB a SQLite.
"""
import re
import sqlite3
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
SQL = RAIZ / "data" / "galpon_avicola.sql"
DB = RAIZ / "data" / "galpon_avicola.db"


def limpiar_create(bloque: str) -> str:
    """Quita lo que SQLite no entiende (ENGINE, CHARSET, tamanos de int)."""
    bloque = re.sub(r"\)\s*ENGINE=.*?;", ");", bloque, flags=re.S)
    bloque = re.sub(r"int\(\d+\)", "INTEGER", bloque)
    bloque = re.sub(r"varchar\(\d+\)", "TEXT", bloque)
    bloque = re.sub(r"decimal\(\d+,\d+\)", "REAL", bloque)
    bloque = re.sub(r"\bdatetime\b|\btimestamp\b", "TEXT", bloque)
    bloque = re.sub(r"\bdate\b", "TEXT", bloque)
    bloque = re.sub(r"\btext\b", "TEXT", bloque)
    bloque = bloque.replace("`", '"')
    # AUTO_INCREMENT y comentarios no aplican en SQLite
    bloque = re.sub(r"\s+AUTO_INCREMENT", "", bloque)
    return bloque


def main() -> None:
    texto = SQL.read_text(encoding="utf-8")
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    creates = re.findall(r"CREATE TABLE `\w+` \(.*?\) ENGINE=.*?;", texto, flags=re.S)
    for c in creates:
        con.execute(limpiar_create(c))
    inserts = re.findall(r"INSERT INTO `\w+` \(.*?\) VALUES\n.*?;\n", texto, flags=re.S)
    for ins in inserts:
        con.execute(ins.replace("`", '"'))
    con.commit()
    tablas = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    print(f"Base creada: {DB.name} con {len(tablas)} tablas")
    for (t,) in tablas:
        n = con.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
        print(f"  {t:22s} {n:3d} filas")
    con.close()


if __name__ == "__main__":
    main()
