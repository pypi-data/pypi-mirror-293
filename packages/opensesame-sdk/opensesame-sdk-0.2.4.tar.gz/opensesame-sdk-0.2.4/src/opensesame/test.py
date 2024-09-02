from opensesame import OpenSesame_openai
from opensesame import OpenSesame_gemini
from opensesame import OpenSesame_anthropic 
from opensesame import OpenSesame_groq
from opensesame import OpenSesame_huggingface
from opensesame import OpenSesame_cohere 
from opensesame import OpenSesame_azure_openai
# openai test
def test_openai() :
    client = OpenSesame_openai({
        'api_key': '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',
        'open_sesame_key': '6def3c47-847e-428d-a7bd-899da351a19c',
        'project_name': 'proj1',  # Make sure this is correct
    })

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role" : "system", "content" : "You are a scientist"},{"role": "user", "content": "Explain nuclear fission in simple steps"}]
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
        'project_name': 'proj1'
    })

    try :
        response = client.GenerativeModel(model_name="gemini-1.5-pro").generate_content(prompt="Who holds the record for the longest recorded swim")
        print(response)
    except Exception as e:
        print(f"An error occured {e}")

def test_anthropic() :
    client = OpenSesame_anthropic({
    'api_key': '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',
    'open_sesame_key': '6def3c47-847e-428d-a7bd-899da351a19c',
    'project_name': 'proj1'
    })

    message = client.Messages(client).create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system="You are an honest and helpful assistant",
        messages=[
            {"role": "user", "content": "How does a GPU work"}
        ]
    )
    print(message)

def test_groq() :
    client = OpenSesame_groq({
    'api_key': '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',
    'open_sesame_key': '6def3c47-847e-428d-a7bd-899da351a19c',
    'project_name': 'proj1'
    })
    
    result = client.ChatCompletions(client).create(
        model="llama3-8b-8192",
        messages=[
            {"role" : "system", "content" : "You are an honest and helpful assistant"},
            {"role": "user", "content": "Who build the llama language models ?"}
        ]
    )

    print(result)

def test_hf() :
    client = OpenSesame_huggingface({
    "hf_api_token":"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",
    "open_sesame_key":'6def3c47-847e-428d-a7bd-899da351a19c',
    "project_name" : 'proj1'
    })   

    result = client.generate_text(
        model_name="gpt2",
        prompt="What is gpt2"
    )

    print(f"********** This is the result ***************** {result}")

def test_cohere() :
    co = OpenSesame_cohere({
        'cohere_api_key': 'brE5c46Ac6AmfAO2kxo1wQUUQUMv3oGIxJBKsiyS',
        'open_sesame_key': '6def3c47-847e-428d-a7bd-899da351a19c',
        'project_name': 'proj1'
    })

    result = co.chat(
        message = "Who invented chocolate ?",
        preamble = "You are an honest and helpful assistant"
    )

    print(result)

def test_os() :
    from opensesame import OpenSesame 

    os = OpenSesame(
        open_sesame_key = "6def3c47-847e-428d-a7bd-899da351a19c",
        project_name = "proj1"
    )

    response = os.evaluate(prompt="The user prompt", answer="The LLM response")

def test_azure() :
    endpoint="https://openai-tester-1212.openai.azure.com/"
    deployment="gpt3-5"
    api_key="1d92798df728469ca6a324a2fe809d31"
    api_version="2024-06-01"
    config = {
    'api_key': api_key,
    'azure_endpoint': endpoint,
    'deployment': deployment,
    'api_version' : api_version,
    'open_sesame_key': "6def3c47-847e-428d-a7bd-899da351a19c",
    'project_name': 'proj1'
    }   

    client = OpenSesame_azure_openai(config)
    response = client.call(
        prompt='What is japans population decline rate'
    )

    print(response)

test_azure()









