import argparse
import pandas as pd
from pubmed_fetcher.fetcherr import fetch_pubmed_ids, fetch_article_details, parse_article

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers and identify non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed query string.")
    parser.add_argument("-f", "--file", type=str, help="File to save the output as CSV.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output.")
    args = parser.parse_args()

    if args.debug:
        print(f"Querying PubMed for: {args.query}")

    ids = fetch_pubmed_ids(args.query)
    articles = fetch_article_details(ids)

    data = []
    for article in articles:
        pubmed_id, title, pub_date, na_authors, companies, email = parse_article(article)
        data.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(na_authors),
            "Company Affiliation(s)": "; ".join(companies),
            "Corresponding Author Email": email,
        })

    df = pd.DataFrame(data)

    if args.file:
        df.to_csv(args.file, index=False)
        print(f"Saved results to {args.file}")
    else:
        print(df.to_string(index=False))
