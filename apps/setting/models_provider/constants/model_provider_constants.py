# coding=utf-8
"""
    @project: AIFun
    @Author：JackyFan
    @file： model_provider_constants.py
    @date：2024/04/17
    @desc: Model Enum
"""
from enum import Enum

from setting.models_provider.impl.openai_model_provider.openai_model_provider import OpenAIModelProvider
# from setting.models_provider.impl.wenxin_model_provider.wenxin_model_provider import WenxinModelProvider
# from setting.models_provider.impl.azure_model_provider.azure_model_provider import AzureModelProvider
# from setting.models_provider.impl.ollama_model_provider.ollama_model_provider import OllamaModelProvider
class ModelProvideConstants(Enum):
    model_openai_provider = OpenAIModelProvider()
    # model_azure_provider = AzureModelProvider()
    # model_wenxin_provider = WenxinModelProvider()
    # model_ollama_provider = OllamaModelProvider()
