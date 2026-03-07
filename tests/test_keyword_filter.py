from zotero_arxiv_daily.executor import Executor
from zotero_arxiv_daily.protocol import Paper
from omegaconf import OmegaConf


def _make_papers(*titles):
    return [
        Paper(source="arxiv", title=t, authors=[], abstract="", url="http://example.com")
        for t in titles
    ]


class TestFilterByKeywords:
    def test_no_keywords_returns_all(self, config):
        executor = Executor.__new__(Executor)
        executor.config = config
        papers = _make_papers("LLM Survey", "RAG System", "Diffusion Model")
        result = executor.filter_by_keywords(papers)
        assert result == papers

    def test_keyword_filters_by_title(self, config):
        cfg = OmegaConf.merge(config, OmegaConf.create({"executor": {"keyword": ["LLM"]}}))
        executor = Executor.__new__(Executor)
        executor.config = cfg
        papers = _make_papers("LLM Survey", "RAG System", "Diffusion Model")
        result = executor.filter_by_keywords(papers)
        assert len(result) == 1
        assert result[0].title == "LLM Survey"

    def test_keyword_is_case_insensitive(self, config):
        cfg = OmegaConf.merge(config, OmegaConf.create({"executor": {"keyword": ["llm"]}}))
        executor = Executor.__new__(Executor)
        executor.config = cfg
        papers = _make_papers("LLM Survey", "RAG System")
        result = executor.filter_by_keywords(papers)
        assert len(result) == 1
        assert result[0].title == "LLM Survey"

    def test_multiple_keywords_uses_or_logic(self, config):
        cfg = OmegaConf.merge(config, OmegaConf.create({"executor": {"keyword": ["LLM", "RAG"]}}))
        executor = Executor.__new__(Executor)
        executor.config = cfg
        papers = _make_papers("LLM Survey", "RAG System", "Diffusion Model")
        result = executor.filter_by_keywords(papers)
        assert len(result) == 2
        titles = {p.title for p in result}
        assert titles == {"LLM Survey", "RAG System"}

    def test_no_matching_keywords_returns_empty(self, config):
        cfg = OmegaConf.merge(config, OmegaConf.create({"executor": {"keyword": ["transformer"]}}))
        executor = Executor.__new__(Executor)
        executor.config = cfg
        papers = _make_papers("LLM Survey", "RAG System", "Diffusion Model")
        result = executor.filter_by_keywords(papers)
        assert result == []

    def test_keyword_matches_substring(self, config):
        cfg = OmegaConf.merge(config, OmegaConf.create({"executor": {"keyword": ["diffusion"]}}))
        executor = Executor.__new__(Executor)
        executor.config = cfg
        papers = _make_papers("Latent Diffusion Models", "Diffusion Model", "RAG System")
        result = executor.filter_by_keywords(papers)
        assert len(result) == 2

    def test_empty_keyword_list_returns_all(self, config):
        cfg = OmegaConf.merge(config, OmegaConf.create({"executor": {"keyword": []}}))
        executor = Executor.__new__(Executor)
        executor.config = cfg
        papers = _make_papers("LLM Survey", "RAG System")
        result = executor.filter_by_keywords(papers)
        assert result == papers
