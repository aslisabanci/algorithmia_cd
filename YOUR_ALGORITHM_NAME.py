import Algorithmia
import json
import os.path
import joblib

client = Algorithmia.client()


def load_model_config(config_rel_path="model_config.json"):
    """Loads the model manifest file as a dict. 
    A manifest file has the following structure:
    {
      "model_filepath": Uploaded model path on Algorithmia data collection
      "model_md5_hash": MD5 hash of the uploaded model file
      "model_origin_repo": Model development repository having the Github CI workflow
      "model_origin_commit_SHA": Commit SHA related to the trigger of the CI workflow
      "model_origin_commit_msg": Commit message related to the trigger of the CI workflow
      "model_uploaded_utc": UTC timestamp of the automated model upload
    }
    """
    config = []
    config_path = "{}/{}".format(os.getcwd(), (config_rel_path))
    if os.path.exists(config_path):
        with open(config_path) as json_file:
            config = json.load(json_file)
    return config


def load_model(config):
    """Loads the model object from the file at model_filepath key in config dict"""
    model_path = config["model_filepath"]
    model_file = client.file(model_path).getFile().name
    model = joblib.load(model_file)
    return model_file, model


config = load_model_config()
model_file, model = load_model(config)


# API calls will begin at the apply() method, with the request body passed as 'input'
# For more details, see algorithmia.com/developers/algorithm-development/languages
def apply(input):
    print(f"Echoing back input: {input}")


if __name__ == "__main__":
    """
    Remember to create the Algorithmia client object with your API Key when you're testing locally
    So, change the Algorithmia client creation above to:
    client = Algorithmia.client(YOUR_API_KEY)
    But! remember not to commit/push this key for security!
    """

    algo_input = "Simple test input"
    print(f"Calling algorithm apply() func with input: {algo_input}")

    algo_result = apply(algo_input)
    print(algo_result)

