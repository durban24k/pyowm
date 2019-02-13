import json
from pyowm.pollutionapi30 import no2index, so2index
from pyowm.weatherapi25 import location
from pyowm.abstractions import jsonparser
from pyowm.exceptions import parse_response_error
from pyowm.utils import formatting, timestamps


class NO2IndexParser(jsonparser.JSONParser):
    """
    Concrete *JSONParser* implementation building an *NO2Index* instance out
    of raw JSON data coming from OWM Weather API responses.

    """

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses an *NO2Index* instance out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: an *NO2Index* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        try:
            # -- reference time (strip away Z and T on ISO8601 format)
            t = d['time'].replace('Z', '+00').replace('T', ' ')
            reference_time = formatting._ISO8601_to_UNIXtime(t)

            # -- reception time (now)
            reception_time = timestamps.now('unix')

            # -- location
            lon = float(d['location']['longitude'])
            lat = float(d['location']['latitude'])
            place = location.Location(None, lon, lat, None)

            # -- CO samples
            no2_samples = [dict(label=key,
                                precision=d['data'][key]['precision'],
                                value=d['data'][key]['value']) for key in d['data']]

        except KeyError:
            raise parse_response_error.ParseResponseError(
                      ''.join([__name__, ': impossible to parse NO2Index']))

        return no2index.NO2Index(reference_time, place, None, no2_samples,
                                 reception_time)

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)


class SO2IndexParser(jsonparser.JSONParser):
    """
    Concrete *JSONParser* implementation building an *SO2Index* instance out
    of raw JSON data coming from OWM Weather API responses.

    """

    def __init__(self):
        pass

    def parse_JSON(self, JSON_string):
        """
        Parses an *SO2Index* instance out of raw JSON data. Only certain
        properties of the data are used: if these properties are not found or
        cannot be parsed, an error is issued.

        :param JSON_string: a raw JSON string
        :type JSON_string: str
        :returns: a *SO2Index* instance or ``None`` if no data is available
        :raises: *ParseResponseError* if it is impossible to find or parse the
            data needed to build the result, *APIResponseError* if the JSON
            string embeds an HTTP status error

        """
        if JSON_string is None:
            raise parse_response_error.ParseResponseError('JSON data is None')
        d = json.loads(JSON_string)
        try:
            # -- reference time (strip away Z and T on ISO8601 format)
            t = d['time'].replace('Z', '+00').replace('T', ' ')
            reference_time = formatting._ISO8601_to_UNIXtime(t)

            # -- reception time (now)
            reception_time = timestamps.now('unix')

            # -- location
            lon = float(d['location']['longitude'])
            lat = float(d['location']['latitude'])
            place = location.Location(None, lon, lat, None)

            # -- SO2 samples
            so2_samples = d['data']

        except KeyError:
            raise parse_response_error.ParseResponseError(
                      ''.join([__name__, ': impossible to parse COIndex']))

        return so2index.SO2Index(reference_time, place, None, so2_samples,
                                 reception_time)

    def __repr__(self):
        return "<%s.%s>" % (__name__, self.__class__.__name__)
