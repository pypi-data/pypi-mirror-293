"""**Utilities** are the integrations with third-part systems and packages.

Other LangChain classes use **Utilities** to interact with third-part systems
and packages.
"""

from typing import TYPE_CHECKING, Any

from langchain._api import create_importer

if TYPE_CHECKING:
    from langchain_community.utilities import (
        AlphaVantageAPIWrapper,
        ApifyWrapper,
        ArceeWrapper,
        ArxivAPIWrapper,
        BibtexparserWrapper,
        BingSearchAPIWrapper,
        BraveSearchWrapper,
        DuckDuckGoSearchAPIWrapper,
        GoldenQueryAPIWrapper,
        GoogleFinanceAPIWrapper,
        GoogleJobsAPIWrapper,
        GoogleLensAPIWrapper,
        GooglePlacesAPIWrapper,
        GoogleScholarAPIWrapper,
        GoogleSearchAPIWrapper,
        GoogleSerperAPIWrapper,
        GoogleTrendsAPIWrapper,
        GraphQLAPIWrapper,
        JiraAPIWrapper,
        LambdaWrapper,
        MaxComputeAPIWrapper,
        MerriamWebsterAPIWrapper,
        MetaphorSearchAPIWrapper,
        NasaAPIWrapper,
        OpenWeatherMapAPIWrapper,
        OutlineAPIWrapper,
        Portkey,
        PowerBIDataset,
        PubMedAPIWrapper,
        Requests,
        RequestsWrapper,
        SceneXplainAPIWrapper,
        SearchApiAPIWrapper,
        SearxSearchWrapper,
        SerpAPIWrapper,
        SparkSQL,
        SQLDatabase,
        StackExchangeAPIWrapper,
        SteamWebAPIWrapper,
        TensorflowDatasets,
        TextRequestsWrapper,
        TwilioAPIWrapper,
        WikipediaAPIWrapper,
        WolframAlphaAPIWrapper,
        ZapierNLAWrapper,
    )

# Create a way to dynamically look up deprecated imports.
# Used to consolidate logic for raising deprecation warnings and
# handling optional imports.
DEPRECATED_LOOKUP = {
    "AlphaVantageAPIWrapper": "langchain_community.utilities",
    "ApifyWrapper": "langchain_community.utilities",
    "ArceeWrapper": "langchain_community.utilities",
    "ArxivAPIWrapper": "langchain_community.utilities",
    "BibtexparserWrapper": "langchain_community.utilities",
    "BingSearchAPIWrapper": "langchain_community.utilities",
    "BraveSearchWrapper": "langchain_community.utilities",
    "DuckDuckGoSearchAPIWrapper": "langchain_community.utilities",
    "GoldenQueryAPIWrapper": "langchain_community.utilities",
    "GoogleFinanceAPIWrapper": "langchain_community.utilities",
    "GoogleLensAPIWrapper": "langchain_community.utilities",
    "GoogleJobsAPIWrapper": "langchain_community.utilities",
    "GooglePlacesAPIWrapper": "langchain_community.utilities",
    "GoogleScholarAPIWrapper": "langchain_community.utilities",
    "GoogleTrendsAPIWrapper": "langchain_community.utilities",
    "GoogleSearchAPIWrapper": "langchain_community.utilities",
    "GoogleSerperAPIWrapper": "langchain_community.utilities",
    "GraphQLAPIWrapper": "langchain_community.utilities",
    "JiraAPIWrapper": "langchain_community.utilities",
    "LambdaWrapper": "langchain_community.utilities",
    "MaxComputeAPIWrapper": "langchain_community.utilities",
    "MerriamWebsterAPIWrapper": "langchain_community.utilities",
    "MetaphorSearchAPIWrapper": "langchain_community.utilities",
    "NasaAPIWrapper": "langchain_community.utilities",
    "OpenWeatherMapAPIWrapper": "langchain_community.utilities",
    "OutlineAPIWrapper": "langchain_community.utilities",
    "Portkey": "langchain_community.utilities",
    "PowerBIDataset": "langchain_community.utilities",
    "PubMedAPIWrapper": "langchain_community.utilities",
    # We will not list PythonREPL in __all__ since it has been removed from community
    # it'll proxy to community package, which will raise an appropriate exception.
    "PythonREPL": "langchain_community.utilities",
    "Requests": "langchain_community.utilities",
    "SteamWebAPIWrapper": "langchain_community.utilities",
    "SQLDatabase": "langchain_community.utilities",
    "SceneXplainAPIWrapper": "langchain_community.utilities",
    "SearchApiAPIWrapper": "langchain_community.utilities",
    "SearxSearchWrapper": "langchain_community.utilities",
    "SerpAPIWrapper": "langchain_community.utilities",
    "SparkSQL": "langchain_community.utilities",
    "StackExchangeAPIWrapper": "langchain_community.utilities",
    "TensorflowDatasets": "langchain_community.utilities",
    "RequestsWrapper": "langchain_community.utilities",
    "TextRequestsWrapper": "langchain_community.utilities",
    "TwilioAPIWrapper": "langchain_community.utilities",
    "WikipediaAPIWrapper": "langchain_community.utilities",
    "WolframAlphaAPIWrapper": "langchain_community.utilities",
    "ZapierNLAWrapper": "langchain_community.utilities",
}

_import_attribute = create_importer(__package__, deprecated_lookups=DEPRECATED_LOOKUP)


def __getattr__(name: str) -> Any:
    """Look up attributes dynamically."""
    return _import_attribute(name)


__all__ = [
    "AlphaVantageAPIWrapper",
    "ApifyWrapper",
    "ArceeWrapper",
    "ArxivAPIWrapper",
    "BibtexparserWrapper",
    "BingSearchAPIWrapper",
    "BraveSearchWrapper",
    "DuckDuckGoSearchAPIWrapper",
    "GoldenQueryAPIWrapper",
    "GoogleFinanceAPIWrapper",
    "GoogleLensAPIWrapper",
    "GoogleJobsAPIWrapper",
    "GooglePlacesAPIWrapper",
    "GoogleScholarAPIWrapper",
    "GoogleTrendsAPIWrapper",
    "GoogleSearchAPIWrapper",
    "GoogleSerperAPIWrapper",
    "GraphQLAPIWrapper",
    "JiraAPIWrapper",
    "LambdaWrapper",
    "MaxComputeAPIWrapper",
    "MerriamWebsterAPIWrapper",
    "MetaphorSearchAPIWrapper",
    "NasaAPIWrapper",
    "OpenWeatherMapAPIWrapper",
    "OutlineAPIWrapper",
    "Portkey",
    "PowerBIDataset",
    "PubMedAPIWrapper",
    "Requests",
    "SteamWebAPIWrapper",
    "SQLDatabase",
    "SceneXplainAPIWrapper",
    "SearchApiAPIWrapper",
    "SearxSearchWrapper",
    "SerpAPIWrapper",
    "SparkSQL",
    "StackExchangeAPIWrapper",
    "TensorflowDatasets",
    "RequestsWrapper",
    "TextRequestsWrapper",
    "TwilioAPIWrapper",
    "WikipediaAPIWrapper",
    "WolframAlphaAPIWrapper",
    "ZapierNLAWrapper",
]
