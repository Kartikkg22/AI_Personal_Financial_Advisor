import spacy

nlp = spacy.load("en_core_web_sm")

def categorize_expense(description: str):
    # Dummy categorization (could be extended with more sophisticated models)
    doc = nlp(description)
    if "Uber" in description:
        return "Transportation"
    elif "Starbucks" in description:
        return "Food & Beverage"
    else:
        return "Other"
