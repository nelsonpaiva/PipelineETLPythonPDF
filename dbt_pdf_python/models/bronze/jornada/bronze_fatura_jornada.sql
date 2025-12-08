/*
SELECT TO_DATE(REPLACE(vencto, '/', ''), 'DDMMYYYY')
FROM {{source("investimentos","fatura_jornada")}}
*/

WITH formatted AS (
    SELECT
        "n_nota" as n_nota, --correções de nomenclarutras
        "cv",
        "merc",
        "tipo",
        TO_DATE("vencto", 'DDMMYYYY') AS vecto, --correção de date_time
        CAST("qted" AS INT) AS qted, -- fazendo cast(tipo de dado) de inteiro
        "mercadoria",
        CAST(REPLACE("cotacao", ',', '.') AS DECIMAL(10, 2)) AS cotacao,--antes de fazer um cast(tipo de dado) para decimal, estou fazendo um Replace. Tirando o que é virgula e colocando ponto.
        TO_DATE("data_de_pregao", 'DDMMYYYY') AS data_de_pregao,
        CAST(REPLACE("txop", ',', '.') AS DECIMAL(10, 2)) AS txop
    FROM
        {{ source('investimentos', 'fatura_jornada') }}
)

SELECT * 
FROM formatted