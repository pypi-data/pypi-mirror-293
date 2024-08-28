import typing as t

from llama_cpp import Llama
from openai import OpenAI
from ..desc.template import FN_TEMPLATE
from ..desc.func_desc import FN_DESC
import json
# import traceback


def chat_oai_stream(
    base_url="http://127.0.0.1:8000/v1",
    api_key="dummy_key",
    model="default_model",
    prompt="Who are you?",
    *args,
    **kwargs
):
    """Chat with OpenAI's GPT-3 model using the specified parameters.

    Args:
        base_url (str): The base URL for the OpenAI API. Default is "http://127.0.0.1:8000/v1".
        api_key (str): The API key for accessing the OpenAI API. Default is "dummy_key".
        model (str): The model ID to use for the chat. Default is "/data/models/Qwen-7B-Chat-Int4".
        prompt (str): The initial prompt for the chat conversation.

    Yields:
        str: The generated content from the chat conversation.

    """
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=True,
        *args,
        **kwargs
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        yield content


def chat_oai_invoke(
    base_url="http://127.0.0.1:8000/v1",
    api_key="dummy_key",
    model="default_model",
    prompt="Who are you?",
    *args,
    **kwargs
):
    """Invoke OpenAI chat API to generate a response based on the given prompt.

    Args:
        base_url (str): The base URL of the OpenAI API. Default is "http://127.0.0.1:8000/v1".
        api_key (str): The API key for accessing the OpenAI API. Default is "dummy_key".
        model (str): The model to use for generating the response. Default is "/data/models/Qwen-7B-Chat-Int4".
        prompt (str): The prompt message to start the conversation. Default is "Who are you?".

    Returns:
        str: The response generated by the OpenAI chat API based on the prompt.
    """
    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        stream=False,
        *args,
        **kwargs
    )

    return response.choices[0].message.content


class GGUF_M(Llama):
    def __init__(
        self,
        model_path :str,
        device: str='gpu',
        generation_kwargs: dict = {},
        server_ip: str = "127.0.0.1",
        server_port: int = 8000,
        *args,
        **kwargs
    ):
        """Initialize the model with the specified parameters.

        Args:
            model_path (str): The path to the model.
            device (str, optional): The device to use, either 'gpu' or 'cpu'. Defaults to 'gpu'.
            generation_kwargs (dict, optional): Additional generation keyword arguments. Defaults to {}.
            server_ip (str, optional): The IP address of the server. Defaults to "127.0.0.1".
            server_port (int, optional): The port of the server. Defaults to 8000.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            KeyError: If 'num_threads' or 'max_context_length' is missing in generation_kwargs.
        """
        print("正在从本地加载模型...")
        if device.lower() == 'cpu':
            super().__init__(
                model_path=model_path,
                n_threads=generation_kwargs['num_threads'],
                n_ctx=generation_kwargs['max_context_length'],
                *args,
                **kwargs
            )
        else:
            super().__init__(
                model_path=model_path,
                n_threads=generation_kwargs['num_threads'],
                n_ctx=generation_kwargs['max_context_length'],
                n_gpu_layers=-1,
                flash_attn=True,
                *args,
                **kwargs
            )
        self.generation_kwargs = generation_kwargs

    def invoke(
        self,
        prompt : str,
        stop: list[str] | None = ["USER:", "ASSISTANT:"],
        # history: list = [],
        **kwargs: t.Any,
    ) -> str:
        """Invoke the model to generate a response based on the given prompt.

        Args:
            prompt (str): The prompt to be used for generating the response.
            stop (list[str], optional): List of strings that indicate when the model should stop generating the response. Defaults to ["USER:", "ASSISTANT:"].
            **kwargs: Additional keyword arguments to be passed to the model.

        Returns:
            str: The generated response based on the prompt.
        """
        prompt_final = f"USER:\n{prompt}\nASSISTANT:\n"

        result = self.create_completion(
            prompt_final,
            repeat_penalty=self.generation_kwargs["repetition_penalty"],
            max_tokens=self.generation_kwargs["max_new_tokens"],
            stop=stop,
            echo=False,
            temperature=self.generation_kwargs["temperature"],
            mirostat_mode = 2,
            mirostat_tau=4.0,
            mirostat_eta=1.1
        )
        resp = result['choices'][0]['text']
        # history.append(
        #     [prompt, resp]
        # )
        return resp

    def stream(
        self,
        prompt: str,
        stop: list[str] | None = ["USER:", "ASSISTANT:"],
        # history: list = [],
        **kwargs: t.Any,
    ):
        """Generate text responses based on the given prompt using the model.

        Args:
            prompt (str): The prompt to generate text responses.
            stop (list[str], optional): List of strings to stop the generation. Defaults to ["USER:", "ASSISTANT:"].
            **kwargs: Additional keyword arguments for the model.

        Yields:
            str: Text responses generated by the model based on the prompt.
        """
        prompt = f"USER:\n{prompt}\nASSISTANT:\n"
        output = self.create_completion(
            prompt,
            stream=True,
            repeat_penalty=self.generation_kwargs["repetition_penalty"],
            max_tokens=self.generation_kwargs["max_new_tokens"],
            stop=stop,
            echo=False,
            temperature=self.generation_kwargs["temperature"],
            mirostat_mode = 2,
            mirostat_tau=4.0,
            mirostat_eta=1.1
        )
        # history.append([])
        for chunk in output:
            item = chunk['choices'][0]['text']
            # self.resps[-1].append(item)
            yield chunk['choices'][0]['text']
        # self.resps[-1] = "".join(self.resps[-1])


# class GGUF_M():
#     def __init__(
#         self,
#         model_path :str,
#         device: str='gpu',
#         generation_kwargs: dict = {},
#         server_ip: str = "127.0.0.1",
#         server_port: int = 8000,
#     ):
#         """Initialize the model with the provided model path and optional parameters.

#         Args:
#             model_path (str): The path to the model.
#             device (str, optional): The device to use for model initialization. Defaults to 'gpu'.
#             generation_kwargs (dict, optional): Additional keyword arguments for model generation. Defaults to {}.
#             server_ip (str, optional): The IP address of the server. Defaults to "127.0.0.1".
#             server_port (int, optional): The port of the server. Defaults to 8000.
#         """
#         # 从本地初始化模型
#         # super().__init__()
#         self.generation_kwargs = generation_kwargs
#         print("正在从本地加载模型...")
#         if device == 'cpu':
#             self.model = Llama(
#                 model_path=model_path,
#                 n_threads=self.generation_kwargs['num_threads'],
#                 n_ctx=self.generation_kwargs['max_context_length'],
#             )
#         else:
#             self.model = Llama(
#                 model_path=model_path,
#                 n_threads=self.generation_kwargs['num_threads'],
#                 n_ctx=self.generation_kwargs['max_context_length'],
#                 n_gpu_layers=-1,
#                 flash_attn=True
#             )

#         print("完成本地模型的加载")

#     def invoke(
#         self,
#         prompt : str,
#         stop: list[str] | None = ["USER:", "ASSISTANT:"],
#         # history: list = [],
#         **kwargs: t.Any,
#     ) -> str:
#         """Invoke the model to generate a response based on the given prompt.

#         Args:
#             prompt (str): The prompt to be used for generating the response.
#             stop (list[str], optional): List of strings that indicate when the model should stop generating the response. Defaults to ["USER:", "ASSISTANT:"].
#             **kwargs: Additional keyword arguments to be passed to the model.

#         Returns:
#             str: The generated response based on the prompt.
#         """
#         prompt_final = f"USER:\n{prompt}\nASSISTANT:\n"

#         result = self.model.create_completion(
#             prompt_final,
#             repeat_penalty=self.generation_kwargs["repetition_penalty"],
#             max_tokens=self.generation_kwargs["max_new_tokens"],
#             stop=stop,
#             echo=False,
#             temperature=self.generation_kwargs["temperature"],
#             mirostat_mode = 2,
#             mirostat_tau=4.0,
#             mirostat_eta=1.1
#         )
#         resp = result['choices'][0]['text']
#         # history.append(
#         #     [prompt, resp]
#         # )
#         return resp

#     def stream(
#         self,
#         prompt: str,
#         stop: list[str] | None = ["USER:", "ASSISTANT:"],
#         # history: list = [],
#         **kwargs: t.Any,
#     ):
#         """Generate text responses based on the given prompt using the model.

#         Args:
#             prompt (str): The prompt to generate text responses.
#             stop (list[str], optional): List of strings to stop the generation. Defaults to ["USER:", "ASSISTANT:"].
#             **kwargs: Additional keyword arguments for the model.

#         Yields:
#             str: Text responses generated by the model based on the prompt.
#         """
#         prompt = f"USER:\n{prompt}\nASSISTANT:\n"
#         output = self.model.create_completion(
#             prompt,
#             stream=True,
#             repeat_penalty=self.generation_kwargs["repetition_penalty"],
#             max_tokens=self.generation_kwargs["max_new_tokens"],
#             stop=stop,
#             echo=False,
#             temperature=self.generation_kwargs["temperature"],
#             mirostat_mode = 2,
#             mirostat_tau=4.0,
#             mirostat_eta=1.1
#         )
#         # history.append([])
#         for chunk in output:
#             item = chunk['choices'][0]['text']
#             # self.resps[-1].append(item)
#             yield chunk['choices'][0]['text']
#         # self.resps[-1] = "".join(self.resps[-1])


class OpenAI_M():
    def __init__(
        self,
        model_path: str = "default_model",
        device: str='gpu',
        generation_kwargs: dict = {},
        server_ip: str = "172.28.1.2",
        server_port: int = 8000,
        api_key: str = "dummy_key",
        tools: list = None,
        tool_desc: dict = None,
        *args,
        **kwargs
    ):
        """Initialize the OpenAI client with the specified parameters.

        Args:
            model_path (str): Path to the model (default is "default_model").
            device (str): Device to use (default is 'gpu').
            generation_kwargs (dict): Additional generation arguments (default is an empty dictionary).
            server_ip (str): IP address of the server (default is "172.28.1.2").
            server_port (int): Port of the server (default is 8000).
            api_key (str): API key for authentication (default is "dummy_key").
            tools (list): List of tools.
            tool_desc (dict): Description of tools.

        Raises:
            ValueError: If an invalid argument is provided.
        """
        # self.model_path = model_path
        self.server_ip = server_ip
        self.server_port = server_port
        self.base_url = f"http://{self.server_ip}:{str(self.server_port)}/v1"
        self.api_key = api_key
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            *args,
            **kwargs
        )
        self.tools = tools
        self.tool_desc = FN_DESC
        if tool_desc is not None:
            self.tool_desc = self.tool_desc | tool_desc

    def invoke(
        self,
        prompt : str,
        stop: list[str] | None = ["USER:", "ASSISTANT:"],
        # history: list = [],
        model="default_model",
        **kwargs: t.Any,
    ) -> str:
        """Invoke the chatbot with the given prompt and return the response.

        Args:
            prompt (str): The prompt to provide to the chatbot.
            stop (list[str], optional): List of strings that indicate the end of the conversation. Defaults to ["USER:", "ASSISTANT:"].
            **kwargs: Additional keyword arguments to pass to the chatbot.

        Returns:
            str: The response generated by the chatbot.
        """
        response = self.client.chat.completions.create(
            # model=self.model_path,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            stream=False,
            model=model,
            # model=kwargs.get("model", "default_model")
            **kwargs
        )
        return response.choices[0].message.content

    def stream(
        self,
        prompt : str,
        stop: list[str] | None = ["USER:", "ASSISTANT:"],
        # history: list = [],
        model="default_model",
        **kwargs: t.Any,
    ):
        """Generate text completion in a streaming fashion.

        Args:
            prompt (str): The text prompt to generate completion for.
            stop (list[str], optional): List of strings to stop streaming at. Defaults to ["USER:", "ASSISTANT:"].
            **kwargs: Additional keyword arguments to pass to the completion API.

        Yields:
            str: The generated text completion in a streaming fashion.
        """
        response = self.client.chat.completions.create(
            # model=self.model_path,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            stream=True,
            model=model,
            # model=kwargs.get("model", "default_model")
            **kwargs
        )

        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    def get_decision(
        self,
        prompt: str,
        **kwargs: t.Any
    ):
        prompt_final = FN_TEMPLATE
        for tool in self.tools:
            prompt_final += self.tool_desc.get(tool.__name__, "")
        prompt_final += f"\n用户的问题：\n{prompt}"
        # print(prompt_final)
        decision_dict = self.invoke(prompt_final ,**kwargs)
        print(decision_dict)
        return json.loads(decision_dict)

    def get_tool_result(
        self,
        prompt: str,
        **kwargs: t.Any
    ):
        decision_dict = self.get_decision(prompt, **kwargs)
        if decision_dict.get("function_name", None) is None:
            return ""
        else:
            func_name = decision_dict.get("function_name")
            for tool in self.tools:
                if tool.__name__ == func_name:
                    tool_final = tool
            func_kwargs = decision_dict.get("params")
            return tool_final(**func_kwargs)


    def agent_response(
        self,
        prompt : str,
        stream = True,
        **kwargs: t.Any
    ):

        decision_dict = self.get_decision(prompt, **kwargs)
        if decision_dict.get("function_name", None) is None:
            return self.stream(prompt, **kwargs)
        else:
            tool_result = str(self.get_tool_result(prompt, **kwargs))
            prompt_final = "根据上下文回答最后的用户问题：\n上下文信息：\n"
            prompt_final += tool_result
            prompt_final += f"\n用户的问题：\n{prompt}"
            if stream:
                return self.stream(prompt_final, **kwargs)
            else:
                return self.invoke(prompt_final, **kwargs)
