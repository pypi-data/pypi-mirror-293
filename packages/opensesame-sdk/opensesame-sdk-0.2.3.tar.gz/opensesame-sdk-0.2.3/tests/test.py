from opensesame import OpenSesame_openai
from opensesame import OpenSesame_gemini
from opensesame import OpenSesame_anthropic 
from opensesame import OpenSesame_groq
from opensesame import OpenSesame_huggingface
from opensesame import OpenSesame_cohere 
# openai test
def test_openai() :
    client = OpenSesame_openai({
        'api_key': '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',
        'open_sesame_key': '6def3c47-847e-428d-a7bd-899da351a19c',
        'project_name': 'test1',  # Make sure this is correct
        'ground_truth': 'hi',
        'context': 'hello'
    })

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role" : "system", "content" : "OpenAI system"},{"role": "user", "content": "what is your name ?"}]
        )
        print("*********")
        print(completion)
    except Exception as e:
        print(f"An error occurred: {e}")

# gemini test
def test_gemini() :
    client = OpenSesame_gemini({
        "api_key" : "AIzaSyAeCyuUxv7n6ngMwRZdQCDNOt-Tu9-DIpo",
        "open_sesame_key" : '6def3c47-847e-428d-a7bd-899da351a19c',
        'project_name': 'test1',  # Make sure this is correct
        'ground_truth': 'hi',
        'context': 'hello'
    })

    try :
        response = client.GenerativeModel(model_name="gemini-1.5-pro").generate_content(prompt="gemini")
        print(response)
    except Exception as e:
        print(f"An error occured {e}")

def test_anthropic() :
    client = OpenSesame_anthropic({
    'api_key': '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',
    'open_sesame_key': '6def3c47-847e-428d-a7bd-899da351a19c',
    'project_name': 'test1',
    'ground_truth': 'idk',
    'context': 'Hi'
    })

    message = client.Messages(client).create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system="claude system",
        messages=[
            {"role": "user", "content": "What is your name"}
        ]
    )
    print(message)

def test_groq() :
    client = OpenSesame_groq({
    'api_key': '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',
    'open_sesame_key': '6def3c47-847e-428d-a7bd-899da351a19c',
    'project_name': 'test1',
    'ground_truth': 'No idea',
    'context': 'Math'
    })
    
    result = client.ChatCompletions(client).create(
        model="llama3-8b-8192",
        messages=[
            {"role" : "system", "content" : "groq system"},
            {"role": "user", "content": "What is your name ?"}
        ]
    )

    print(result)

def test_hf() :
    client = OpenSesame_huggingface({
    "hf_api_token":"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",
    "open_sesame_key":'6def3c47-847e-428d-a7bd-899da351a19c',
    "project_name":'test1',
    "ground_truth":"idk",
    "context":"slim shady"
    })   

    result = client.generate_text(
        model_name="gpt2",
        prompt="Whats up"
    )

    print(f"********** This is the result ***************** {result}")

def test_cohere() :
    co = OpenSesame_cohere({
        'cohere_api_key': 'brE5c46Ac6AmfAO2kxo1wQUUQUMv3oGIxJBKsiyS',
        'open_sesame_key': '6def3c47-847e-428d-a7bd-899da351a19c',
        'project_name': 'test1',
        'ground_truth': 'i dont know',
        'context': 'science'
    })

    result = co.chat(
        message = "What is your name ?",
        preamble = "preamble"
    )

    print(result)


test_anthropic()










