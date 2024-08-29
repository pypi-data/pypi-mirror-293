import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(filename='paper_collection.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


class Paper:
    def __init__(self, eid: str, source: str):
        self.eid = eid
        self.source = source  # Identify the source (Scopus or arXiv)
        self.title = ""
        self.year = ""
        self.citedby_count = 0
        self.abstract = ""


class DataSource:
    def search(self, query, limit):
        raise NotImplementedError


class ScopusDataSource(DataSource):
    def __init__(self, config_path=None):
        self._set_config_path(config_path)
        self._import_pybliometrics()

    def _set_config_path(self, config_path):
        if config_path is not None:
            os.environ["PYB_CONFIG_FILE"] = config_path
        else:
            os.environ["PYB_CONFIG_FILE"] = "D:/.pybliometrics/pybliometrics.cfg"

    def _import_pybliometrics(self):
        global ScopusSearch, AbstractRetrieval
        from pybliometrics.scopus import ScopusSearch, AbstractRetrieval


    def search(self, query, limit=None):
        try:
            print(f"Querying Scopus with limit: {limit}")
            if limit is None:
                search = ScopusSearch(query)
            else:
                search = ScopusSearch(query, count=limit)
            eids = search.get_eids()
            print(f"Number of EIDs returned from Scopus: {len(eids)}")

            if eids:
                abstracts = [AbstractRetrieval(eid, view='FULL') for eid in eids]
                print(f"Number of abstracts retrieved from Scopus: {len(abstracts)}")
                return abstracts
            else:
                print("No abstracts retrieved.")
        except Exception as e:
            logging.error(f"Failed to query Scopus: {e}")
            return []



class ArxivDataSource(DataSource):
    ARXIV_API_ENDPOINT = "http://export.arxiv.org/api/query"

    def search(self, query, limit=None):
        try:
            params = {"search_query": query, "start": 0}

            # Fetching initial batch of results
            if limit is not None:
                params["max_results"] = limit
                response = requests.get(self.ARXIV_API_ENDPOINT, params=params)
                response.raise_for_status()
                root = ET.fromstring(response.text)
                entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            else:
                entries = []
                # If no limit is specified, try to fetch all available results (with caution)
                while True:
                    response = requests.get(self.ARXIV_API_ENDPOINT, params=params)
                    response.raise_for_status()
                    root = ET.fromstring(response.text)
                    new_entries = root.findall("{http://www.w3.org/2005/Atom}entry")
                    if not new_entries:
                        break
                    entries.extend(new_entries)
                    params["start"] += len(new_entries)

            return entries
        except Exception as e:
            logging.error(f"Failed to query arXiv: {e}")
            return []


class MultiSourcePaperCollector:
    def __init__(self, data_sources, queries=None, limit=None, **query_params):
        if not isinstance(data_sources, list):
            data_sources = [data_sources]
        self.data_sources = data_sources
        self.queries = queries or self.build_query(**query_params)
        self.limit = limit
        self.results = pd.DataFrame()

    @staticmethod
    def build_query(keywords=None, startyear=None, endyear=None, fixyear=None,
                    openaccess=None):
        if not any([keywords, startyear, endyear, fixyear, openaccess]):
            raise ValueError("At least one search parameter must be provided.")

        # For Scopus
        scopus_query = ""
        if keywords:
            scopus_query += f"TITLE-ABS-KEY({keywords})"
        if startyear or endyear:
            scopus_query += f" AND PUBYEAR > {startyear}" if startyear else ""
            scopus_query += f" AND PUBYEAR < {endyear}" if endyear else ""
        elif fixyear:
            scopus_query += f" AND PUBYEAR = {fixyear}"
        if openaccess:
            scopus_query += " AND OA(all)"

        # For arXiv
        arxiv_query = ""
        if keywords:
            arxiv_query += f"all:{keywords}"

        # Print the generated queries
        print(f"Scopus Query: {scopus_query}")
        print(f"arXiv Query: {arxiv_query}")

        return {"Scopus": scopus_query, "arXiv": arxiv_query}

    def collect_papers(self):
        last_logged_time = datetime.now()
        all_papers = []

        for data_source in self.data_sources:
            try:
                if isinstance(data_source, ScopusDataSource):
                    query = self.queries["Scopus"]
                    abstracts = data_source.search(query, self.limit)
                    papers = [self._parse_scopus_abstract(abstract) for abstract in abstracts]
                elif isinstance(data_source, ArxivDataSource):
                    query = self.queries["arXiv"]
                    entries = data_source.search(query, self.limit)
                    papers = [self._parse_arxiv_entry(entry) for entry in entries]
                all_papers.extend(papers)

                # Log progress
                if (datetime.now() - last_logged_time).seconds >= 3600:
                    logging.info(f"Ongoing collection at {datetime.now()}: Collected {len(all_papers)} papers so far.")
                    last_logged_time = datetime.now()

            except Exception as e:
                logging.error(f"Error during data collection from {type(data_source).__name__}: {e}")

        self.results = pd.DataFrame([vars(p) for p in all_papers], index=[p.eid for p in all_papers])
        logging.info("Paper collection completed successfully.")

    def _parse_scopus_abstract(self, abstract):
        paper = Paper(abstract.eid, "Scopus")
        paper.title = abstract.title
        paper.year = abstract.coverDate[:4]
        paper.citedby_count = abstract.citedby_count
        paper.abstract = abstract.abstract
        return paper

    def _parse_arxiv_entry(self, entry):
        paper = Paper(entry.find("{http://www.w3.org/2005/Atom}id").text,
                      "arXiv")
        paper.title = entry.find("{http://www.w3.org/2005/Atom}title").text
        paper.year = entry.find("{http://www.w3.org/2005/Atom}published").text[:4]
        paper.abstract = entry.find("{http://www.w3.org/2005/Atom}summary").text
        return paper

