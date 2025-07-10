from typing import List, Dict, Tuple
from Bio import Entrez
from pubmed_fetcher.util import is_non_academic, extract_email

Entrez.email = "alugojusriharshini@gmail.com"  # REQUIRED for PubMed API

def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    """
    Fetch PubMed IDs for a given query.
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record["IdList"]

def fetch_article_details(pubmed_ids: List[str]) -> List[Dict]:
    """
    Fetch full article details given a list of PubMed IDs.
    """
    handle = Entrez.efetch(db="pubmed", id=",".join(pubmed_ids), rettype="medline", retmode="xml")
    records = Entrez.read(handle)
    return records["PubmedArticle"]

def parse_article(article: Dict) -> Tuple[str, str, str, List[str], List[str], str]:
    """
    Parse article details to extract required fields.
    Returns:
        PubmedID, Title, Publication Date, Non-academic Author(s), Company Affiliations, Email
    """
    pubmed_id = article["MedlineCitation"]["PMID"]
    title = article["MedlineCitation"]["Article"]["ArticleTitle"]
    pub_date = article["MedlineCitation"]["Article"]["Journal"]["JournalIssue"].get("PubDate", {})
    year = pub_date.get("Year", "")
    month = pub_date.get("Month", "")
    day = pub_date.get("Day", "")
    publication_date = "-".join(filter(None, [year, month, day]))

    authors_info = article["MedlineCitation"]["Article"].get("AuthorList", [])
    non_academic_authors, companies, email = [], [], ""

    for author in authors_info:
        affil = author.get("AffiliationInfo", [])
        name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip()

        if affil:
            affiliation = affil[0].get("Affiliation", "")
            if is_non_academic(affiliation):
                non_academic_authors.append(name)
                companies.append(affiliation)

            if "@" in affiliation and not email:
                email = extract_email(affiliation)

    return pubmed_id, title, publication_date, non_academic_authors, companies, email
