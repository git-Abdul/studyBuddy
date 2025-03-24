from transformers import GPT2LMHeadModel, GPT2TokenizerFast

model = GPT2LMHeadModel.from_pretrained('gpt2')
tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')

prompt = input("Enter your prompt: ")
input_ids = tokenizer(prompt, return_tensors='pt').input_ids
gen_tokens = model.generate(input_ids, do_sample=True, temperature=1.0, max_length=len(input_ids[0]) + 50)
gen_text = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True)[0]

print(gen_text)
