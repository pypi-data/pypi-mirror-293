import re

def extract_tamil_sentences(input_text):
    tamil_sentence_pattern = re.compile(r'[\u0B80-\u0BFF]+(?:\s+[\u0B80-\u0BFF]+)*[.,!?:;]?')
    tamil_sentences = tamil_sentence_pattern.findall(input_text)
    extracted_text = ' '.join(sentence.strip() for sentence in tamil_sentences if sentence.strip())
    return extracted_text