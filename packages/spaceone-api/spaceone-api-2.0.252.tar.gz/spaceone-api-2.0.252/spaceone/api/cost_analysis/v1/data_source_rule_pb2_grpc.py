# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.cost_analysis.v1 import data_source_rule_pb2 as spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2

GRPC_GENERATED_VERSION = '1.64.1'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in spaceone/api/cost_analysis/v1/data_source_rule_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class DataSourceRuleStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSourceRule/create',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.CreateDataSourceRuleRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.FromString,
                _registered_method=True)
        self.update = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSourceRule/update',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.UpdateDataSourceRuleRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.FromString,
                _registered_method=True)
        self.change_order = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSourceRule/change_order',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.ChangeDataSourceRuleOrderRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.FromString,
                _registered_method=True)
        self.delete = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSourceRule/delete',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.get = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSourceRule/get',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.FromString,
                _registered_method=True)
        self.list = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSourceRule/list',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRulesInfo.FromString,
                _registered_method=True)
        self.stat = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.DataSourceRule/stat',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                _registered_method=True)


class DataSourceRuleServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Creates a new DataSourceRule. When creating the resource, this method can apply two types of conditions: mapping projects where the cost incurred to the Cost, and mapping cloud service accounts to the Cost. By adjusting the `condition_policy` parameter, the DataSourceRule can be applied when all conditions are met, applied when any of the conditions are met, or always applied regardless of whether the conditions are met.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Updates a specific DataSourceRule. You can make changes in DataSourceRule settings, including filtering conditions. If the parameter `is_default` is `true`, only `Admin` type User can use this method.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def change_order(self, request, context):
        """Changes the priority order of the DataSourceRules to apply. If there are multiple DataSourceRules applied in a specific service account, the priority order of the resources is requried. This method changes the priority order to apply DataSourceRules.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Deletes a specific DataSourceRule. You must specify the `data_source_rule_id` of the DataSourceRule to delete. If the parameter `is_default` is `true`, only `Admin` type User can use this method.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Gets a specific DataSourceRule. Prints detailed information about the DataSourceRule, including  `conditions_policy` and conditions applied to DataSources.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Gets a list of all DataSourceRules. You can use a query to get a filtered list of DataSourceRules.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DataSourceRuleServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.CreateDataSourceRuleRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.UpdateDataSourceRuleRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.SerializeToString,
            ),
            'change_order': grpc.unary_unary_rpc_method_handler(
                    servicer.change_order,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.ChangeDataSourceRuleOrderRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRulesInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.cost_analysis.v1.DataSourceRule', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('spaceone.api.cost_analysis.v1.DataSourceRule', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class DataSourceRule(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.DataSourceRule/create',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.CreateDataSourceRuleRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.DataSourceRule/update',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.UpdateDataSourceRuleRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def change_order(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.DataSourceRule/change_order',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.ChangeDataSourceRuleOrderRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.DataSourceRule/delete',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.DataSourceRule/get',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.DataSourceRule/list',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleQuery.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRulesInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.DataSourceRule/stat',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_data__source__rule__pb2.DataSourceRuleStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
