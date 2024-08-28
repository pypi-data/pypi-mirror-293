from langfuse import Langfuse
    
from datetime import datetime
import os




def connect(secret_key=None, public_key=None, host=None):
    """
    Function Overview:

        This function establishes a connection with the trinity platform using the provided credentials.
        Input Parameters:

        Mandatory Parameters:
            secret_key: A string representing the secret key for the trinity platform.
                Example: secret_key = "your_secret_key"
            public_key: A string representing the public key for the trinity platform.
                Example: public_key = "your_public_key"
            host: A string representing the host URL for the trinity platform.
                Example: host = "https://api.trinity.com"

    Important Notes:

        Required Data:
            The secret_key, public_key, and host parameters are mandatory for the function to run.
        
    Example of calling the function with all the input parameters:
    # Input parameters
        secret_key = "your_secret_key"
        public_key = "your_public_key"
        host = "https://api.trinity.com"

    # Function call
        connect(secret_key=secret_key, public_key=public_key, host=host)
    
    ##  Please contact Giggso support team if you face any issue while running this script on local ##
    """
    try:
        if not secret_key or not public_key or not host:
            print("Secret key, public key, and host are required. Please make sure you have provided all the necessary parameters.")
            return
        os.environ["TRINITY_SECRET_KEY"] = secret_key
        os.environ["TRINITY_PUBLIC_KEY"] = public_key
        os.environ["TRINITY_HOST"] = host
        try:
            langfuse = Langfuse(
                secret_key=os.environ.get("TRINITY_SECRET_KEY"),
                public_key=os.environ.get("TRINITY_PUBLIC_KEY"),
                host=os.environ.get("TRINITY_HOST")
            )
            print(f"Connected to Trinity platform with the following credentials: Secret Key: {secret_key}, Public Key: {public_key}, Host: {host}")
        except:
            print("An error occurred while attempting to connect to the Trinity platform. Please ensure that the input credentials are correct.")
            return
        
    except Exception as e:
        print(f"Error occurred: {e}")


def record(experiment_name=None,questions=None, contexts=None, generated_prompts=None, answers=None, ground_truths=None, model_temperature=None, top_k=None, model_name=None, prompt_template=None):
    """
    Function Overview:

        This function evaluates a series of questions using various spans, depending on the availability of input data.
        Input Parameters:

        Mandatory Parameters:
            experiment_name: A string representing the name of the experiment.
                Example: experiment_name = "Experiment_1"
            questions: A list of strings containing the questions to be evaluated.
                Example: questions = ["What is the capital of France?", "Who wrote '1984'?"]
            answers: A list of strings containing the corresponding answers.
                Example: answers = ["Paris", "George Orwell"]

        Optional Parameters:
            contexts: A list of strings providing context for each question.
                Example: contexts = ["Capital cities of European countries", "Famous books and their authors"]
            generated_prompts: A list of strings with prompts generated for each question.
                Example: generated_prompts = ["Tell me about European capitals.", "Discuss authors of classic literature."]
            ground_truths: A list of strings with the correct answers or ground truths.
                Example: ground_truths = ["Paris", "George Orwell"]

        Configuration Parameters:
            model_temperature: A string representing the model temperature.
                Example: model_temperature = "0.3"
            top_k: A string indicating the top-K sampling for the model.
                Example: top_k = "5"
            model_name: A string specifying the model name to be used.
                Example: model_name = "GPT-3"
            prompt_template: A string with the template to be used for prompts.
                Example: prompt_template = "Describe the following topic:"

    Important Notes:

        Required Data:
            The experiment_name, questions, and answers parameters are mandatory for the function to run.
        Enhanced Evaluation:
            Including contexts, ground_truths, and generated_prompts can enhance the evaluation metrics, though they are optional.
        
    Example of calling the function with all the input parameters:
     # Input parameters
        experiment_name = "Experiment_1"
        questions = ["What is the capital of France?", "Who wrote '1984'?"]
        contexts = ["Capital cities of European countries", "Famous books and their authors"]
        generated_prompts = ["Tell me about European capitals.", "Discuss authors of classic literature."]
        answers = ["Paris", "George Orwell"]
        ground_truths = ["Paris", "George Orwell"]
        model_temperature = "0.3"
        top_k = "5"
        model_name = "GPT-3"
        prompt_template = "Describe the following topic:"

    # Function call
        record(
            experiment_name=experiment_name,
            questions=questions,
            contexts=contexts,
            generated_prompts=generated_prompts,
            answers=answers,
            ground_truths=ground_truths,
            model_temperature=model_temperature,
            top_k=top_k,
            model_name=model_name,
            prompt_template=prompt_template
        )
    
    ##  Please contact Giggso support team if you face any issue while running this script on local ##
    """
    try:
        if not experiment_name:
            print("Experiment name is required. Please make sure you have provided all the necessary parameters.")
            return
        if not questions or not answers:
            print("Both 'questions' and 'answers' are required. Please make sure you have provided all the necessary parameters.")
            return

        if not model_name or not top_k or not prompt_template or not model_temperature:
            print("Model parameters (name, top_k, prompt_template, temperature) are required. Please make sure you have provided all the necessary parameters.")
            return
        try:
            langfuse = Langfuse(
                secret_key=os.environ.get("TRINITY_SECRET_KEY"),
                public_key=os.environ.get("TRINITY_PUBLIC_KEY"),
                host=os.environ.get("TRINITY_HOST")
            )
        except Exception as e:
            print("An error occurred while connecting to the Trinity platform. Please ensure that the Trinity environment variables (TRINITY_SECRET_KEY, TRINITY_PUBLIC_KEY, TRINITY_HOST) are set, or test the connectivity using the 'connect' function provided by Trinity.")
            print(f"Error occurred: {e}")
            return

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        trace_name = "Experiment_A"

        trace = langfuse.trace(name=trace_name, metadata={
            "ExperimentName": trace_name,
            "Timestamp": timestamp,
            "ModelTemperature": model_temperature,
            "TopK": top_k,
            "PromptTemplate": prompt_template,
        })

        for question, context, generated_prompt, answer, ground_truth in zip(questions, contexts or [], generated_prompts or [], answers, ground_truths or []):
            if all([question, answer, generated_prompt, context, ground_truth]):
                trace.span(name="Answer Generation", input={"question": question}, output={"answer": answer})
                trace.span(name="Contextual Answer Generation(RETRIEVAR)", input={"question": question, "context": context}, output={"answer": answer})
                trace.span(name="Answer Validation(PERFORMANCE)", input={"question": question}, output={"answer": answer, "ground_truth": ground_truth})
                trace.span(name="Prompt-Based Answer Generation(PROMPT)", input={"question": question, "generated_prompt": generated_prompt}, output={"answer": answer})
                print(
                    "Run recorded successfully with the following details:"
                    + "\n Timestamp: " + timestamp
                    + "\n Record Count: " + str(len(questions))
                    + "\n Model Name: " + model_name
                    + "\n Model Temperature: " + model_temperature
                    + "\n Top K: " + top_k
                    + "\n questions: " + str(len(questions))
                    + "\n contexts: " + str(len(contexts))
                    + "\n generated prompts: " + str(len(generated_prompts))
                    + "\n answers: " + str(len(answers))
                    + "\n ground truths: " + str(len(ground_truths))
                    + "\n Prompt Template: " + prompt_template
                    
                    )

            elif question and answer and context:
                trace.span(name="Contextual Answer Generation", input={"question": question, "context": context}, output={"answer": answer})
                print(
                    "Run recorded successfully with the following details:"
                    + "\n Timestamp: " + timestamp
                    + "\n Record Count: " + str(len(questions))
                    + "\n Model Name: " + model_name
                    + "\n Model Temperature: " + model_temperature
                    + "\n Top K: " + top_k
                    + "\n questions: " + str(len(questions))
                    + "\n contexts: " + str(len(contexts))
                    + "\n generated prompts: " + str(generated_prompts)
                    + "\n answers: " + str(len(answers))
                    + "\n ground truths: " + str(ground_truths)
                    + "\n Prompt Template: " + str(prompt_template)
                    
                    )

            elif question and answer and ground_truth:
                trace.span(name="Answer Validation(RETRIEVAR)", input={"question": question}, output={"answer": answer, "ground_truth": ground_truth})
                print(f"Trace recorded successfully with question: {question}, answer: {answer}, and ground truth: {ground_truth}.")
                print(
                    "Run recorded successfully with the following details:"
                    + "\n Timestamp: " + timestamp
                    + "\n Record Count: " + str(len(questions))
                    + "\n Model Name: " + model_name
                    + "\n Model Temperature: " + model_temperature
                    + "\n Top K: " + top_k
                    + "\n questions: " + str(len(questions))
                    + "\n contexts: " + str(contexts)
                    + "\n generated prompts: " + str(generated_prompts)
                    + "\n answers: " + str(len(answers))
                    + "\n ground truths: " + str(len(ground_truths))
                    + "\n Prompt Template: " + str(prompt_template)
                    
                    )
                
            
            elif question and answer and generated_prompt:
                trace.span(name="Prompt-Based Answer Generation(PERFORMANCE)", input={"question": question, "generated_prompt": generated_prompt}, output={"answer": answer})
                print(f"Trace recorded successfullly with question: {question}, answer: {answer}, and generated prompt: {generated_prompt}.")
                print(
                    "Run recorded successfully with the following details:"
                    + "\n Timestamp: " + timestamp
                    + "\n Record Count: " + str(len(questions))
                    + "\n Model Name: " + model_name
                    + "\n Model Temperature: " + model_temperature
                    + "\n Top K: " + top_k
                    + "\n questions: " + str(len(questions))
                    + "\n contexts: " + str(contexts)
                    + "\n generated prompts: " + str(len(generated_prompts))
                    + "\n answers: " + str(len(answers))
                    + "\n ground truths: " + str(ground_truths)
                    + "\n Prompt Template: " + str(prompt_template)
                    
                    )
            
            
            elif question and answer:
                trace.span(name="Answer Generation(PROMPT)", input={"question": question}, output={"answer": answer})
                print(
                    "Run recorded successfully with the following details:"
                    + "\n Timestamp: " + timestamp
                    + "\n Record Count: " + str(len(questions))
                    + "\n Model Name: " + model_name
                    + "\n Model Temperature: " + model_temperature
                    + "\n Top K: " + top_k
                    + "\n questions: " + str(len(questions))
                    + "\n contexts: " + str(contexts)
                    + "\n generated prompts: " + str(generated_prompts)
                    + "\n answers: " + str(len(answers))
                    + "\n ground truths: " + str(ground_truths)
                    + "\n Prompt Template: " + str(prompt_template)
                    
                    )
                

    except Exception as e:
        print(f"Error occurred: {e}")