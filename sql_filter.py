import copy


def tree_to_plain(tree, ret_list):  #만들어진 AST를 하나의 리스트로 넣어주는 함수
    for data in tree:
        if type(data) is list:
            tree_to_plain(data, ret_list)

        else:
            ret_list.append(data)



def parse(origin_sql):  # 괄호 처리. () 내부는 하나의 리스트로 묶여짐, 리스트는 AST 생성 시 나중에 또 괄호 처리를 해주어야 함 
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
            if end != -1:                                #괄호 처리가 필요
                subquery = origin_sql[int(start)+1:end]
                sql.append(subquery)

            else:
                sql.append(origin_sql[i])

        elif end < i:                                   #괄호 처리가 이루어지면 처리한 괄호의 끝 부분 까지는 괄호 처리 작업이 진행되면 안됨
            sql.append(origin_sql[i])

    return sql



def subparse(sql,start):    # 괄호 처리에 쓰이는 기능. 어디서 어디 까지를 괄호로 묶을 지 판단
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




def splitcheck(origin_sql):    # ' ' 단위로 잘린 문자열의 str 청크 리스트에 대해서 각 청크에서 '(', ')', '+', '&', '=' 을 주위의 문자들과 분리시키는 작업  예) ['(select', 'from'] -> ['(', 'select', 'from']
    sql = []
    for chunk in origin_sql:
        if ',' in chunk or '(' in chunk or ')' or '+' or '&' or '='in chunk:
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

                elif char == '=':
                    end = idx - 1
                    if end >= 0:
                        if chunk[start:end + 1] != '':
                            sql.append(chunk[start:end + 1])
                    sql.append('=')
                    start = idx + 1

                elif char == '&':
                    end = idx - 1
                    if end >= 0:
                        if chunk[start:end + 1] != '':
                            sql.append(chunk[start:end + 1])
                    sql.append('&')
                    start = idx + 1

                elif char == '+':
                    end = idx - 1
                    if end >= 0:
                        if chunk[start:end + 1] != '':
                            sql.append(chunk[start:end + 1])
                    sql.append('+')
                    start = idx + 1

            if start != len(chunk):
                sql.append(chunk[start:])
                    
        else:
            sql.append(chunk)                

    return sql



def find_chunk_end(sql, start):  # sql injecton에서 독립적인 구문들이 여러개 있는 경우 구문의 끝을 대략적으로 파악하는 함수. 구문의 끝은 새로운 구문의 시작과 비슷하다고 가정
    sql_start_keywords = ['select', 'update', 'delete', 'insert']  # 새로운 구문이 시작될 때 나오는 키워드
    chunk_end = start
    chunk_end_found = False

    while not chunk_end_found and chunk_end < len(sql):
        if sql[chunk_end] in sql_start_keywords:
            chunk_end_found = True

        else:
            chunk_end = chunk_end + 1

    chunk_end = chunk_end - 1

    return chunk_end


            

def sql_tree_maker(origin_sql):  # sql AST를 만드는 함수, 엄격하게 트리 구조를 만드는 것이 아니라, sql이 아닌 구문 또한 정상적으로 결과값이 나와야 함
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
                    if sql_chunk[temp_pos + 1] == 'by':
                        pos_in_order_list.append(temp_pos)

            if 'having' in sql_chunk:
                temp_pos = sql_chunk.index('having')
                pos_in_order_list.append(temp_pos)

            if 'order' in sql_chunk:
                temp_pos = sql_chunk.index('order')
                if temp_pos < len(sql_chunk) - 1:
                    if sql_chunk[temp_pos + 1] == 'by':
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



        elif type(word) is list:            #리스트는 이전에 괄호 처리된 내용들 임으로 내부 내용에 대한 AST를 만들어 붙이는 방식으로 구현
            if idx < len(sql) - 1:
                return sql[:idx] + [sql_tree_maker(parse(word))] + sql_tree_maker(sql[idx + 1:])  #내부 내용에 대해 괄호처리가 되어야 함
            else:
                return sql[:idx] + [sql_tree_maker(parse(word))]

    return sql


