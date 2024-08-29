import json
from typing import Any, Dict, List
from datetime import datetime

from .. import network
from ..utils.time import standard_time_zone
from ..utils.extras import list_monitors_images
from ._base import Base
from ..pages import ExchangeMonitor as ExchangeMonitorPage

def _convert_specific_format(text: str, character: str = '_') -> str:
    acentos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'}
    for acento, sin_acento in acentos.items():
        text = text.lower().replace(acento, sin_acento).replace(' ', character)
    return text

class ExchangeMonitor(Base):
    PAGE = ExchangeMonitorPage

    @classmethod
    def _load(cls, **kwargs) -> List[Dict[str, Any]]:
        url = f'{cls.PAGE.provider}api/app/rates'
        response = network.get(url, params={'type': 'VE'})
        results = json.loads(response).get('data')
            
        data = []
        for result in results:
            name  = result['name']
            key = _convert_specific_format(name)
            price = round(1 / float(result['rate']), 2)

            last_update = datetime.now(standard_time_zone)
            image = next((image.image for image in list_monitors_images if image.provider == 'exchangemonitor' and image.title == _convert_specific_format(name)), None)

            data.append({
                'key': key,
                'title': name,
                'price': price,
                'last_update': last_update,
                'image': image
            })

        return data