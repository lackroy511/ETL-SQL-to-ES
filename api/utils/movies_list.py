
def form_query(request):
    
    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=50, type=int)
    sort_field = request.args.get('sort_by', default='id', type=str)
    sort_order = request.args.get('sort_order', default='asc', type=str)
    search = request.args.get('search', default='', type=str)

    query = {
        'from': ((page if page > 0 else 1) - 1) * limit,
        'size': limit,
        'sort':  [
            {
                sort_field: {
                    'order': sort_order,
                },
            },
        ],
    }
    if search:
        query['query'] = {
            'multi_match': {
                'query': search,
                'fuzziness': 'auto',
                'fields': [
                    'title^1',
                    'description^2',
                    'genre^3',
                    'actors_names^4',
                    'writers_names^5',
                ],
            },
        }
    
    return query
