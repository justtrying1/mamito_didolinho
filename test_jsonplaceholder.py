"""
О тестируемом сервисе:
API сайта https://jsonplaceholder.typicode.com содержит 6 эндпоинтов 
/posts
/comments
/albums
/photos
/todos
/users

эндпоинты связаны между друг другом:

/posts/1/comments
/albums/1/photos
/users/1/albums
/users/1/todos
/users/1/posts

Запросы доступные по эндпоинту на примере posts:

GET	/posts
GET	/posts/1
GET	/posts/1/comments
GET	/comments?postId=1
POST	/posts
PUT	/posts/1
PATCH	/posts/1
DELETE	/posts/1

Данный проект реализует тестирование заявленных функций, маршрутов, а также некоторые крайние случаи  

"""
import pytest
import json
import requests

# Cписок всех эндпоинтов для параметризации 
endpoints = ['posts', 'comments', 'albums', 'photos', 'todos', 'users']
# Аналогичный случай с запросами через url/endpoint?Id=1
endpoints_alt = {"comments" : "postId", "albums":"userId", "todos":"userId", "posts":"userId", 'photos': 'albumId'} 

prefix = ['http', 'https'] # для параметризации http/https запрос

# Получение полей которые должны быть в JSON каждого эндпоинта 
def initialize_endpoint_fields() -> dict[str, str]: # endpoint_fields : {endpoint: [field_1, field_2]}
    endpoint_fields = {}
    for ep in endpoints:
        fields = []
        url = f"https://jsonplaceholder.typicode.com/{ep}/1".format(ep)  
        response = requests.get(url)
        for field in response.json():
            fields.append(field)
        endpoint_fields[ep] = fields
    return endpoint_fields
    
# endpoint_fields нужна для валидации json ответа с помощью итерации через данную переменную
endpoint_fields = initialize_endpoint_fields() 



"""
#######
GET
#######
"""

# GET по эндпоинтам с обращением по индексу к первому элементу 
@pytest.mark.parametrize("prefix", prefix)
@pytest.mark.parametrize("endpoint", endpoints)
def test_get_index(endpoint, prefix):
    
    url = f"{prefix}://jsonplaceholder.typicode.com/{endpoint}/1".format(prefix, endpoint)  
    
    response = requests.get(url)
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'

    # Проверка структуры json'а из ответа
    data = response.json()  
    assert isinstance(data, dict)
     # Проверка наличия полей из endpoint_fields соответствующих эндпоинту
    for field in endpoint_fields[endpoint]:
        assert field in data

# GET по несуществующему индексу
@pytest.mark.parametrize("prefix", prefix)
@pytest.mark.parametrize("endpoint", endpoints)
def test_get_index_marginal(endpoint, prefix):
    json_endpoint = requests.get(f"https://jsonplaceholder.typicode.com/{endpoint}".format(endpoint), timeout=3).json()
    endpoint_length = len(json_endpoint)  
    url = f"{prefix}://jsonplaceholder.typicode.com/{endpoint}/{endpoint_length+10}".format(prefix, endpoint)  
   # import pdb; pdb.set_trace()
    response = requests.get(url)
    
    # Проверка статуса 
    assert  response.status_code == 404  # Обращение по несуществующему индексу

@pytest.mark.parametrize("endpoint", list(endpoints_alt.keys())) # проходим по ключам endpoints_alt 
def test_get_index_alt_marginal(endpoint): 
    json_endpoint = requests.get(f"https://jsonplaceholder.typicode.com/{endpoint}".format(endpoint), timeout=3).json()
    endpoint_length = len(json_endpoint) 
    # Получаем кодовое слово для айдишника по ключу
    Id = endpoints_alt[endpoint] 
    # Формируем запрос на основе полученных значений из endpoints_alt
    url = f"https://jsonplaceholder.typicode.com/{endpoint}?{Id}={endpoint_length + 10}".format(endpoint, Id, endpoint_length) 
    
    response = requests.get(url)
    
    # Проверка статуса 
    assert response.status_code == 404 



# GET по эндпоинтам без обращения к отдельному элементу 
@pytest.mark.parametrize("endpoint", endpoints)
def test_get(endpoint):


    url = f"https://jsonplaceholder.typicode.com/{endpoint}".format(endpoint)  # Изменился адрес
    try:
        
        response = requests.get(url, timeout=3)
    except:
        pass
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'
    
    # Проверка структуры json'а из ответа
    data = response.json()  
    assert isinstance(data, list)
    # Проверка наличия полей из endpoint_fields соответствующих эндпоинту 
    for field in endpoint_fields[endpoint]: 
        assert field in data[0]

@pytest.mark.parametrize("endpoint", list(endpoints_alt.keys())) # проходим по ключам endpoints_alt 
def test_get_index_alt(endpoint): 
    # Получаем кодовое слово для айдишника по ключу
    Id = endpoints_alt[endpoint] 
    # Формируем запрос на основе полученных значений из endpoints_alt
    url = f"https://jsonplaceholder.typicode.com/{endpoint}?{Id}=1".format(endpoint, Id) 
    
    response = requests.get(url)
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'

    # Проверка структуры json'а из ответа
    data = response.json()  
    assert isinstance(data, list)
    for field in endpoint_fields[endpoint]: # Проверка наличия полей из endpoint_fields соответствующих эндпоинту
        assert field in data[1]


"""
########
DELETE 
########
"""

@pytest.mark.parametrize("endpoint", endpoints) # по endpoints
def test_delete_index(endpoint):
    
    url = f"https://jsonplaceholder.typicode.com/{endpoint}/1".format(endpoint)  
    
    response = requests.delete(url)
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'

'''
@pytest.mark.parametrize("endpoint", list(endpoints_alt.keys())) # проходим по ключам endpoints_alt 
def test_delete_index_alt(endpoint): 
    # Получаем кодовое слово для айдишника по ключу
    Id = endpoints_alt[endpoint] 
    # Формируем запрос на основе полученных значений из endpoints_alt
    url = f"https://jsonplaceholder.typicode.com/{endpoint}?{Id}=1".format(endpoint, Id) 
    import pdb; pdb.set_trace()
    response = requests.delete(url)
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'
'''

"""
######
PUT
######
"""

@pytest.mark.parametrize("endpoint", endpoints)
def test_put_index(endpoint):


    url = f"https://jsonplaceholder.typicode.com/{endpoint}/1".format(endpoint) 
    try:
        
        response = requests.put(url, json= {field: "foo bar" for field in endpoint_fields[endpoint]}, timeout=3)
    
    except:
        pass
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'
    
    # Проверка структуры json'а из ответа
    data = response.json()  
    import pdb; pdb.set_trace()
    assert isinstance(data, list)
    # Проверка наличия полей из endpoint_fields соответствующих эндпоинту 
    for field in endpoint_fields[endpoint]: 
        assert field in data[0]

@pytest.mark.parametrize("endpoint", list(endpoints_alt.keys())) # проходим по ключам endpoints_alt 
def test_put_index_alt(endpoint): 
    # Получаем кодовое слово для айдишника по ключу
    Id = endpoints_alt[endpoint] 
    # Формируем запрос на основе полученных значений из endpoints_alt
    url = f"https://jsonplaceholder.typicode.com/{endpoint}?{Id}=1".format(endpoint, Id) 
    
    response = requests.get(url)
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'

    # Проверка структуры json'а из ответа
    data = response.json()  
    assert isinstance(data, list)
    for field in endpoint_fields[endpoint]: # Проверка наличия полей из endpoint_fields соответствующих эндпоинту
        assert field in data[1]

"""
########
POST
########
"""

def test_post(endpoint):
    url = f"https://jsonplaceholder.typicode.com/{endpoint}".format(endpoint) 
    try:     
        response = requests.post(url, json= {field : "foo bar" for field in endpoint_fields[endpoint]}, timeout=3)
    except:
        pass
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'
    
    # Проверка структуры json'а из ответа
    data = response.json()  
    
    assert isinstance(data, list)
    # Проверка наличия полей из endpoint_fields соответствующих эндпоинту 
    for field in endpoint_fields[endpoint]: 
        assert field in data[0]

@pytest.mark.parametrize("endpoint", endpoints) 
def test_post_negative(endpoint): # Тест на отправку большого пейлоада

    with pytest.raises(Exception):
        url = f"https://jsonplaceholder.typicode.com/{endpoint}".format(endpoint) 
    
        payload = {f: "foo bar" for f in range(0,100000)}
        response = requests.post(url, json= payload, timeout=10)

"""
########
PATCH
########
"""

def test_patch(endpoint):
    url = f"https://jsonplaceholder.typicode.com/{endpoint}/1".format(endpoint) 
    try:     
        response = requests.patch(url, json= {field : "foo bar" for field in endpoint_fields[endpoint]}, timeout=3)
    except:
        pass
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'
    
    # Проверка структуры json'а из ответа
    data = response.json()  
    
    assert isinstance(data, list)
    # Проверка наличия полей из endpoint_fields соответствующих эндпоинту 
    for field in endpoint_fields[endpoint]: 
        assert field in data[0]

def test_patch_non_existent_fields(endpoint): # тест с патчем несуществующих полей
    url = f"https://jsonplaceholder.typicode.com/{endpoint}/1".format(endpoint) 
    try:     
        response = requests.patch(url, json= {field : "foo bar" for field in endpoint_fields[endpoint]}, timeout=3)
    except:
        pass
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'
    
    # Проверка структуры json'а из ответа
    data = response.json()  
    
    assert isinstance(data, list)
    # Проверка наличия полей из endpoint_fields соответствующих эндпоинту 
    for field in endpoint_fields[endpoint]: 
        assert field in data[0]

def test_patch_existing_field(endpoint): # тест с патчем существующих полей
    url = f"https://jsonplaceholder.typicode.com/{endpoint}/1".format(endpoint) 
    try:     
        response = requests.patch(url, json= {"body" : "foo bar"}, timeout=3)
    except:
        pass
    
    # Проверка статуса 
    assert response.status_code == 200 

    # Проверка формата ответа
    assert response.headers["Content-Type"] == 'application/json; charset=utf-8'
    
    # Проверка структуры json'а из ответа
    data = response.json()  
    
    assert isinstance(data, list)
    # Проверка наличия полей из endpoint_fields соответствующих эндпоинту 
    for field in endpoint_fields[endpoint]: 
        assert field in data[0]
    # Проверка результатов изменения
    assert data['body'] == 'foo bar' 
import pdb; pdb.set_trace()
test_patch_existing_field('posts')