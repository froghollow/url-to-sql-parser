def url_to_sql( url_input ):
    import json
    import re
    from urllib.parse import urlparse

    parts = urlparse(url_input)

    page_number = 1
    page_size = 100
    parsed_url = {
        'UrlInput' : url_input,
        'BaseUrl' : f"{parts.scheme}://{parts.netloc}",
        'Endpoint' : parts.path,
        'TableName' : parts.path.split('/')[-1],
        'ColumnList' : '*',
        'FilterSpec' : '',
        'SortSpec' : '',
        'PageSize' : page_size,
        'PageNumber' : page_number,
        'Offset' : 0,
        'Format' : 'json' # or 'csv'
    }

    if parts.query > '':
        url_parms = parts.query.replace(' ','').split('&')
        for parm in url_parms:
            parm_value = parm.split('=')[1]
            if parm.startswith('fields='):
                parsed_url['ColumnList'] = parm_value
            elif parm.startswith('filter='):
                filters = parm_value
                operators = {
                    ':lt:'  : ' < ',   # Less than
                    ':lte:' : ' <= ',  # Less than or equal to
                    ':gt:'  : ' > ',   # Greater than
                    ':gte:' : ' >= ',  # Greater than or equal to
                    ':eq:'  : ' = ',   # Equal to
                    ':in:'  : ' in '   # Contained in a given set
                    }
                for op in operators:
                    #print ( op, operators[op] )

                    if op ==':in:':
                        inlist = re.findall('\(.*?\)', filters)                 # find any lists of values enclosed within '()'' ...
                        for s in inlist:
                            filters = filters.replace(s, s.replace(',','|'))    # ... temporarily replace ',' delimeters with '|'

                    filters = filters.replace(op, operators[op])
                    f = filters.split(",")

                parsed_url['FilterSpec'] = " and ".join(f).replace('|',',')

            elif parm.startswith('sort='):
                sorts = parm_value.split(',')
                for n, s in enumerate(sorts):
                    if s.startswith('-'):
                        sorts[n] = s[1:] + ' desc'
                    else:
                        sorts[n] = s + ' asc'
                parsed_url['SortSpec'] = ','.join(sorts)

            elif parm.startswith('format='):
                parsed_url['Format'] = parm_value

            elif parm.startswith('page[number]='):
                page_number = int(parm_value)
                parsed_url['PageNumber'] = page_number
                parsed_url['Offset'] = page_size * (page_number - 1)

            elif parm.startswith('page[size]='):
                page_size = int(parm_value)
                parsed_url['PageSize'] = int(parm_value)

            else:
                print( f'Ignoring unknown parm {parm}' )

    '''
      select {ColumnList}
        from {TableName}
       where {FilterSpec}
    order by {SortSpec}
       limit {PageSize} offset {PageSize * PageNumber} ;
    '''
    sql =  f"  select {parsed_url['ColumnList']} \n    from {parsed_url['TableName']} \n"
    if parsed_url['FilterSpec'] > '':
        sql += f"   where {parsed_url['FilterSpec']} \n"
    if parsed_url['SortSpec'] > '':
        sql += f"order by {parsed_url['SortSpec']} \n"
    if parsed_url['PageSize'] > 0:
        sql += f"   limit {parsed_url['PageSize']} offset {parsed_url['Offset']} \n"

    parsed_url['SQL'] = sql

    print( json.dumps(parsed_url, indent=2))
    return parsed_url
