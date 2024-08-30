import warnings
from typing import ClassVar, Generic, TypeVar

from llm_taxi.types import NOT_SUPPORTED, NotSupportedOr, SupportedParams

_T = TypeVar("_T")


class Client(Generic[_T]):
    env_vars: ClassVar[dict[str, str]] = {}
    param_mapping: ClassVar[dict[SupportedParams, NotSupportedOr[str]]] = {}

    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        base_url: str | None = None,
        call_kwargs: dict | None = None,
        **client_kwargs,
    ) -> None:
        """Initialize the Client instance.

        Args:
            model (str): The model to be used.
            api_key (str): The API key for authentication.
            base_url (str, optional): The base URL for the API. Defaults to None.
            call_kwargs (dict, optional): Additional keyword arguments for the API call. Defaults to None.
            **client_kwargs: Additional keyword arguments for the client initialization.

        Returns:
            None
        """
        if not call_kwargs:
            call_kwargs = {}

        self._model = model
        self._api_key = api_key
        self._base_url = base_url
        self._call_kwargs = call_kwargs | {"model": self.model}
        self._client = self._init_client(
            api_key=self._api_key,
            base_url=self._base_url,
            **client_kwargs,
        )

    @property
    def model(self) -> str:
        return self._model

    @property
    def client(self) -> _T:
        return self._client

    def _init_client(self, **kwargs) -> _T:
        raise NotImplementedError

    def _get_call_kwargs(self, **kwargs) -> dict:
        kwargs = self._call_kwargs | kwargs

        kept_kwargs = {}
        for key, value in kwargs.items():
            rename = self.param_mapping.get(key)
            if rename == NOT_SUPPORTED:
                warnings.warn(
                    f"Parameter '{key}' is not supported by the API, and will be ignored.",
                    stacklevel=2,
                )
                continue

            kept_kwargs[rename or key] = value

        return kept_kwargs
