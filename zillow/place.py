from abc import abstractmethod
from zillow import ZillowError

class SourceData(classmethod):

    @abstractmethod
    def set_data(self, source_data):
        """
        @type source_data: dict
        """
        raise NotImplementedError()

    @abstractmethod
    def debug(self):
        for i in self.__dict__.keys():
            print "%s: %s" % (i, self.__dict__[i])

    @abstractmethod
    def get_dict(self):
        res = {}
        for i in self.__dict__.keys():
            res[i] = self.__dict__[i]
        return res

    @abstractmethod
    def set_values_from_dict(self, data_dict):
        """
        @type data_dict: dict
        """
        for i in self.__dict__.keys():
            if i in data_dict.keys():
                self.__dict__[i] = data_dict[i]


class Links(SourceData):
    def __init__(self, **kwargs):
        self.home_details = None
        self.graphs_and_data = None
        self.map_this_home = None
        self.comparables = None

    def set_data(self, source_data):
        """
        :source_data: Data from data.get('SearchResults:searchresults', None)['response']['results']['result']['links']
        :return:
        """
        self.home_details = source_data['homedetails']
        try:
            self.graphs_and_data = source_data['graphsanddata']
        except:
            self.graphs_and_data = None
        self.map_this_home = source_data['mapthishome']
        self.comparables = source_data['comparables']

class FullAddress(SourceData):
    def __init__(self, **kwargs):
        self.street = None
        self.zipcode = None
        self.city = None
        self.state = None
        self.latitude = None
        self.longitude = None

    def set_data(self, source_data):
        """
        :source_data: Data from data.get('SearchResults:searchresults', None)['response']['results']['result']['address']
        :return:
        """
        self.street = source_data['street']
        self.zipcode = source_data['zipcode']
        self.city = source_data['city']
        self.state = source_data['state']
        self.latitude = source_data['latitude']
        self.longitude = source_data['longitude']

class ZEstimateData(SourceData):
    def __init__(self, **kwargs):
        self.amount = None
        self.amount_currency = None
        self.amount_last_updated = None
        self.amount_change_30days = None
        self.valuation_range_low = None
        self.valuation_range_high = None

    def set_data(self, source_data):
        """
        :source_data: Data from data.get('SearchResults:searchresults', None)['response']['results']['result']['zestimate']
        :return:
        """
        self.amount = int(source_data['amount']['#text'])
        self.amount_currency = source_data['amount']['@currency']
        self.amount_last_updated = source_data['last-updated']
        self.amount_change_30days = int(source_data['valueChange']['#text'])
        self.valuation_range_low = int(source_data['valuationRange']['low']['#text'])
        self.valuation_range_high = int(source_data['valuationRange']['high']['#text'])

class LocalRealEstate(SourceData):
    def __init__(self, **kwargs):
        self.region_name = None
        self.region_id = None
        self.region_type = None
        self.overview_link = None
        self.fsbo_link = None
        self.sale_link = None

    def set_data(self, source_data):
        """
        :source_data": Data from data.get('SearchResults:searchresults', None)['response']['results']['result']['localRealEstate']
        :return:
        """
        self.region_name = source_data['region']['@name']
        self.region_id = source_data['region']['@id']
        self.region_type =  source_data['region']['@type']
        self.overview_link =  source_data['region']['links']['overview']
        self.fsbo_link =  source_data['region']['links']['forSaleByOwner']
        self.sale_link =  source_data['region']['links']['forSale']


class Place(SourceData):
    """
    A class representing a property and it's details
    """
    def __init__(self, **kwargs):
        self.zpid = None
        self.links = Links()
        self.full_address = FullAddress()
        self.zestiamte = ZEstimateData()
        self.local_realestate = LocalRealEstate()

    def set_data(self, source_data):
        """
        :source_data": Data from data.get('SearchResults:searchresults', None)['response']['results']['result']
        :param source_data:
        :return:
        """
        if 'Zestimate:zestimate' in source_data:
            search_results = source_data.get('Zestimate:zestimate', None)['response']
        elif 'SearchResults:searchresults' in source_data:
            search_results = source_data.get('SearchResults:searchresults', None)['response']['results']['result']
        else:
            raise ZillowError({'message': "Invalid search results" % source_data})

        self.zpid = search_results.get('zpid', None)
        self.links.set_data(search_results['links'])
        self.full_address.set_data(search_results['address'])
        self.zestiamte.set_data(search_results['zestimate'])
        self.local_realestate.set_data(search_results['localRealEstate'])

    def get_dict(self):
        data = {
            'zpid': self.zpid,
            'links': self.links.get_dict(),
            'full_address': self.full_address.get_dict(),
            'zestimate': self.zestiamte.get_dict(),
            'local_realestate': self.local_realestate.get_dict()
        }
        return data



