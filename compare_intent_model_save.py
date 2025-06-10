from transformers import AutoModelForSequenceClassification, AutoTokenizer

model_name = "facebook/bart-large-mnli"
hf_token   = "sign in to hugging face and use your hugging face apikey"

model = AutoModelForSequenceClassification.from_pretrained(
    model_name, use_auth_token=hf_token
)
tokenizer = AutoTokenizer.from_pretrained(
    model_name, use_auth_token=hf_token
)

save_dir = "./facebook-bart-large-mnli"
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
