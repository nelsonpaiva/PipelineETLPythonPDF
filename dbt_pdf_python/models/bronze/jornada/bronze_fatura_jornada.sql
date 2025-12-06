SELECT TO_DATE(REPLACE(vencto, '/', ''), 'DDMMYYYY')
FROM {{source("investimentos","fatura_jornada")}}

