# es_simple

A package for query ElasticSearch and parse response easy.

## Usage

```python
import es_simple
import time
qb = es_simple.QueryBuilder("hostname:*live*", # query string
                            int(time.time() * 1000 - 3600 * 1000), "start timestamp in ms"
                            int(time.time() * 1000), # end timestamp in ms
                            "5m", # interval
                            "log_timestamp", # time field
                            "Asia/Shanghai")  # time zone
  

qb.add_metric("avg_tcp_re_rate", "avg", "tcp_re_rate")
qb.add_metric("avg_cpu", "avg", "cpu_idle")
qb.add_date_histogram_bucket("ts")
qb.add_terms_bucket("nodename", "nodename", "20", {"tcp_re_rerate": "desc"})

es_query = qb.build()

print(es_query)
```

