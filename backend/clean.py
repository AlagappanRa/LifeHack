import json
import pickle
import re

import pandas as pd
import preprocessor as p
import spacy
from tqdm import tqdm

nlp = spacy.load("en_core_web_sm")

def clean(text: str) -> str:
    p.set_options(
        p.OPT.URL,
        p.OPT.MENTION,
        p.OPT.HASHTAG,
        p.OPT.RESERVED,
        p.OPT.EMOJI,
        p.OPT.SMILEY,
    )
    text = re.sub(r"\n", " ", text)
    text = p.clean(text)
    return text


def spacify(texts: pd.Series) -> pd.Series:
    return pd.Series(tqdm(nlp.pipe(texts), total=len(texts)))


def extract_entities(doc) -> list[tuple[str, str]]:
    entities = [(ent.lemma_.lower(), ent.label_) for ent in doc.ents]
    return entities


def main():

    # Load JSON data with UTF-8 encoding
    with open("backend/content_dataset.json", "r", encoding="utf-8-sig") as file:
        data = json.load(file)

    # Convert JSON data to DataFrame
    df = pd.DataFrame(data)

    # Apply preprocessing to the text column
    df["cleaned_text"] = df["text"].apply(clean)

    print("Starting spacy")
    df["spacied"] = spacify(df["cleaned_text"])

    print("Done spacy")
    df["entities"] = df["spacied"].apply(extract_entities)

    print("Starting dump")

    with open("cleaned.pkl", "wb") as f:
        pickle.dump(df, f)

    print("Preprocessed data saved to cleaned_content")


if __name__ == "__main__":
    main()
