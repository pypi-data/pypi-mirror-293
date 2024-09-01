from plexflow.utils.api.rest.antibot_restful import AntibotRestful
from plexflow.utils.api.rest.restful import Restful
from plexflow.core.torrents.providers.therarbg.utils import TheRarbgSearchResult
from plexflow.utils.torrent.extract.therarbg import extract_torrent_results
from typing import List

class TheRarbg(Restful):
    def __init__(self, base_url: str = 'https://therarbg.com'):
        super().__init__(base_url=base_url)
    
    def search(self, query: str) -> List[TheRarbgSearchResult]:
        response = self.get(f'/get-posts/keywords:{query}/')
        
        response.raise_for_status
        
        data = extract_torrent_results(html=response.text)
        return list(map(lambda t: TheRarbgSearchResult(**t), data))
