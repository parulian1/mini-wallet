from rest_framework import status


class ResponseCode(object):
    error_auth = 'error_auth'
    error_missing_bearer = 'error_missing_bearer'
    error_token_expired = 'error_token_expired'
    error_wallet_not_found = 'error_wallet_not_found'
    error_wallet_already_enabled = 'error_wallet_already_enabled'
    error_wallet_is_disabled = 'error_wallet_is_disabled'
    error_wallet_already_disabled = 'error_wallet_already_disabled'
    error_wallet_insufficient_balance = 'error_wallet_insufficient_balance'
    error_user_not_found = 'error_user_not_found'
    error_param = 'error_param'
    error_sign = 'error_sign'
    error_forbidden = 'error_forbidden'
    error_network = 'error_network'
    error_system_busy = 'error_system_busy'
    error_validation_failure = 'error_validation_failure'
    error_method_not_allowed = 'error_method_not_allowed'
    error_permission = 'error_permission'
    no_content = 'no_content'
    created = 'created'
    ok = 'ok'
    already_reported = 'already_reported'


RESPONSE_STATUS = {
    ResponseCode.error_auth: status.HTTP_401_UNAUTHORIZED,
    ResponseCode.error_token_expired: status.HTTP_401_UNAUTHORIZED,
    ResponseCode.error_missing_bearer: status.HTTP_401_UNAUTHORIZED,
    ResponseCode.error_user_not_found: status.HTTP_404_NOT_FOUND,
    ResponseCode.error_wallet_not_found: status.HTTP_404_NOT_FOUND,
    ResponseCode.error_wallet_already_enabled: status.HTTP_208_ALREADY_REPORTED,
    ResponseCode.error_wallet_is_disabled: status.HTTP_404_NOT_FOUND,
    ResponseCode.error_wallet_already_disabled: status.HTTP_404_NOT_FOUND,
    ResponseCode.error_wallet_insufficient_balance: status.HTTP_400_BAD_REQUEST,
    ResponseCode.error_param: status.HTTP_400_BAD_REQUEST,
    ResponseCode.error_sign: status.HTTP_400_BAD_REQUEST,
    ResponseCode.error_validation_failure: status.HTTP_400_BAD_REQUEST,
    ResponseCode.error_permission: status.HTTP_400_BAD_REQUEST,

    ResponseCode.error_forbidden: status.HTTP_403_FORBIDDEN,
    ResponseCode.error_network: status.HTTP_503_SERVICE_UNAVAILABLE,
    ResponseCode.error_system_busy: status.HTTP_503_SERVICE_UNAVAILABLE,

    ResponseCode.error_method_not_allowed: status.HTTP_405_METHOD_NOT_ALLOWED,

    ResponseCode.no_content: status.HTTP_204_NO_CONTENT,
    ResponseCode.created: status.HTTP_201_CREATED,
    ResponseCode.ok: status.HTTP_200_OK,
    ResponseCode.already_reported: status.HTTP_208_ALREADY_REPORTED
}

VALID_RESPONSE = [ResponseCode.no_content, ResponseCode.created, ResponseCode.ok, ResponseCode.already_reported]
