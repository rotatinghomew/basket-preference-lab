"""已有资料的描述性概览。"""
def summarize(data):
    rows = data["rows"]
    return {'visits': len(rows), 'households': len({row['household'] for row in rows}), 'products': data['products'], 'opportunity_versions': len(data['opportunities'])}
