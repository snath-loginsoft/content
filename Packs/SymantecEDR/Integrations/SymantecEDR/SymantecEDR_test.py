"""
Symantec EDR (On-prem) Integration - Unit Tests file
"""
# type: ignore
import pytest
import json
from datetime import datetime, timedelta
import dateparser
import os
from CommonServerPython import DemistoException
from SymantecEDR import Client, get_file_instance_command, get_domain_instance_command, get_endpoint_instance_command, \
    get_endpoint_file_association_list_command, get_domain_file_association_list_command, \
    get_endpoint_domain_association_list_command, get_deny_list_command, get_allow_list_command, \
    get_event_list_command, get_audit_event_command, get_system_activity_command, get_incident_list_command, \
    get_event_for_incident_list_command, pagination, PAGE_NUMBER_ERROR_MSG, PAGE_SIZE_ERROR_MSG, \
    compile_command_title_string, check_valid_indicator_value,\
    get_endpoint_status_command, get_endpoint_command, get_incident_uuid, convert_to_iso8601, \
    extract_headers_for_readable_output, get_data_of_current_page, parse_event_object_data, issue_sandbox_command, \
    check_sandbox_status, get_sandbox_verdict, get_association_filter_query, convert_list_to_str, get_query_limit


def util_load_json(path):
    with open(path) as f:
        return json.loads(f.read())


client = Client(
    base_url="http://test.com",
    verify=False,
    proxy=False,
    client_id="test_123",
    client_secret="test@12345"
)

FILE_INSTANCE_RESPONSE = util_load_json('test_data/file_instance_data.json')
DOMAIN_INSTANCE_RESPONSE = util_load_json('test_data/domain_instance_data.json')
ENDPOINT_INSTANCE_RESPONSE = util_load_json('test_data/endpoint_instance.json')
ENDPOINT_FILE_ASSOCIATION_RESPONSE = util_load_json('test_data/endpoint_file_association.json')
DOMAIN_FILE_ASSOCIATION_RESPONSE = util_load_json('test_data/domain_file_association.json')
ENDPOINT_DOMAIN_ASSOCIATION_RESPONSE = util_load_json('test_data/endpoint_domain_association.json')
DENY_LIST_RESPONSE = util_load_json('test_data/deny_list.json')
ALLOW_LIST_RESPONSE = util_load_json('test_data/deny_list.json')
EVENT_LIST_RESPONSE = util_load_json('test_data/event_list_data.json')
AUDIT_EVENT_RESPONSE = util_load_json('test_data/audit_event_data.json')
SYSTEM_ACTIVITY_RESPONSE = util_load_json('test_data/system_activity.json')
INCIDENT_LIST_RESPONSE = util_load_json('test_data/incident_list_data.json')
INCIDENT_COMMENT_RESPONSE = util_load_json('test_data/incident_comment_data.json')
INCIDENT_EVENT_FOR_INCIDENT = util_load_json('test_data/incident_event_data.json')
ENDPOINT_COMMAND_STATUS = util_load_json('test_data/endpoint_command_status.json')
ENDPOINT_COMMAND_ISOLATE = util_load_json('test_data/endpoint_command_isolate_endpoint.json')
ENDPOINT_COMMAND_REJOIN = util_load_json('test_data/endpoint_command_rejoin.json')
ENDPOINT_COMMAND_CANCEL = util_load_json('test_data/endpoint_command_cancel.json')
ENDPOINT_COMMAND_DELETE = util_load_json('test_data/endpoint_command_delete_endpoint_file.json')
HEADER_LIST = util_load_json('test_data/header_list.json')
SANDBOX_ISSUE_COMMAND = util_load_json('test_data/sandbox_issue_command.json')
SANDBOX_STATUS_COMMAND = util_load_json('test_data/sandbox_status_command.json')
SANDBOX_VERDICT_COMMAND = util_load_json('test_data/sandbox_verdict_command.json')


@pytest.mark.parametrize('raw_response, expected', [(FILE_INSTANCE_RESPONSE, FILE_INSTANCE_RESPONSE)])
def test_get_file_instance_command(mocker, raw_response, expected):
    """
    Tests get_get_file_instance_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_file_instance_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'get_file_instance', side_effect=[raw_response])
    with open(os.path.join("test_data", "command_readable_output/file_instance_command_readable_output.md"), 'r') as f:
        readable_output = f.read()
    command_results = get_file_instance_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']['result']
    assert context_detail == expected.get("result")
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(DOMAIN_INSTANCE_RESPONSE, DOMAIN_INSTANCE_RESPONSE)])
def test_get_domain_instance_command(mocker, raw_response, expected):
    """
    Tests get_domain_instance_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_domain_instance_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'get_domain_instance', side_effect=[raw_response])
    with open(os.path.join("test_data", "command_readable_output/endpoint_domain_instance_readable_output.md"), 'r') as f:
        readable_output = f.read()
    command_results = get_domain_instance_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']['result']
    assert context_detail == expected.get("result")
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(ENDPOINT_INSTANCE_RESPONSE, ENDPOINT_INSTANCE_RESPONSE)])
def test_get_endpoint_instance_command(mocker, raw_response, expected):
    """
    Tests get_endpoint_instance_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_endpoint_instance_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'get_endpoint_instance', side_effect=[raw_response])
    with open(os.path.join("test_data",
                           "command_readable_output/endpoint_instance_command_readable_output.md"), 'r') as f:
        readable_output = f.read()
    command_results = get_endpoint_instance_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']['result']
    assert context_detail == expected.get("result")
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(ENDPOINT_FILE_ASSOCIATION_RESPONSE,
                                                     ENDPOINT_FILE_ASSOCIATION_RESPONSE)])
def test_get_endpoint_file_association_list_command(mocker, raw_response, expected):
    """
    Tests get_endpoint_file_association_list_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_endpoint_file_association_list_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'list_endpoint_file', side_effect=[raw_response])
    with open(os.path.join(
            "test_data", "command_readable_output/endpoint_file_association_command_readable_output.md"), 'r') as f:
        readable_output = f.read()
    command_results = get_endpoint_file_association_list_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']['result']
    assert context_detail == expected.get("result")
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(DOMAIN_FILE_ASSOCIATION_RESPONSE,
                                                     DOMAIN_FILE_ASSOCIATION_RESPONSE)])
def test_get_domain_file_association_list_command(mocker, raw_response, expected):
    """
    Tests get_domain_file_association_list_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_domain_file_association_list_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'list_domain_file', side_effect=[raw_response])
    with open(os.path.join(
            "test_data", "command_readable_output/domain_file_association_command_readable_output.md"), 'r') as f:
        readable_output = f.read()
    command_results = get_domain_file_association_list_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(ENDPOINT_DOMAIN_ASSOCIATION_RESPONSE,
                                                     ENDPOINT_DOMAIN_ASSOCIATION_RESPONSE)])
def test_get_endpoint_domain_association_list_command(mocker, raw_response, expected):
    """
    Tests get_endpoint_domain_association_list_command function.
        Given:
            - mocker object.
            - raw_response test data.
            - expected output.
        When:
            - Running the 'get_endpoint_domain_association_list_command'.
        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'list_endpoint_domain', side_effect=[raw_response])
    with open(os.path.join(
            "test_data", "command_readable_output/endpoint_domain_association_command_readable_output.md"), 'r') as f:
        readable_output = f.read()
    command_results = get_endpoint_domain_association_list_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(DENY_LIST_RESPONSE, DENY_LIST_RESPONSE)])
def test_get_deny_list_command(mocker, raw_response, expected):
    """
    Tests get_deny_list_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.
        When:
            - Running the 'get_deny_list_command'.
        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 10}
    mocker.patch.object(client, 'get_deny_list', side_effect=[raw_response])
    with open(os.path.join(
            "test_data", "command_readable_output/deny_list_command_readable_output.md"), 'r') as f:
        readable_output = f.read()
    command_results = get_deny_list_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(ALLOW_LIST_RESPONSE, ALLOW_LIST_RESPONSE)])
def test_get_allow_list_command(mocker, raw_response, expected):
    """
    Tests get_allow_list_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_allow_list_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 10}
    mocker.patch.object(client, 'get_allow_list', side_effect=[raw_response])
    command_results = get_allow_list_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")


@pytest.mark.parametrize('raw_response, expected', [(EVENT_LIST_RESPONSE, EVENT_LIST_RESPONSE)])
def test_get_event_list_command(mocker, raw_response, expected):
    """
    Tests get_event_list_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_event_list_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'get_event_list', side_effect=[raw_response])
    command_results = get_event_list_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")


@pytest.mark.parametrize('raw_response, expected', [(AUDIT_EVENT_RESPONSE, AUDIT_EVENT_RESPONSE)])
def test_get_audit_event_command(mocker, raw_response, expected):
    """
    Tests get_audit_event_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_audit_event_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'get_audit_event', side_effect=[raw_response])
    command_results = get_audit_event_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")


@pytest.mark.parametrize('raw_response, expected', [(SYSTEM_ACTIVITY_RESPONSE, SYSTEM_ACTIVITY_RESPONSE)])
def test_get_system_activity_command(mocker, raw_response, expected):
    """
    Tests get_system_activity_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_system_activity_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'get_system_activity', side_effect=[raw_response])
    command_results = get_system_activity_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")


@pytest.mark.parametrize('raw_response, expected', [(INCIDENT_LIST_RESPONSE, INCIDENT_LIST_RESPONSE)])
def test_get_incident_list_command(mocker, raw_response, expected):
    """
    Tests get_incident_list_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_incident_list_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'get_incident', side_effect=[raw_response])
    command_results = get_incident_list_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")


@pytest.mark.parametrize('raw_response, expected', [(INCIDENT_LIST_RESPONSE, '9d6f2100-7158-11ed-da26-000000000001')])
def test_get_incident_uuid(mocker, raw_response, expected):
    args = {
        "incident_id": 100010
    }
    mocker.patch.object(client, 'http_request', side_effect=[raw_response])
    uuid = get_incident_uuid(client, args)

    # results is CommandResults list
    assert uuid == expected


@pytest.mark.parametrize('raw_response, expected', [(INCIDENT_EVENT_FOR_INCIDENT, INCIDENT_EVENT_FOR_INCIDENT)])
def test_get_event_for_incident_list_command(mocker, raw_response, expected):
    """
    Tests get_event_for_incident_list_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_event_for_incident_list_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"limit": 1}
    mocker.patch.object(client, 'get_event_for_incident', side_effect=[raw_response])
    command_results = get_event_for_incident_list_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["result"]
    assert context_detail == expected.get("result")


@pytest.mark.parametrize('raw_response, expected', [(ENDPOINT_COMMAND_STATUS, ENDPOINT_COMMAND_STATUS)])
def test_get_endpoint_status_command(mocker, raw_response, expected):
    """
    Tests get_endpoint_status_command function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_endpoint_status_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"command_id": '35fcb7c144764188b810799a120b26eb-2022-12-09'}
    with open(os.path.join(
            "test_data",
            "command_readable_output/endpoint_command_status_readable_output.md"
    ), 'r') as f:
        readable_output = f.read()
    mocker.patch.object(client, 'http_request', side_effect=[raw_response])
    command_results = get_endpoint_status_command(client, args)

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']["status"]
    assert context_detail == expected.get("status")
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(ENDPOINT_COMMAND_ISOLATE, ENDPOINT_COMMAND_ISOLATE)])
def test_get_endpoint_command_isolate(mocker, raw_response, expected):
    """
    Tests get_endpoint_command isolate endpoint function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_endpoint_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"device_id": '"393b8e82-fe40-429f-8e5e-c6b79a0f2b1c'}
    with open(os.path.join(
            "test_data",
            "command_readable_output/endpoint_command_isolate_readable_output.md"
    ), 'r') as f:
        readable_output = f.read()
    mocker.patch.object(client, 'get_isolate_endpoint', side_effect=[raw_response])
    command_results = get_endpoint_command(client, args, 'symantec-edr-endpoint-isolate')

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']
    assert context_detail == expected
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(ENDPOINT_COMMAND_REJOIN, ENDPOINT_COMMAND_REJOIN)])
def test_get_endpoint_command_rejoin(mocker, raw_response, expected):
    """
    Tests get_endpoint_command rejoin function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_endpoint_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"device_id": '"393b8e82-fe40-429f-8e5e-c6b79a0f2b1c'}
    with open(os.path.join(
            "test_data",
            "command_readable_output/endpoint_command_rejoin_readable_output.md"
    ), 'r') as f:
        readable_output = f.read()
    mocker.patch.object(client, 'get_rejoin_endpoint', side_effect=[raw_response])
    command_results = get_endpoint_command(client, args, 'symantec-edr-endpoint-rejoin')

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']
    assert context_detail == expected
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(ENDPOINT_COMMAND_DELETE, ENDPOINT_COMMAND_DELETE)])
def test_get_endpoint_command_delete(mocker, raw_response, expected):
    """
    Tests get_endpoint_command delete function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_endpoint_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {
        'device_id': '393b8e82-fe40-429f-8e5e-c6b79a0f2b1c',
        'sha2': '0ce49dc9f71360bf9dd21b8e3af4641834f85eed7d80a7de0940508437e68970'
    }
    with open(os.path.join(
            "test_data",
            "command_readable_output/endpoint_command_delete_readable_output.md"
    ), 'r') as f:
        readable_output = f.read()
    mocker.patch.object(client, 'get_delete_endpoint', side_effect=[raw_response])
    command_results = get_endpoint_command(client, args, 'symantec-edr-endpoint-delete-file')

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']
    assert context_detail == expected
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('raw_response, expected', [(ENDPOINT_COMMAND_CANCEL, ENDPOINT_COMMAND_CANCEL)])
def test_get_endpoint_command_cancel(mocker, raw_response, expected):
    """
    Tests get_endpoint_command cancel function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'get_endpoint_command'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"device_id": '"393b8e82-fe40-429f-8e5e-c6b79a0f2b1c'}
    with open(os.path.join(
            "test_data",
            "command_readable_output/endpoint_command_cancel_readable_output.md"
    ), 'r') as f:
        readable_output = f.read()
    mocker.patch.object(client, 'get_cancel_endpoint', side_effect=[raw_response])
    command_results = get_endpoint_command(client, args, 'symantec-edr-endpoint-cancel-command')

    # results is CommandResults list
    context_detail = command_results.to_context()['Contents']
    assert context_detail == expected
    assert command_results.readable_output == readable_output


@pytest.mark.parametrize('sub_context, params, total_record, expected_title', [
    ('File Endpoint', {'page': 1, 'page_size': 10}, 100,
     'File Endpoint List\nShowing page 1\nShowing 10 out of 100 Record(s) Found.'),
    ('File Endpoint', {'page': 0, 'page_size': 0}, 0, 'File Endpoint List'),
    ('File Endpoint', {'limit': 5, 'page': None, 'page_size': 10}, 10,
     'File Endpoint List\nShowing page 1\nShowing 10 out of 10 Record(s) Found.'),
    ('File Endpoint', {'limit': 5, 'page': 1, 'page_size': None}, 10,
     'File Endpoint List\nShowing page 1\nShowing 10 out of 10 Record(s) Found.'),
    ('File Endpoint', {'limit': 5}, 10, 'File Endpoint List'),
])
def test_compile_command_title_string(sub_context, params, total_record, expected_title):
    """
        Tests the compile_command_title_string function

            Given:
                1. a sub context, page, page size and total records arguments.
                2. a sub context, 0 values for page, page size and total records arguments.
                3. a sub context, page = None.
                4. a sub context, page size = None.

            When:
                - Running the 'compile_command_title_string function'.

            Then:
                - Checks the output of the command function with the expected output.
    """

    actual_title = compile_command_title_string(sub_context, params, total_record)
    assert actual_title == expected_title


# @pytest.mark.parametrize('context_dict, expected_result', [
#     ({'access_token_timestamp': int(time.time()), 'access_token': '12345'}, '12345'),
#     ({'access_token_timestamp': int(time.time() - 300), 'access_token': '12345'}, '12345'),
#     ({'access_token_timestamp': int(time.time() - 3660), 'access_token': '12345'}, None),
#     ({}, None),
# ])
# def test_get_access_token_from_context(context_dict, expected_result):
#     actual_result = get_access_token_from_context(context_dict)
#     assert actual_result == expected_result


@pytest.mark.parametrize('indicator_type, indicator_value, expected_result', [
    ('urls', 'https://www.facebook.com', True),
    ('ip', '1.1.1.1', True),
    ('sha256', '1dc0c8d7304c177ad0e74d3d2f1002eb773f4b180685a7df6bbe75ccc24b0164', True),  # File sha256
    ('md5', 'eb67bdf0eaac6ea0ca18667f6cacd5fb', True)
])
def test_check_valid_indicator_value(indicator_type, indicator_value, expected_result):
    """
        Tests the check_valid_indicator_value function.

            Given:
                indicator_type - type of indicator
                indicator_value - Value of indicator

            When:
                - Running the 'check_valid_indicator_value function'.

            Then:
                - Checks the output of the command function with the expected result.
    """
    actual_result = check_valid_indicator_value(indicator_type, indicator_value)
    assert actual_result == expected_result


@pytest.mark.parametrize('indicator_type, indicator_value, expected_err_msg', [
    ('domains', 'abcd123', 'Indicator domains type id not support'),
    ('urls', '123245', '123245 is not a valid urls'),
    ('ip', 'google.1234', '"google.1234" is not a valid IP'),
    ('sha256', 'abcde34', 'abcde34 is not a valid sha256'),
    ('md5', 'eb67bdf0eaac6e', 'eb67bdf0eaac6e is not a valid md5')
])
def test_check_valid_indicator_value_wrong_input(indicator_type, indicator_value, expected_err_msg):
    """
        Tests the check_valid_indicator_value function.

            Given:
                indicator_type - type of indicator.
                indicator_value - Value of indicator massage.

            When:
                - Running the 'check_valid_indicator_value function'.

            Then:
                - Checks the output of the command function with the expected error message.
    """
    with pytest.raises(ValueError) as e:
        check_valid_indicator_value(indicator_type, indicator_value)
    assert e.value.args[0] == expected_err_msg


def test_get_access_token_or_login(requests_mock):
    """
        Tests the get_access_token_or_login function.
            Given:
                - requests_mock object.
            When:
                - Running the 'get_access_token_or_login function'.
            Then:
                -  Checks the output of the command function with the expected output.
    """
    post_req_url = client._base_url + '/atpapi/oauth2/tokens'
    # before login, access_token is not present
    requests_mock.post(post_req_url, json={'access_token': '12345'})
    assert client.headers == {'Content-Type': 'application/json'}
    client.get_access_token_or_login()
    assert client.access_token == "12345"
    # after login, access_token is present
    assert client.headers == {'Authorization': f'Bearer {client.access_token}', 'Content-Type': 'application/json'}


@pytest.mark.parametrize('raw_response, expected', [(INCIDENT_LIST_RESPONSE, 'ok')])
def test_test_module(mocker, raw_response, expected):
    """
        Tests the test_module function.
            Given:
                - no argument required.
            When:
                - Running the 'test_module function'.
            Then:
                - Check weather the given credentials are correct or not.
    """
    from SymantecEDR import test_module
    mocker.patch.object(client, 'http_request', side_effect=[raw_response])
    output = test_module(client)
    # results
    assert output == expected


@pytest.mark.parametrize('response_code', [401, 500])
def test_test_module__invalid(requests_mock, response_code):
    """
        Tests the test_module handle exception.
            Given:
                - no argument required.
            When:
                - Running the 'test_module function'.
            Then:
                - Check weather the given credentials are correct or not.
    """
    from SymantecEDR import test_module
    with pytest.raises(DemistoException) as e:
        post_req_url = client._base_url + '/atpapi/v2/incidents'
        requests_mock.get(post_req_url, headers=client.headers)
        test_module(client)
        assert e.value.res.status_code == response_code


DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
now = str(datetime.today())
now_iso = dateparser.parse(now, settings={'TIMEZONE': 'UTC'}).strftime(DATE_FORMAT)[:23] + "Z"
week_before = str(datetime.today() - timedelta(days=7))
iso_datatime_week_before = dateparser.parse(week_before, settings={'TIMEZONE': 'UTC'}).strftime(DATE_FORMAT)[:23] + "Z"


@pytest.mark.parametrize('date_string, expected_result', [
    (now, now_iso),
    (week_before, iso_datatime_week_before)
])
def test_convert_to_iso8601(date_string, expected_result):
    """
        Tests the convert timestamp to iso8601 formate.

            Given:
                date_string - Datetime.
            When:
                - Running the 'test_convert_to_iso8601 function'.

            Then:
                - Checks the output of the command function with the expected ISO Date format .
    """
    actual_result = convert_to_iso8601(date_string)
    assert actual_result == str(expected_result)


@pytest.mark.parametrize('raw_response, expected', [(HEADER_LIST, 'Id')])
def test_extract_headers_for_readable_output(raw_response, expected):
    """
    Tests extract_headers_for_readable_output function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'extract_headers_for_readable_output'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    actual_result = extract_headers_for_readable_output(raw_response)
    assert actual_result[0] == expected


@pytest.mark.parametrize('raw_response, offset, limit, expected', [(HEADER_LIST, 0, 3, HEADER_LIST[:3]),
                                                                   (HEADER_LIST, 2, 3, HEADER_LIST[2:2 + 3])])
def test_get_data_of_current_page(raw_response, offset, limit, expected):
    """
    Tests get_data_of_current_page function.
        Given:
            - raw_response test data.
            - offset Page Offset.
            - limit Max rows to fetches
            - expected output.
        When:
            - Running the 'get_data_of_current_page'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    actual_result = get_data_of_current_page(raw_response, offset, limit)
    assert actual_result == expected


@pytest.mark.parametrize('raw_event_data', [EVENT_LIST_RESPONSE])
def test_parse_event_object_data(raw_event_data):
    """
    Tests parse_event_object_data function.
        Given:
            - raw_response test data.
            - expected output.
        When:
            - Running the 'parse_event_object_data'.
        Then:
            -  Checks the output of the command function with the expected output.
    """
    results = parse_event_object_data(raw_event_data.get('result')[0])
    assert results.get('file_file_sha2') == 'c4e078607db2784be7761c86048dffa6f3ef04b551354a32fcdec3b6a3450905'


@pytest.mark.parametrize('raw_response, expected', [(SANDBOX_ISSUE_COMMAND, SANDBOX_ISSUE_COMMAND)])
def test_issue_sandbox_command(mocker, raw_response, expected):
    """
    Tests issue_sandbox_command Issue function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'issue_sandbox_command('.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"file": '1dc0c8d7304c177ad0e74d3d2f1002eb773f4b180685a7df6bbe75ccc24b0164'}
    mocker.patch.object(client, 'http_request', side_effect=[raw_response])
    command_results = issue_sandbox_command(client, args,)

    # results is CommandResults list
    context_detail = command_results.raw_response
    assert context_detail == expected


@pytest.mark.parametrize('raw_response, expected', [(SANDBOX_STATUS_COMMAND, SANDBOX_STATUS_COMMAND)])
def test_check_sandbox_status(mocker, raw_response, expected):
    """
    Tests check_sandbox_status status function.

        Given:
            - mocker object.
            - raw_response test data.
            - expected output.

        When:
            - Running the 'check_sandbox_status'.

        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"command_id": 'a4277ce5ebd84fe18c30fa67a05b42c9-2023-02-06'}
    mocker.patch.object(client, 'http_request', side_effect=[raw_response])
    command_results = check_sandbox_status(client, args,)

    # results is CommandResults list
    context_detail = command_results.raw_response
    assert context_detail == expected


@pytest.mark.parametrize('raw_response, expected', [(SANDBOX_VERDICT_COMMAND, SANDBOX_VERDICT_COMMAND)])
def test_get_sandbox_verdict(mocker, raw_response, expected):
    """
    Tests get_sandbox_verdict status function.
        Given:
            - mocker object.
            - raw_response test data.
            - expected output.
        When:
            - Running the 'get_sandbox_verdict'.
        Then:
            -  Checks the output of the command function with the expected output.
    """
    args = {"file": '1dc0c8d7304c177ad0e74d3d2f1002eb773f4b180685a7df6bbe75ccc24b0164'}
    mocker.patch.object(client, 'http_request', side_effect=[raw_response] * 5)
    command_results = get_sandbox_verdict(client, args)

    # results is CommandResults list
    context_detail = command_results.raw_response
    assert context_detail == expected


@pytest.mark.parametrize('query_type, query_value, expected_result', [
    ('sha256', '1dc0c8d7304c177ad0e74d3d2f1002eb773f4b180685a7df6bbe75ccc24b0164',
     'sha2: (1dc0c8d7304c177ad0e74d3d2f1002eb773f4b180685a7df6bbe75ccc24b0164)'),
    ('device_uid', '393b8e82-fe40-429f-8e5e-c6b79a0f2b1c',
     'device_uid: (393b8e82-fe40-429f-8e5e-c6b79a0f2b1c)')
])
def test_get_association_filter_query(query_type, query_value, expected_result):
    """
        Tests the get_association_filter_query function.

            Given:
                query_type - Indicator search obj
                query_value - Indicator search value
            When:
                - Running the 'get_association_filter_query function'.

            Then:
                - Checks the output of the command function with the expected result.
    """
    args = {'search_object': query_type, 'search_value': query_value}
    result = get_association_filter_query(args)
    assert result == expected_result


@pytest.mark.parametrize('list_data, expected_result', [
    ([1, 2, 3, 4], "1,2,3,4"),
])
def test_convert_list_to_str(list_data, expected_result):
    """
        Tests the convert_list_to_str function.

            Given:
                list_data - Lists data
            When:
                - Running the 'convert_list_to_str function'.

            Then:
                - Checks the output of the command function with the expected result.
    """
    result = convert_list_to_str(list_data)
    assert result == expected_result


@pytest.mark.parametrize('page, page_size, expected_result', [
    # page, page_size, (page_limit, offset)
    (2, 5, (10, 5)),
    (None, 5, (5, 0)),
    (2, None, (100, 50)),
    (3, None, (150, 100)),
    (1, 1, (1, 0)),
    (None, None, (50, 0))
])
def test_pagination(page, page_size, expected_result):
    """
    Tests the pagination function.

        Given:
            - page and page size arguments.

        When:
            - Running the 'pagination function'.

        Then:
            - Checks that the limit and offset are calculated as expected.
    """
    actual_result = pagination(page, page_size)
    assert actual_result == expected_result


@pytest.mark.parametrize('page, page_size, expected_err_msg', [
    (0, 5, PAGE_NUMBER_ERROR_MSG),
    (1, 0, PAGE_SIZE_ERROR_MSG),
    (-1, 5, PAGE_NUMBER_ERROR_MSG),
    (1, -2, PAGE_SIZE_ERROR_MSG),
])
def test_pagination_wrong_input(page, page_size, expected_err_msg):
    """
    Tests the pagination function.

        Given:
            1+2 -  page and page size arguments with 0 value.
            3+4 -  page and page size arguments with < 0 value.

        When:
            - Running the 'pagination function'.

        Then:
            - Checks that the expected err message is raised.
    """
    with pytest.raises(DemistoException) as e:
        pagination(page, page_size)
    assert e.value.args[0] == expected_err_msg


@pytest.mark.parametrize('param, expected_result', [
    ({'limit': 5, 'page_size': None}, (5, 0)),  #
    ({'limit': 5, 'page_size': 15}, (15, 0)),
    ({'limit': 5, 'page': 1}, (50, 0)),
    ({'limit': 5, 'page': 1, 'page_size': 10}, (10, 0)),
    ({'limit': 5, 'page': 2, 'page_size': 10}, (20, 10)),
])
def test_get_query_limit(param, expected_result):
    """
        Tests the get_query_limit function.

            Given:
                param - parameter data
            When:
                - Running the 'get_query_limit function'.

            Then:
                - Checks the output of the command function with the expected result.
    """
    (limit, offset) = get_query_limit(param)
    assert limit == expected_result[0], f"Validate limit {limit} == {expected_result[0]}"
    assert offset == expected_result[1], f"Validate offset {offset} == {expected_result[1]}"
