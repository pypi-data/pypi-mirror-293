
def build_aggs(buckets, metric_aggs, interval, time_field, time_zone):
    if len(buckets) == 0:
        return metric_aggs
    else:
        bucket = buckets[0]
        sub_aggs = build_aggs(buckets[1:], metric_aggs, interval, time_field, time_zone)
        agg_config = {}
        if bucket['agg_type'] == 'date_histogram':
            agg_config = {
                bucket['agg_type']: {
                    "field": time_field,
                    "interval": interval,
                    "time_zone": time_zone,
                }
            }

        elif bucket['agg_type'] == 'terms':
            agg_config = {
                bucket['agg_type']: {
                    "field": bucket['field'],
                    "size": bucket['size'],
                    "order": bucket['order'],
                }
            }
        elif bucket['agg_type'] == "filters":

            filters_config = {}
            for filter in bucket['filters'].filters:
                filters_config[filter['name']] = {
                    "query_string": {
                      "query": filter['query_string'],
                      "analyze_wildcard": True,
                      "default_field": "*"
                    }
                }
            agg_config = {
                bucket['agg_type']: {
                    "filters": filters_config
                }
            }
        else:
            raise Exception("unsupport agg_type")
        agg_config['aggs'] = sub_aggs
        return {
            bucket['name']: agg_config,
        }

def build_query(metrics, buckets, query_string, start_ms, end_ms, interval, time_field, time_zone):
    metric_aggs = {}
    for metric in metrics:
        metric_aggs[metric['name']] = {
            metric['agg_func']: {
                "field": metric['field']
            }
        }
    aggs = build_aggs(buckets, metric_aggs, interval, time_field, time_zone)
    es_query = {
        "aggs": aggs,
        "size": 0,
        "docvalue_fields": [
            {
                "field": time_field,
                "format": "date_time"
            }
        ],
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": query_string,
                            "analyze_wildcard": True,
                            "default_field": "*"
                        }
                    },
                    {
                        "range": {
                            time_field: {
                                "gte": start_ms,
                                "lte": end_ms,
                                "format": "epoch_millis"
                            }
                        }
                    }
                ],
                "filter": [],
                "should": [],
                "must_not": []
            }
        }
    }
    return es_query

class FiltersBucket:
    def __init__(self):
        self.filters = []

    def add_filter(self, name, query_string):
        self.filters.append({"name": name, "query_string":query_string})

class QueryBuilder:

    def __init__(self, query_string, start_ms, end_ms, interval="5m", time_field="log_timestamp", time_zone="Asia/Shanghai"):
        self.query_string = query_string
        self.start_ms = start_ms
        self.end_ms = end_ms
        self.interval = interval
        self.time_field = time_field
        self.time_zone = time_zone
        self.buckets = []
        self.metrics = []

    def add_date_histogram_bucket(self, name):
        self.buckets.append({"name": name, "agg_type": "date_histogram"})

    def add_terms_bucket(self, name, field, size, order):
        self.buckets.append({"name": name, "agg_type": "terms", "field": field, "size": size, "order": order})

    def add_filters_bucket(self, name, filters:FiltersBucket):
        self.buckets.append({"agg_type": "filters", "name": name, "filters": filters})


    def add_metric(self, name, agg_func, field):
        self.metrics.append({"name": name, "agg_func": agg_func, "field": field})

    def set_time(self, start_ms, end_ms):
        self.start_ms = start_ms
        self.end_ms = end_ms

    def build(self):
        return build_query(self.metrics, self.buckets, self.query_string, self.start_ms, self.end_ms, self.interval, self.time_field, self.time_zone)

