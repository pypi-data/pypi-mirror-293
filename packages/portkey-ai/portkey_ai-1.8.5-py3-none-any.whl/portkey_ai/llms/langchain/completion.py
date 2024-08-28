from __future__ import annotations
from portkey_ai import Portkey

import logging
from typing import Any, Iterator, List, Mapping, Optional, Union

try:
    from langchain.callbacks.manager import CallbackManagerForLLMRun
    from langchain.llms.base import LLM
    from langchain.pydantic_v1 import Field, PrivateAttr
    from langchain.schema.output import GenerationChunk
except ImportError as exc:
    raise Exception(
        "Langchain is not installed.Please install it with `pip install langchain`."
    ) from exc


logger = logging.getLogger(__name__)


class PortkeyLLM(LLM):
    """Portkey Service models
    To use, you should have the ``portkey-ai`` python package installed, and the
    environment variable ``PORTKEY_API_KEY``, set with your API key, or pass
    it as a named parameter to the `Portkey` constructor.
    NOTE: You can install portkey using ``pip install portkey-ai``
    Example:
        .. code-block:: python
            import portkey
            from langchain.llms import Portkey
            # Simplest invocation for an openai provider. Can be extended to
            # others as well
            llm_option = portkey.LLMOptions(
                provider="openai",
                # Checkout the docs for the virtual-api-key
                virtual_key="openai-virtual-key",
                model="text-davinci-003"
            )
            # Initialise the client
            client = Portkey(
                api_key="PORTKEY_API_KEY",
                mode="single"
            ).add_llms(llm_params=llm_option)
            response = client("What are the biggest risks facing humanity?")
    """

    model: Optional[str] = Field(default="gpt-3.5-turbo")
    _client: Any = PrivateAttr()

    api_key: Optional[str] = None
    base_url: Optional[str] = None
    virtual_key: Optional[str] = None
    config: Optional[Union[Mapping, str]] = None
    provider: Optional[str] = None
    trace_id: Optional[str] = None
    custom_metadata: Optional[str] = None
    streaming: bool = False

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        virtual_key: Optional[str] = None,
        config: Optional[Union[Mapping, str]] = None,
        provider: Optional[str] = None,
        trace_id: Optional[str] = None,
        custom_metadata: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__()

        self._client = Portkey(
            api_key=api_key,
            base_url=base_url,
            virtual_key=virtual_key,
            config=config,
            provider=provider,
            trace_id=trace_id,
            metadata=custom_metadata,
            **kwargs,
        )
        self.model = None

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call Portkey's completions endpoint.
        Args:
            prompt: The prompt to pass into the model.
            stop: Optional list of stop words to use when generating.
        Returns:
            The string generated by the provider set in the initialisation of the LLM.
        Example:
            .. code-block:: python
                response = portkey("Tell me a joke.")
        """
        response = self._client.completions.create(
            prompt=prompt, stream=False, stop=stop, **kwargs
        )
        text = response.choices[0].text
        return text or ""

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Call Portkey completion_stream and return the resulting generator.
        Args:
            prompt: The prompt to pass into the model.
            stop: Optional list of stop words to use when generating.
        Returns:
            A generator representing the stream of tokens from Portkey.
        Example:
            .. code-block:: python
                prompt = "Write a poem about a stream."
                generator = portkey.stream(prompt)
                for token in generator:
                    yield token
        """
        response = self._client.completions.create(
            stream=True, prompt=prompt, stop=stop, **kwargs
        )
        for token in response:
            chunk = GenerationChunk(text=token.choices[0].text or "")
            yield chunk
            if run_manager:
                run_manager.on_llm_new_token(chunk.text, chunk=chunk)

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "portkey-ai-gateway"
