# Azure OpenAI Setup

This codebase supports both OpenAI and Azure OpenAI. The system automatically detects which service to use based on environment variables.

## Using OpenAI (Default)

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

## Using Azure OpenAI

To use Azure OpenAI instead, set these environment variables:

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-azure-api-key"
export AZURE_OPENAI_API_VERSION="2024-02-01"  # Optional, defaults to 2024-02-01
```

## Model Configuration

When using Azure OpenAI, ensure your model deployments match the model names used in the code. The default model is `gpt-4o-mini`, but you can specify different models when creating enrichers.

For example, if you've deployed GPT-4 as "gpt-4-deployment" in Azure, you can use:

```python
from cheat_at_search.agent.enrich import create_cached_enricher

enricher = create_cached_enricher(
    cls=YourModel,
    model="gpt-4-deployment",  # Your Azure deployment name
    system_prompt="Your system prompt"
)
```

## Automatic Detection

The system automatically detects which service to use:
- If `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` are set → Uses Azure OpenAI
- Otherwise → Uses OpenAI

## Merging Upstream Changes

This implementation is designed to be maintainable when pulling changes from upstream:

1. The original `OpenAIEnricher` class remains unchanged
2. New `AzureOpenAIEnricher` class is added alongside it
3. Factory functions choose the appropriate implementation
4. Most existing code uses the factory functions, making it compatible with both services

To update existing code that directly uses `OpenAIEnricher`:

```python
# Old code:
from cheat_at_search.agent.enrich import CachedEnricher, OpenAIEnricher
enricher = CachedEnricher(OpenAIEnricher(cls=YourModel, model="gpt-4o-mini", system_prompt="..."))

# New code:
from cheat_at_search.agent.enrich import create_cached_enricher
enricher = create_cached_enricher(cls=YourModel, model="gpt-4o-mini", system_prompt="...")
```

This approach ensures that when you pull new changes from the instructor's repository, you only need to update any new files that directly instantiate `OpenAIEnricher` to use the factory function instead. 