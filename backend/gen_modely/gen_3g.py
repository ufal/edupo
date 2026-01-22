import logging

import torch

from unsloth import FastLanguageModel

MODEL = 'TODO:MODEL_PATH'

def load_model(modelspec=None, load16bit=True, model_path=MODEL):

    logging.info(f"Loading model {modelspec} {model_path}")

    kwargs = {}
    if load16bit:
        kwargs['dtype'] = torch.bfloat16
        kwargs['load_in_4bit'] = False
    else:
        kwargs['load_in_4bit'] = True
        logging.info("Loading in 4bit.")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_path,
        **kwargs,
        )
    FastLanguageModel.for_inference(model)

    #logging.info(f"model_3g: {model_path}")
    #logging.info(f"tokenizer_3g: {tokenizer}")

    logging.info("Model loaded: " + modelspec)
    return model, tokenizer, None

def generuj(gen, template, params):

    poem = '<poem>\n<format-v-1/>\n'

    _, generated = gen(poem, max_new=2048)

    poem += generated

    return poem, [], 'Anonym', 'Bez názvu'
