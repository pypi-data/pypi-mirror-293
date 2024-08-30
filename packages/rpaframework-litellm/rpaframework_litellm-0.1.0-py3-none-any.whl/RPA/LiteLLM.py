import logging

from typing import Optional, Union

import litellm


class LiteLLM:
    """Library to support `LiteLLM <https://litellm.ai>`_ unified API for LLM services.

    Library is **not** included in the `rpaframework` package, so in order to use it
    you have to add `rpaframework-litellm` with the desired version in your
    *conda.yaml* file.

    **Robot Framework example usage**

    .. code-block:: robotframework

        *** Settings ***
        Library    RPA.Robocorp.Vault
        Library    RPA.LiteLLM

        *** Tasks ***
        Create a text completion
        ${secrets}   Get Secret   secret_name=LiteLLM
        Authorize To LiteLLM
        ...    api_key=${secrets}[api_key]
        ...    api_base=${secrets}[api_base]
        ${completion}    Completion Create
        ...    openai/gpt-4o-mini
        ...    Write a tagline for an ice cream shop
        ...    temperature=0.6
        Log   ${completion}

    **Python example usage**

    .. code-block:: python

        from RPA.Robocorp.Vault import Vault
        from RPA.OpenAI import LiteLLM

        secrets = Vault().get_secret("LiteLLM")
        baselib = LiteLLM()
        baselib.authorize_to_litellm(secrets["api_key"], secrets["api_base"])

        result = baselib.completion_create(
            'openai/gpt-4o-mini',
            'Create a tagline for icecream shop',
            temperature=0.6,
        )
        print(result)
    """  # noqa: E501

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "REST"

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.service_type = "LiteLLM"

    def authorize_to_litellm(
        self,
        api_key: str,
        api_base: str,
    ) -> None:
        """Keyword for authorizing to LiteLLM.

        :param api_key: Your LiteLLM API key
        :param api_base: Your Endpoint URL. Example: https://cloud.litellm.ai/

        Robot Framework example:

        .. code-block:: robotframework

            ${secrets}   Get Secret   secret_name=LiteLLM
            Authorize To LiteLLM
            ...    api_key=${secrets}[api_key]
            ...    api_base=${secrets}[api_base]

        Python example:

        .. code-block:: python

            secrets = Vault().get_secret("LiteLLM")
            baselib = LiteLLM()
            baselib.authorize_to_litellm(
                secrets["api_key"],
                secrets["api_base"],
            )

        """  # noqa: E501
        litellm.api_key = api_key
        litellm.api_base = api_base

    def completion_create(
        self,
        model: str,
        prompt: str,
        # Optional OpenAI params
        timeout: Optional[Union[float, int]] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        stream: Optional[bool] = None,
        stream_options: Optional[dict] = None,
        stop=None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[dict] = None,
        user: Optional[str] = None,
        # openai v1.0+ new params
        response_format: Optional[dict] = None,
        seed: Optional[int] = None,
        tools: Optional[list] = None,
        tool_choice: Optional[str] = None,
        parallel_tool_calls: Optional[bool] = None,
        logprobs: Optional[bool] = None,
        top_logprobs: Optional[int] = None,
        deployment_id=None,
        # soon to be deprecated params by OpenAI
        functions: Optional[list] = None,
        function_call: Optional[str] = None,
        # set api_base, api_version, api_key
        base_url: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None,
        model_list: Optional[list] = None,  # pass in a list of api_base,keys, etc.
        # Optional liteLLM function params
        **kwargs,
    ) -> None:
        """Keyword for creating text completions.
        Keyword returns a text string.

        :param model: the ID of the model to use, e.g. ``text-davinci-003``.
        :param prompt: Text submitted for creating natural language.
        :param temperature: What sampling temperature to use.
            Higher values means the model will take more risks..
        :param max_tokens: The maximum number of tokens to generate in the completion..
        :param top_probability: Controls diversity via nucleus sampling. 0.5 means half
            of all likelihood-weighted options are considered.
        :param frequency_penalty: Number between -2.0 and 2.0. Positive values penalize
            new tokens based on their existing frequency in the text so far.
        :param presence_penalty: Number between -2.0 and 2.0. Positive values penalize
            new tokens based on whether they appear in the text so far.

        Robot Framework example:

        .. code-block:: robotframework

            ${completion}    Completion Create
            ...    openai/gpt-4o-mini
            ...    Write a tagline for an ice cream shop
            ...    temperature=0.6
            Log   ${completion}

        Python example:

        .. code-block:: python

            result = baselib.completion_create(
                'openai/gpt-4o-mini',
                'Create a tagline for icecream shop',
                temperature=0.6,
            )
            print(result)

        """  # noqa: E501
        parameters = locals()
        parameters.update(parameters.pop("kwargs"))
        response = litellm.text_completion(**parameters)
        self.logger.info(response)
        text = response["choices"][0]["text"].strip()
        return text

    def chat_completion_create(
        self,
        model: str,
        user_content: str = None,
        conversation: Optional[list] = None,
        system_content: Optional[str] = None,
        # Optional OpenAI params
        timeout: Optional[Union[float, int]] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        n: Optional[int] = None,
        stream: Optional[bool] = None,
        stream_options: Optional[dict] = None,
        stop=None,
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        logit_bias: Optional[dict] = None,
        user: Optional[str] = None,
        # openai v1.0+ new params
        response_format: Optional[dict] = None,
        seed: Optional[int] = None,
        tools: Optional[list] = None,
        tool_choice: Optional[str] = None,
        parallel_tool_calls: Optional[bool] = None,
        logprobs: Optional[bool] = None,
        top_logprobs: Optional[int] = None,
        deployment_id=None,
        # soon to be deprecated params by OpenAI
        functions: Optional[list] = None,
        function_call: Optional[str] = None,
        # set api_base, api_version, api_key
        base_url: Optional[str] = None,
        api_version: Optional[str] = None,
        api_key: Optional[str] = None,
        model_list: Optional[list] = None,  # pass in a list of api_base,keys, etc.
        # Optional liteLLM function params
        **kwargs,
    ) -> None:
        """Keyword for creating chat completions.
        Keyword returns the response as a string and the message history as a list.

        :param model: the ID of the model to use, e.g. ``openai/text-davinci-003``.
        :param user_content: Text submitted to generate completions.
        :param conversation: List containing the conversation to be continued. Leave
         empty for a new conversation.
        :param system_content: The system message helps set the behavior of
         the assistant.
        :param temperature: What sampling temperature to use between 0 to 2. Higher
         values means the model will take more risks.
        :param top_probability: An alternative to sampling with temperature, called
         nucleus sampling, where the model considers the results of the tokens with
         top_p probability mass.
        :param frequency_penalty: Number between -2.0 and 2.0. Positive values penalize
         new tokens based on their existing frequency in the text so far.
        :param presence_penalty: Number between -2.0 and 2.0. Positive values penalize
         new tokens based on whether they appear in the text so far.

        Robot Framework example:

        .. code-block:: robotframework

            # Get response without conversation history.
            ${response}   @{llm_conversation}=     Chat Completion Create
            ...    openai/gpt-4o-mini
            ...    user_content=What is the biggest mammal?
            VAR    @{llm_conversation}    @{llm_conversation}    scope=SUITE
            Log    ${response}
            Log    ${llm_conversation}

            # Continue the conversation by using the "conversation" argument.
            ${response}    @{llm_conversation}=    Chat Completion Create
            ...    openai/gpt-4o-mini
            ...    conversation=@{llm_conversation}
            ...    user_content=How old can it live?
            Log    ${response}
            Log    ${llm_conversation}
        """
        parameters = locals()
        parameters.update(parameters.pop("kwargs"))
        messages = parameters.pop("conversation") or []
        if system_content := parameters.pop("system_content", None):
            messages.append(
                {"role": "system", "content": system_content},
            )
        messages.append(
            {"role": "user", "content": parameters.pop("user_content")},
        )
        response = litellm.completion(messages=messages, **parameters)
        self.logger.info(response)
        text = response["choices"][0]["message"]["content"]
        messages.append(
            {"role": "assistant", "content": text},
        )
        return_list = [text, *messages]
        self.logger.info(return_list)
        return return_list
