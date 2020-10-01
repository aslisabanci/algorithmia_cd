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
    try:
        if __name__ == "__main__":
            # Loading the model file as usual, since we're working with the local model file in this template
            return joblib.load(model_path)
            # However, you can still load a model from an Algorithmia data collection if you initialize Algorithmia client with your API key.
        else:
            return joblib.load(client.file(model_path).getFile().name)
    except Exception as e:
        print("Exception occurred while loading the model file: {}".format(e))
        return None


config = load_model_config()
model = load_model(config)


# API calls will begin at the apply() method, with the request body passed as 'input'
# For more details, see algorithmia.com/developers/algorithm-development/languages
def apply(input):
    # You can use your model object here
    return f"Echoing back input: {input}"


if __name__ == "__main__":
    # Now the apply() function will be able to access the locally loaded model
    algo_result = apply("Test input")
    print(algo_result)

