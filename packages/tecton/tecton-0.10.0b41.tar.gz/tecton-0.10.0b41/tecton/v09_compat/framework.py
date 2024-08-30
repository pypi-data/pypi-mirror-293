from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from typeguard import typechecked

from tecton import FeatureReference
from tecton import types
from tecton.framework import base_tecton_object
from tecton.framework import configs
from tecton.framework.entity import Entity as Entity_v1_0
from tecton.framework.feature_view import FeatureView
from tecton.framework.feature_view import RealtimeFeatureView as RealtimeFeatureView_v1_0
from tecton_core import conf
from tecton_core import feature_definition_wrapper
from tecton_core import id_helper
from tecton_core import specs
from tecton_core.data_types import UnknownType
from tecton_proto.args import basic_info__client_pb2 as basic_info_pb2
from tecton_proto.args import entity__client_pb2 as entity__args_pb2
from tecton_proto.common import schema__client_pb2 as schema_pb2


class Entity(Entity_v1_0):
    """A Tecton Entity, used to organize and join features.

    An Entity is a class that represents an Entity that is being modeled in Tecton. Entities are used to index and
    organize features - a :class:`FeatureView` contains at least one Entity.

    Entities contain metadata about *join keys*, which represent the columns that are used to join features together.

    Example of an Entity declaration:

    .. code-block:: python

        from tecton import Entity

        customer = Entity(
            name='customer',
            join_keys=['customer_id'],
            description='A customer subscribing to a Sports TV subscription service',
            owner='matt@tecton.ai',
            tags={'release': 'development'}
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        prevent_destroy: bool = False,
        join_keys: Optional[Union[str, List[str]]] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """Declare a new Entity.

        :param name: Unique name for the new entity.
        :param description: Short description of the new entity.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
            destructive update) during tecton plan/apply. To remove or update this object, `prevent_destroy` must be
            set to False via the same tecton apply or a separate tecton apply. `prevent_destroy` can be used to prevent accidental changes
            such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
            triggers expensive rematerialization jobs. `prevent_destroy` also blocks changes to dependent Tecton objects
            that would trigger a recreate of the tagged object, e.g. if `prevent_destroy` is set on a Feature Service,
            that will also prevent deletions or re-creates of Feature Views used in that service. `prevent_destroy` is
            only enforced in live (i.e. non-dev) workspaces.
        :param join_keys: Names of columns that uniquely identify the entity in FeatureView's SQL statement
            for which features should be aggregated. Defaults to using ``name`` as the entity's join key.
        :param options: Additional options to configure the Entity. Used for advanced use cases and beta features.

        :raises TectonValidationError: if the input non-parameters are invalid.
        """
        from tecton_core.repo_file_handler import construct_fco_source_info

        if not join_keys:
            resolved_join_keys = schema_pb2.Column(name=name, offline_data_type=UnknownType().proto)
        elif isinstance(join_keys, str):
            resolved_join_keys = [schema_pb2.Column(name=join_keys, offline_data_type=UnknownType().proto)]
        else:
            resolved_join_keys = [
                schema_pb2.Column(name=join_key, offline_data_type=UnknownType().proto) for join_key in join_keys
            ]

        args = entity__args_pb2.EntityArgs(
            entity_id=id_helper.IdHelper.generate_id(),
            info=basic_info_pb2.BasicInfo(name=name, description=description, tags=tags, owner=owner),
            join_keys=resolved_join_keys,
            version=feature_definition_wrapper.FrameworkVersion.FWV5.value,
            prevent_destroy=prevent_destroy,
            options=options,
        )
        info = base_tecton_object.TectonObjectInfo.from_args_proto(args.info, args.entity_id)
        source_info = construct_fco_source_info(args.entity_id)
        self.__attrs_init__(info=info, spec=None, args=args, source_info=source_info)

        # Note! This is 1.0 behavior required by validation on creation
        if not conf.get_bool("TECTON_SKIP_OBJECT_VALIDATION"):
            self._validate()
        self._spec = specs.EntitySpec.from_args_proto(self._args)
        base_tecton_object._register_local_object(self)


class OnDemandFeatureView(RealtimeFeatureView_v1_0):
    # TODO(FE-2269): Move deprecated function implementations to v09 objects
    pass


@typechecked
def on_demand_feature_view(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    owner: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
    prevent_destroy: bool = False,
    mode: str,
    sources: List[Union[configs.RequestSource, FeatureView, "FeatureReference"]],
    schema: List[types.Field],
    environments: Optional[List[str]] = None,
):
    """
    Declare an On-Demand Feature View

    :param mode: Whether the annotated function is a pipeline function ("pipeline" mode) or a transformation function ("python" or "pandas" mode).
        For the non-pipeline mode, an inferred transformation will also be registered.
    :param sources: The data source inputs to the feature view. An input can be a RequestSource or a materialized Feature View.
    :param schema: Tecton schema matching the expected output of the transformation.
    :param description: A human readable description.
    :param owner: Owner name (typically the email of the primary maintainer).
    :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
    :param name: Unique, human friendly name that identifies the FeatureView. Defaults to the function name.
    :param prevent_destroy: If True, this Tecton object will be blocked from being deleted or re-created (i.e. a
        destructive update) during tecton plan/apply. To remove or update this object, ``prevent_destroy`` must be
        set to False via the same tecton apply or a separate tecton apply. ``prevent_destroy`` can be used to prevent accidental changes
        such as inadvertantly deleting a Feature Service used in production or recreating a Feature View that
        triggers expensive rematerialization jobs. ``prevent_destroy`` also blocks changes to dependent Tecton objects
        that would trigger a recreate of the tagged object, e.g. if ``prevent_destroy`` is set on a Feature Service,
        that will also prevent deletions or re-creates of Feature Views used in that service. ``prevent_destroy`` is
        only enforced in live (i.e. non-dev) workspaces.
    :param environments: The environments in which this feature view can run. Defaults to `None`, which means
        the feature view can run in any environment. If specified, the feature view will only run in the specified
        environments. Learn more about environments at
        https://docs.tecton.ai/docs/defining-features/feature-views/on-demand-feature-view/on-demand-feature-view-environments.
    :return: An object of type :class:`tecton.OnDemandFeatureView`.

    An example declaration of an on-demand feature view using Python mode.
    With Python mode, the function sources will be dictionaries, and the function is expected to return a dictionary matching the schema from `output_schema`.
    Tecton recommends using Python mode for improved online serving performance.

    .. code-block:: python

        from tecton import RequestSource, on_demand_feature_view
        from tecton.types import Field, Float64, Int64

        # Define the request schema
        transaction_request = RequestSource(schema=[Field("amount", Float64)])

        # Define the output schema
        output_schema = [Field("transaction_amount_is_high", Int64)]

        # This On-Demand Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
        @on_demand_feature_view(
            sources=[transaction_request],
            mode='python',
            schema=output_schema,
            owner='matt@tecton.ai',
            tags={'release': 'production', 'prevent-destroy': 'true', 'prevent-recreate': 'true'},
            description='Whether the transaction amount is considered high (over $10000)'
        )

        def transaction_amount_is_high(transaction_request):
            result = {}
            result['transaction_amount_is_high'] = int(transaction_request['amount'] >= 10000)
            return result

    An example declaration of an on-demand feature view using Pandas mode.
    With Pandas mode, the function sources will be Pandas Dataframes, and the function is expected to return a Dataframe matching the schema from `output_schema`.

    .. code-block:: python

        from tecton import RequestSource, on_demand_feature_view
        from tecton.types import Field, Float64, Int64
        import pandas

        # Define the request schema
        transaction_request = RequestSource(schema=[Field("amount", Float64)])

        # Define the output schema
        output_schema = [Field("transaction_amount_is_high", Int64)]

        # This On-Demand Feature View evaluates a transaction amount and declares it as "high", if it's higher than 10,000
        @on_demand_feature_view(
            sources=[transaction_request],
            mode='pandas',
            schema=output_schema,
            owner='matt@tecton.ai',
            tags={'release': 'production', 'prevent-destroy': 'true', 'prevent-recreate': 'true'},
            description='Whether the transaction amount is considered high (over $10000)'
        )
        def transaction_amount_is_high(transaction_request):
            import pandas as pd

            df = pd.DataFrame()
            df['transaction_amount_is_high'] = (transaction_request['amount'] >= 10000).astype('int64')
            return df
    """

    def decorator(feature_view_function):
        return OnDemandFeatureView(
            name=name or feature_view_function.__name__,
            description=description,
            owner=owner,
            tags=tags,
            prevent_destroy=prevent_destroy,
            mode=mode,
            sources=sources,
            schema=schema,
            feature_view_function=feature_view_function,
            environments=environments,
            # Tecton 1.0 parameters.
            features=None,
            context_parameter_name=None,
        )

    return decorator
