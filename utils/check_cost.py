def check_cost(response, model):
    input_tokens = response.usage.prompt_tokens  # Tokens used for the prompt
    output_tokens = response.usage.completion_tokens  # Tokens used for the completion

    if model == "gpt-4o-mini":
        # Pricing details for GPT-4o-mini
        input_cost_per_million = 0.15  # USD per million input tokens
        output_cost_per_million = 0.60  # USD per million output tokens

    elif model == "gpt-4o":
        # Pricing details for GPT-4-turbo
        input_cost_per_million = 2.5  # USD per million input tokens
        output_cost_per_million = 10  # USD per million output tokens

    elif model == "gpt-4-turbo":
        # Pricing details for GPT-4-turbo
        input_cost_per_million = 10  # USD per million input tokens
        output_cost_per_million = 30  # USD per million output tokens

    # Calculate the cost for input and output tokens
    input_cost = (input_tokens / 1_000_000) * input_cost_per_million
    output_cost = (output_tokens / 1_000_000) * output_cost_per_million
    total_cost = input_cost + output_cost

    return total_cost