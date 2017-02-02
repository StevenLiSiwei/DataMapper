def trim(string):
    string = string.replace('\n', '')
    return string
    
def price_str_formatter(string):
    string = string.replace('$', '')
    string = string.replace('variable', '0')
    return string

def codename_formatter( index ):
    index_str = str(index)
    final_str = 'OPT{0}'.format(index_str .zfill(4))
    return final_str

    
def add_options_essential_list(item):
    dictionary = {'item_id':item['id'],'item_name':item['name'],'base_price':item['price']}
    return dictionary

def add_option(index, item):
    id = str(index)
    codename = codename_formatter(index)
    dict_opt = {'id': id, 'item_id':item['id'],'codename':codename, 'name':item['variant'], 'description':'NULL', 'price':item['price'], 'is_delete':'0'}
    return dict_opt

def opt2str(item):
    string = ''
    for key in item:
        item[key] = trim(item[key])
        string += item[key]
        string += ','
    string = string.rstrip(',')
    return string

def price_comparator(base_price, target_price):
    base_price = price_str_formatter(base_price)
    target_price = price_str_formatter(target_price)
    base_price_decimal = float(base_price)
    target_price_decimal = float(target_price)
    if(base_price_decimal == target_price_decimal):
        return '0'
    elif (base_price_decimal > target_price_decimal):
        result = base_price_decimal - target_price_decimal;
        return '-'+str(result)
    else:
        result = target_price_decimal - base_price_decimal;
        return str(result)

def find_id(name, lst):
    id = 0
    for item in lst:
        if(name == item[1]):
            id = item[0]
    return id


def data_to_item_mapper(src):
    d = {'id': src['id'], 'codename': src['id'], 'name': src['name'], 'description': 'NULL', 'barcode': src['sku'], 'category_id': src['category_id'], 'unit': '1', 'stock': src['stock'],  'price': src['price'], 'tax_rate': '0', 'cost': src['cost'], 'type': 'standard', 'is_print': '1', 'printer_id': '1', 'is_delete': '0'}
    return d

def price_checker(item, lst):
    for i in lst:
        if (i[0] == item['name']):
            if(i[1] == 1):
                return item['price']
            else:
                return '0'


input = open('input.csv', mode='r', encoding='utf-8')
lst = []
nested_id_list = []
id = 1
for line in input:
    row_array = line.split(',')
    #print (row_array)
    if not any( i[1] ==  row_array[3] for i in  nested_id_list):
        nested_id_list.append([id, row_array[3]])
        current_id = id;
        id += 1
    else:
        current_id = find_id(row_array[3], nested_id_list);
    dict = {'id': str(current_id), 'sku':row_array[1], 'name': row_array[2], 
    'category_id':row_array[3], 'stock':row_array[4], 'price':row_array[5],
    'cost':row_array[6],'alert_qty':row_array[7],'taxable':row_array[8], 'variant':row_array[9]}
    #print(dict)
    lst.append(dict);
#print(lst)
input.close()

# 生成 item options
#做重叠LIST进行重复次数记录
item_name_nested_list = []
for item in lst:
    exists = False
    for m in item_name_nested_list:
        if(m[0] == item['name'] ):
            m[1] = m[1] + 1
            exists = True
    if (not exists):
        arr = [item['name'], 1]
        item_name_nested_list.append(arr)       
#print(item_name_nested_list)

# 生成 ITEM
index = 1
item_list = []
for item in lst:
    exists = False
    for d in item_list:
        if(d['name']  == item['name'] ):
            exists = True
    if (not exists):
        price = price_checker(item, item_name_nested_list)
        item['price'] = price
        item_list.append(data_to_item_mapper(item))

##生成ITEM 文件
file = open('item.csv', 'w+')
for line in item_list:
    file.write(opt2str(line) + '\n')
file.close()
print("Item 文件已经生成")
    
    




# 同样名字的产品数大于1
final_name_list = []
for item in item_name_nested_list:
    if(item[1] > 1):
        final_name_list.append(item[0])
#print(final_name_list)

# 取每个ITEM的第一个基本价钱，ID，名字
option_essential_list = []
for item in lst:
    if any( name ==  item['name'] for name in  final_name_list):
        if not any(element['item_name'] == item['name'] for element in option_essential_list):
            option_essential_list.append(add_options_essential_list(item))
        
#print(option_essential_list)

# 生成 ITEM OPTIONS
options = []
index = 1
for item in lst:
     if any( name ==  item['name'] for name in  final_name_list):
         for ess in option_essential_list:
             if(item['name'] == ess['item_name']):
                 item['price'] = price_comparator(ess['base_price'], item['price'])
                 item['id'] = ess['item_id']
                 temp = add_option(index, item)
                 #print(temp)
                 options.append(temp)
     index += 1

#print(options)

##生成ITEM OPTION 文件
file = open('item_option.csv', 'w+')
for line in options:
    file.write(opt2str(line) + '\n')
file.close()
print("Item Option 文件已经生成")

