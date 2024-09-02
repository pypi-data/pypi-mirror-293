import re
import json


def find_requests_and_responses(logs, search_pattern):
    """
    Функция для поиска всех запросов и их ответов в логах по заданному регулярному выражению.

    :param logs: Список логов, полученных из браузера
    :param search_pattern: Регулярное выражение для поиска в логах
    :return: Список словарей с данными запросов и ответов
    """
    results = []
    request_id_map = {}  # Для хранения найденных requestId и их запросов

    # Компиляция регулярного выражения
    pattern = re.compile(search_pattern)

    # Поиск запросов
    for log in logs:
        log_message = json.loads(log['message'])
        message = log_message['message']

        if message['method'] == 'Network.requestWillBeSent':
            request = message['params']['request']
            url = request['url']
            if pattern.search(url):
                request_id = message['params']['requestId']
                request_id_map[request_id] = request

    # Поиск ответов на запросы
    for log in logs:
        log_message = json.loads(log['message'])
        message = log_message['message']

        if message['method'] == 'Network.responseReceived':
            request_id = message['params']['requestId']
            if request_id in request_id_map:
                response = message['params']['response']
                request = request_id_map[request_id]
                results.append({
                    'request': request,
                    'response': response
                })

    return results
