from dataclasses import dataclass, field, replace
from enum import Enum
from math import factorial
from typing import Any

class ResourceType(str, Enum):
    use_case = "use_case"
    adapter = "adapter"
    path = "path"
    infrastructure = "infrastructure"
    data = "data"


@dataclass(frozen=True)
class Dependencies:
    factory: dict[Any, Any] = field(default_factory=dict)

    def feed(self, resource_type: ResourceType, resource: Any, factory: Any) -> 'Dependencies':
        return self._feed(resource_type=resource_type, resource=resource, factory=factory)

    def feed_use_case(self, use_case: Any, use_case_factory: Any) -> 'Dependencies':
        return self._feed(resource_type=ResourceType.use_case, resource=use_case, factory=use_case_factory)

    def feed_adapter(self, port: Any, adapter_factory: Any) -> 'Dependencies':
        return self._feed(resource_type=ResourceType.adapter, resource=port, factory=adapter_factory)

    def feed_path(self, path: str, factory) -> 'Dependencies':
        return self._feed(resource_type=ResourceType.path, resource=path, factory=factory)

    def feed_infrastructure(self, infrastructure: Any, factory):
        return self._feed(resource_type=ResourceType.infrastructure, resource=infrastructure, factory=factory)

    def feed_data(self, data_name: str, value: Any):
        return self._feed(resource_type=ResourceType.data, resource=data_name, factory=lambda _: value)

    def _feed(self, resource_type: ResourceType, resource: Any, factory: Any) -> 'Dependencies':
        return replace(self, factory={**self.factory, (resource_type, resource): factory})

    def get_use_case(self, use_case: Any) -> Any:
        return self._get_resource(resource_type=ResourceType.use_case, resource=use_case)

    def get_query(self, query: Any) -> Any:
        return self.get_use_case(query)

    def get_infrastructure(self, infrastructure) -> Any:
        resource = self._get_resource(resource_type=ResourceType.infrastructure, resource=infrastructure)
        return resource

    def get_adapter(self, adapter: Any) -> Any:
        resource = self._get_resource(resource_type=ResourceType.adapter, resource=adapter)
        return resource

    def get_path(self, path_name: str) -> Any:
        return self._get_resource(resource_type=ResourceType.path, resource=path_name)

    def get_data(self, data_name) -> Any:
        return self._get_resource(resource_type=ResourceType.data, resource=data_name)

    def _get_resource(self, resource_type: ResourceType, resource) -> Any:
        if (resource_type, resource) not in self.factory:
            raise Exception(f"{resource_type.value} for {resource} must be injected first")
        return self.factory[(resource_type, resource)](self)

    @classmethod
    def create_empty(cls) -> 'Dependencies':
        return Dependencies()

    def describe(self) -> str:
        def format_item(key):
            (resource_type, resource_name) = key
            resource = self._get_resource(resource_type, resource_name)
            return f"{resource_name}: {resource_type} => {str(type(resource))}"

        return "\n".join([format_item(key) for key in self.factory.keys()])
