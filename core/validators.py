import requests
from django.core.exceptions import ValidationError


class INNCheckValidator:
    _base_url = 'https://egrul.nalog.ru'

    def _get_token(self, value):
        response = requests.post(self._base_url, json={
            "query": value
        })
        if not response.status_code == 200:
            raise ValidationError('Сервис недоступен')
        return response.json().get('t')

    def __call__(self, value):
        token = self._get_token(value)
        response = requests.get(f"{self._base_url}/search-result/{token}")
        if not response.status_code == 200:
            raise ValidationError('Сервис недоступен')
        orgs = response.json().get('rows')
        if not orgs:
            raise ValidationError("ИНН не найдень")
        if len(orgs) > 1:
            raise ValidationError(f"Найден {len(orgs)} организации с указинной инн")
        return orgs[0]
