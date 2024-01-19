from utils.constant import RESPONSE_STATUS, VALID_RESPONSE, ResponseCode

from rest_framework.response import Response


class ApiMixin(object):

    @staticmethod
    def api_response(code=ResponseCode.ok, data=None, message=None):
        """
            Handling customize response

            if not 200 or 201,
                return {'error': <error param>, 'message': <detail of error>}
                do anything with error_param to support FE specific error handling.

            if 200 or 201
                return {'data': <data response'>, 'metadata': <metadata paginate>}
        """
        # return 204 if no data query set
        if not data and code is ResponseCode.no_content:
            return Response(None, status=RESPONSE_STATUS[ResponseCode.no_content])

        resp_data = data
        return Response({
            'status': 'success' if code in VALID_RESPONSE else 'fail',
            'data': resp_data
        }, status=RESPONSE_STATUS[code])
