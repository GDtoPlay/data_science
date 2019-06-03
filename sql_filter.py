import copy


def tree_to_plain(tree, ret_list):
    for data in tree:
        if type(data) is list:
            tree_to_plain(data, ret_list)

        else:
            ret_list.append(data)



def parse(origin_sql):
    sql = []
    flag = 0
    subquery=[]
    start = 0
    end = -1
    check=0
    
    for i in range(0,len(origin_sql)):
        if origin_sql[i] == ",":
            continue
        elif origin_sql[i] is "(":
            start = i
            end = subparse(origin_sql,start)
            if end != -1:
                subquery = origin_sql[int(start)+1:end]
                sql.append(subquery)

            else:
                sql.append(origin_sql[i])

        elif end < i:
            sql.append(origin_sql[i])

    return sql



def subparse(sql,start):
    count = 1
    for i in range(start+1,len(sql)):
        
        l = sql[i]
        if l is "(":
            count += 1
        if l is ")":
            count -= 1
        if count is 0:
            return i
        
    return -1




def splitcheck(origin_sql):
    sql = []
    for chunk in origin_sql:
        if ',' in chunk or '(' in chunk or ')' in chunk:
            start = 0
            end = 0
            for idx, char in enumerate(chunk):
                if char == ',':
                    end = idx - 1
                    if end >= 0:
                        if chunk[start:end + 1] != '':
                            sql.append(chunk[start:end + 1])
                    sql.append(',')
                    start = idx + 1

                elif char == '(':
                    end = idx - 1
                    if end >= 0:
                        if chunk[start:end + 1] != '':
                            sql.append(chunk[start:end + 1])
                    sql.append('(')
                    start = idx + 1

                elif char == ')':
                    end = idx - 1
                    if end >= 0:
                        if chunk[start:end + 1] != '':
                            sql.append(chunk[start:end + 1])
                    sql.append(')')
                    start = idx + 1

            if start != len(chunk):
                sql.append(chunk[start:])
                    
        else:
            sql.append(chunk)                

    return sql



def find_chunk_end(sql, start):
    sql_start_keywords = ['select', 'update', 'delete', 'insert']
    chunk_end = start
    chunk_end_found = False

    while not chunk_end_found and chunk_end < len(sql):
        if sql[chunk_end] in sql_start_keywords:
            chunk_end_found = True

        else:
            chunk_end = chunk_end + 1

    chunk_end = chunk_end - 1

    return chunk_end


            

def sql_tree_maker(origin_sql):
    sql = copy.deepcopy(origin_sql)
    
    sql_start_keywords = ['select', 'update', 'delete', 'insert']
    
    if 'union' in sql:                          #union tree
        union_index = sql.index('union')

        if union_index < len(sql) - 1:
            if sql[union_index + 1] == 'all':
                
                if  union_index + 1 < len(sql) - 1:
                    return ['union', 'all', sql_tree_maker(sql[:union_index]), sql_tree_maker(sql[union_index + 2:])]
                else:
                    return ['union', 'all', sql_tree_maker(sql[:union_index])]

            else:
                return ['union', sql_tree_maker(sql[:union_index]), sql_tree_maker(sql[union_index + 1:])]

        else:
            return ['union', sql_tree_maker(sql[:union_index])]

    for idx, word in enumerate(sql):        #sql query chunk finding
            
        if word == 'insert':            #if start word is insert
            if idx < len(sql) - 1 and sql[idx + 1] == 'into':
                chunk_end = find_chunk_end(sql, idx + 2)

                if chunk_end < len(sql) - 1:
                    return sql[:idx] + ['insert', 'into', sql_tree_maker(sql[idx+2:chunk_end + 1])] + sql_tree_maker(sql[chunk_end + 1:])
                else:
                    return sql[:idx] + ['insert', 'into', sql_tree_maker(sql[idx+2:chunk_end + 1])]
                    
            else:
                continue
            


        elif word == 'update':              # update ~~~ set ~~~ where ~~
            chunk_end = find_chunk_end(sql, idx + 1)
            sql_chunk = sql[idx: chunk_end + 1]

            if 'set' in sql_chunk:
                set_pos = sql_chunk.index('set')

                if set_pos == 1 or set_pos == len(sql_chunk) - 1:            # update set ~~~ OR update ~~~~ set: not ideal update query
                    continue

                else:
                    where_pos = -1

                    if 'where' in sql_chunk:                # where is 'where'?
                        where_pos = sql_chunk.index('where')

                    if where_pos is not -1:
                        if where_pos == set_pos + 1 or where_pos == len(sql_chunk) - 1:     # update ~~~ set where (~~~) OR update ~~~ set ~~~ where
                            continue

                        else:                                                           # update ~~~ set ~~~ where ~~~~
                            mid_chunk = ['update', 'set', 'where']
                            mid_chunk.append(sql_tree_maker(sql_chunk[1:set_pos]))
                            mid_chunk.append(sql_tree_maker(sql_chunk[set_pos + 1:where_pos]))
                            mid_chunk.append(sql_tree_maker(sql_chunk[where_pos + 1:]))

                            if chunk_end < len(sql) - 1:
                                return sql[:idx] + mid_chunk + sql_tree_maker(sql[chunk_end + 1:])
                            else:
                                return sql[:idx] + mid_chunk

                    else:                                           #there is no 'where
                        mid_chunk = ['update', 'set']
                        mid_chunk.append(sql_tree_maker(sql_chunk[1:set_pos]))
                        mid_chunk.append(sql_tree_maker(sql_chunk[set_pos + 1:]))

                        if chunk_end < len(sql) - 1:
                            return sql[:idx] + mid_chunk + sql_tree_maker(sql[chunk_end + 1:])
                        else:
                            return sql[:idx] + mid_chunk

            else:                           #not update query
                continue





        elif word == 'delete':              #delete from ~~~ where ~~~
            if idx < len(sql) - 1 and sql[idx + 1] == 'from':
                chunk_end = find_chunk_end(sql, idx + 2)
                sql_chunk = sql[idx: chunk_end + 1]

                where_pos = -1
                if 'where' in sql_chunk:
                    where_pos = sql_chunk.index('where')

                mid_chunk = []

                if where_pos is not -1:
                    if where_pos < len(sql_chunk) - 1:
                        if sql_chunk[2:where_pos] is not []:                    # delete from ~~~ where ~~~
                            mid_chunk = ['delete', 'from', 'where']
                            mid_chunk.append(sql_tree_maker(sql_chunk[2:where_pos]))
                            mid_chunk.append(sql_tree_maker(sql_chunk[where_pos + 1:]))

                        else:                                                   # delete from where ~~~~~
                            mid_chunk = ['delete', 'from', 'where']
                            mid_chunk.append(sql_tree_maker(sql_chunk[where_pos + 1:]))

                    else:
                        mid_chunk = ['delete', 'from']
                        if sql_chunk[2:where_pos] is not []:                    # delete from ~~~~ where
                            mid_chunk.append(sql_tree_maker(sql_chunk[2:where_pos]))

                        mid_chunk.append('where')

                else:
                    if 2 < len(sql_chunk):                                      # delete from ~~~
                         mid_chunk = ['delete', 'from']
                         mid_chunk.append(sql_tree_maker(sql_chunk[2:]))

                    else:                                                       # delete from
                        mid_chunk = ['delete', 'from']



                if chunk_end < len(sql) - 1:
                    return sql[:idx] + mid_chunk + sql_tree_maker(sql[chunk_end + 1:])
                else:
                    return sql[:idx] + mid_chunk
                        

            else:                                                               #not delete query 
                continue




        elif word == 'select' or word == 'from' or word == 'where':     #select ~~~ from ~~~ where ~~~
            chunk_end = find_chunk_end(sql, idx + 1)

            sql_chunk = sql[idx: chunk_end + 1]

            pos_in_order_list = []

            if 'select' in sql_chunk:                                   #collecting critical keyword loc into 'pos_in_order_list'
                temp_pos = sql_chunk.index('select')
                pos_in_order_list.append(temp_pos)
             
            if 'from' in sql_chunk:
                temp_pos = sql_chunk.index('from')
                pos_in_order_list.append(temp_pos)

            if 'where' in sql_chunk:
                temp_pos = sql_chunk.index('where')
                pos_in_order_list.append(temp_pos)

            if 'group' in sql_chunk:
                temp_pos = sql_chunk.index('group')
                if temp_pos < len(sql_chunk) - 1:
                    if sql_chunk[temp_loc + 1] == 'by':
                        pos_in_order_list.append(temp_pos)

            if 'having' in sql_chunk:
                temp_pos = sql_chunk.index('having')
                pos_in_order_list.append(temp_pos)

            if 'order' in sql_chunk:
                temp_pos = sql_chunk.index('order')
                if temp_pos < len(sql_chunk) - 1:
                    if sql_chunk[temp_loc + 1] == 'by':
                        pos_in_order_list.append(temp_pos)

            make_sence = True
            for i in range(0, len(pos_in_order_list) - 1):        # is this seems_sql_block make sence?
                if pos_in_order_list[i] < pos_in_order_list[i+1]:
                    make_sence = make_sence and True
                else:
                    make_sence = False

            if not make_sence:                                  # this chunk is not sql
                mid_chunk = []
                for sub_word in sql_chunk:
                    if type(sub_word) is list:
                        mid_chunk.append(sql_tree_maker(parse(sub_word)))

                    else:
                        mid_chunk.append(sub_word)
                        
                if chunk_end < len(sql) - 1:
                    return sql[:idx] + mid_chunk + sql_tree_maker(sql[chunk_end + 1:])
                else:
                    return sql[:idx] + mid_chunk

            else:                                           # can be sql
                mid_chunk = []
                func_parameters = []
                last_pos = -1
                for sub_idx, pos in enumerate(pos_in_order_list):
                    if sql_chunk[pos] == 'order' or sql_chunk[pos] == 'group':      # in case of order by OR group by
                        if sql_chunk[last_pos + 1: pos] != []:
                            func_parameters.append(sql_chunk[last_pos + 1: pos])

                        mid_chunk.append(sql_chunk[pos])
                        mid_chunk.append(sql_chunk[pos+1])
                        last_pos = pos + 1

                        if last_pos < len(sql_chunk) -1 and sub_idx == len(pos_in_order_list) - 1:
                            func_parameters.append(sql_chunk[last_pos + 1: ])
                            

                    else:
                        if sql_chunk[last_pos + 1: pos] != []:
                            func_parameters.append(sql_chunk[last_pos + 1: pos])

                        mid_chunk.append(sql_chunk[pos])
                        last_pos = pos

                        if last_pos < len(sql_chunk) -1 and sub_idx == len(pos_in_order_list) - 1:
                            func_parameters.append(sql_chunk[last_pos + 1: ])

                for parameters in func_parameters:
                    mid_chunk.append(sql_tree_maker(parameters))

                if chunk_end < len(sql) - 1:
                    return sql[:idx] + mid_chunk + sql_tree_maker(sql[chunk_end + 1:])
                else:
                    return sql[:idx] + mid_chunk



        elif type(word) is list:
            if idx < len(sql) - 1:
                return sql[:idx] + [sql_tree_maker(parse(word))] + sql_tree_maker(sql[idx + 1:])
            else:
                return sql[:idx] + [sql_tree_maker(parse(word))]

    return sql


