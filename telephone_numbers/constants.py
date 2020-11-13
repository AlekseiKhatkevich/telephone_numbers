from yarl import URL

# Урлы csv файлов на сайте 'rossvyaz.gov.ru'
CSV_URLS = (
    URL('https://rossvyaz.gov.ru/data/ABC-3xx.csv'),
    URL('https://rossvyaz.gov.ru/data/ABC-4xx.csv'),
    URL('https://rossvyaz.gov.ru/data/ABC-8xx.csv'),
    URL('https://rossvyaz.gov.ru/data/DEF-9xx.csv'),
)

# TTL кеша единственной вью.
DEFAULT_CACHE_TTL = 60 * 60 * 24
