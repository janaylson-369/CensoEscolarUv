CREATE TABLE tb_instituicao_ensino (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    co_entidade INTEGER,
    nu_ano_censo INTEGER,
    no_entidade TEXT,
    co_uf INTEGER,
    sg_uf TEXT,
    no_uf TEXT,
    co_municipio INTEGER,
    no_municipio TEXT,
    qt_mat_bas INTEGER DEFAULT 0,
    qt_mat_inf INTEGER DEFAULT 0,
    qt_mat_fund INTEGER DEFAULT 0,
    qt_mat_med INTEGER DEFAULT 0,
    qt_mat_prof INTEGER DEFAULT 0,
    qt_mat_eja INTEGER DEFAULT 0,
    qt_mat_esp INTEGER DEFAULT 0,
    ativo INTEGER NOT NULL DEFAULT 1,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tb_usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    nascimento TEXT,
    email TEXT
)