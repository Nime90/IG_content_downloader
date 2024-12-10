def assign_aida_category(frames_description,model="gpt-4o-mini"):
    from openai import OpenAI
    from utils.check_cost import check_cost
    from dotenv import load_dotenv
    from utils.aida_cta_definitions import text
    import os
    load_dotenv('.env')
    #post categories
    type_description = text
    #Step5: analyze the video and assign a category
    prompt_video = "Given this 33 definitions of CTAs: " + type_description + '''Please evaluate this Social media content summary and fit it in only one of the 33 types.
    In making your choice, please pay attention at the summaries of the descriptions of the images, Caption, Post Type and Post Format
    it is extremely important that you only answer in the following dictionary format. Do not add or subtract anything to your answer: 
    {
    "CTA name": "[the most appropriate cta among the 33 types (e.g. '32. Coaching Philosophy CTA')]",
    "CTA category accuracy": "[How accure you think your choice is (please express the value in %)]",
    "CTA category explanation": "[Please explain the reasoning for this choice]",
    "CTA improvement": "[please explain how the Content could improve to get closer to the perfect selected CTA as described before ]
    }

    '''

    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)
    message='Content description: '+frames_description
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_video},  # Keep the text prompt as it is
                    {"type": "text", "text": message}  # Include any additional text instead of an image
                ]
            }
        ],
        temperature=0,
    )
    cost = check_cost(response, model)
    return response.choices[0].message.content, cost