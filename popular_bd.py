import sqlite3
from pathlib import Path
from helpers.file.json import read

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "censoescolar.db"
JSON_PATH = BASE_DIR / "instituicoes.json"

def importar_instituicoes():
    # 1. Carregar os registos do ficheiro JSON
    instituicoes = read(str(JSON_PATH))
    if not instituicoes:
        print("Nenhum dado encontrado no ficheiro JSON.")
        return

    # 2. Estabelecer ligação à base de dados SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 3. Preparar a instrução SQL de inserção
    sql = """
        INSERT INTO tb_instituicao_ensino (
            no_entidade, co_entidade, no_uf, sg_uf, co_uf,
            no_municipio, co_municipio, nu_ano_censo, qt_mat_bas,
            qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof,
            qt_mat_eja, qt_mat_esp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    # 4. Mapear os campos do JSON para uma lista de tuplos
    valores = [
        (
            item["no_entidade"],
            str(item["co_entidade"]),
            item["no_uf"],
            item["sg_uf"],
            int(item["co_uf"]),
            item["no_municipio"],
            int(item["co_municipio"]),
            int(item["nu_ano_censo"]),
            int(item["qt_mat_bas"]),
            int(item["qt_mat_inf"]),
            int(item["qt_mat_fund"]),
            int(item["qt_mat_med"]),
            int(item["qt_mat_prof"]),
            int(item["qt_mat_eja"]),
            int(item["qt_mat_esp"])
        )
        for item in instituicoes
    ]

    try:
        # 5. Executar a inserção em lote e confirmar as alterações
        cursor.executemany(sql, valores)
        conn.commit()
        print(f"Sucesso: {cursor.rowcount} registos inseridos em tb_instituicao_ensino.")
    except sqlite3.Error as erro:
        conn.rollback()
        print(f"Erro ao inserir dados na base de dados: {erro}")
    finally:
        conn.close()

if __name__ == "__main__":
    importar_instituicoes()