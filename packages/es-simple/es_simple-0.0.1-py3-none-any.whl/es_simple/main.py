
def build_aggs(buckets, metric_aggs, interval, time_field):
    if len(buckets) == 0:
        return metric_aggs
    else:
        bucket = buckets[0]
        sub_aggs = build_aggs(buckets[1:], metric_aggs, interval, time_field)
        agg_config = {}
        if bucket['agg_type'] == 'date_histogram':
            agg_config = {
                bucket['agg_type']: {
                    "field": time_field,
                    "interval": interval,
                    "time_zone": "Asia/Shanghai",
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
        else:
            raise Exception("unsupport agg_type")
        return {
            bucket['name']: agg_config,
            "aggs": sub_aggs
        }

def build_query(metrics, buckets, query_string, start_ms, end_ms, interval, time_field):
    metric_aggs = {}
    for metric in metrics:
        metric_aggs[metric['name']] = {
            metric['agg_func']: {
                "field": metric['field']
            }
        }
    aggs = build_aggs(buckets, metric_aggs, interval, time_field)
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