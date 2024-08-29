import abc
import typing
from collections import namedtuple, defaultdict

import hpotk
import pandas as pd

from gpsea.model import Patient
from gpsea.preprocessing import ProteinMetadataService
from .predicate import PolyPredicate, PatientCategory
from .predicate.genotype import GenotypePolyPredicate, VariantPredicate, ProteinPredicates
from .predicate.phenotype import P, PhenotypePolyPredicate
from .pscore import PhenotypeScorer, CountingPhenotypeScorer

PatientsByHPO = namedtuple('PatientsByHPO', field_names=['all_with_hpo', 'all_without_hpo'])


class HpoMtcReport:
    """
    Class to simplify reporting results of multiple testing filtering by HpoMtcFilter subclasses.
    """
    # TODO: delete with no replacement.

    def __init__(
            self,
            filter_name: str,
            mtc_name: str,
            filter_results_map: typing.Mapping[str, int],
            n_terms_before_filtering: int,
    ):
        """
        Args:
            filter_name: name of the MTC filter strategy (e.g. `heuristic sampler`)
            mtc_name:  name of the MTC function (e.g. `bonferroni`)
            filter_results_map: mapping with reasons for filtering out a term as keys, and counts of filtered terms as values
            n_terms_before_filtering: the number of HPO terms before filtering
        """
        self._filter_name = filter_name
        self._mtc_name = mtc_name
        self._results_map = filter_results_map
        self._n_terms_before_filtering = n_terms_before_filtering

    @property
    def filter_method(self) -> str:
        """
        Returns:
            the name of the HpoMtcFilter method used.
        """
        return self._filter_name

    @property
    def skipped_terms_dict(self) -> typing.Mapping[str, int]:
        """
        Returns:
            a mapping with reasons why an HPO term was skipped as keys and counts of the skipped terms as values.
        """
        return self._results_map

    @property
    def mtc_method(self) -> str:
        """
         Returns:
             the name of the multiple testing correction method used (e.g. `bonferroni`).
        """
        return self._mtc_name

    @property
    def n_terms_before_filtering(self) -> int:
        """
        Get the number of terms before filtering.
        """
        return self._n_terms_before_filtering


class GenotypePhenotypeAnalysisResult:
    """
    `GenotypePhenotypeAnalysisResult` summarizes results of genotype-phenotype correlation analysis of a cohort.
    """
    # TODO: delete and use `gpsea.analysis.pcats.MultiPhenotypeAnalysisResult`.

    def __init__(
            self,
            n_usable: typing.Mapping[P, int],
            all_counts: typing.Mapping[P, pd.DataFrame],
            pvals: pd.Series,
            corrected_pvals: typing.Optional[pd.Series],
            phenotype_categories: typing.Iterable[PatientCategory],
            geno_predicate: PolyPredicate,
            mtc_filter_report: typing.Optional[HpoMtcReport] = None
    ):
        self._n_usable = n_usable
        self._all_counts = all_counts
        self._pvals = pvals
        self._corrected_pvals = corrected_pvals
        self._phenotype_categories = tuple(phenotype_categories)
        self._geno_predicate = geno_predicate
        self._mtc_filter_report = mtc_filter_report

    @property
    def n_usable(self) -> typing.Mapping[P, int]:
        """
        Get a mapping from a phenotype `P` (either an HPO term or a disease ID)
        to an `int` with the number of patients where the phenotype was assessable,
        and are, thus, usable for genotype-phenotype correlation analysis.
        """
        return self._n_usable

    @property
    def all_counts(self) -> typing.Mapping[P, pd.DataFrame]:
        """
        Get a mapping from the phenotype item to :class:`pandas.DataFrame` with counts of patients
        in genotype and phenotype groups.

        An example for a genotype predicate that bins into two categories (`Yes` and `No`) based on presence
        of a missense variant in transcript `NM_123456.7`, and phenotype predicate that checks
        presence/absence of `HP:0001166` (a phenotype term)::

                       Has MISSENSE_VARIANT in NM_123456.7
                       No       Yes
            Present
            Yes        1        13
            No         7        5

        The rows correspond to the phenotype categories, and the columns represent the genotype categories.
        """
        return self._all_counts

    @property
    def pvals(self) -> pd.Series:
        """
        Get a :class:`pandas.Series` with p values for each tested HPO term.
        """
        return self._pvals

    @property
    def corrected_pvals(self) -> typing.Optional[pd.Series]:
        """
        Get an optional :class:`pandas.Series` with p values for each tested HPO term after multiple testing correction.
        """
        return self._corrected_pvals

    @property
    def phenotype_categories(self) -> typing.Sequence[PatientCategory]:
        """
        Get a sequence of phenotype patient categories that can be investigated.
        """
        return self._phenotype_categories

    @property
    def total_tests(self) -> int:
        """
        Get total count of tests that were run for this analysis.
        """
        return len(self._all_counts)

    @property
    def mtc_filter_report(self) -> typing.Optional[HpoMtcReport]:
        return self._mtc_filter_report

    def summarize(
            self, hpo: hpotk.MinimalOntology,
            category: PatientCategory,
    ) -> pd.DataFrame:
        """
        Create a data frame with summary of the genotype phenotype analysis.

        The *rows* of the frame correspond to the analyzed HPO terms.

        The columns of the data frame have `Count` and `Percentage` per used genotype predicate.

        **Example**

        If we use :class:`~gpsea.analysis.predicate.genotype.VariantEffectPredicate`
        which can compare phenotype with and without a missense variant, we will have a data frame
        that looks like this::

            MISSENSE_VARIANT on `NM_1234.5`                       No                  Yes
                                                                  Count    Percent    Count    Percent   p value   Corrected p value
            Arachnodactyly [HP:0001166]                           1/10         10%    13/16        81%   0.000781  0.020299
            Abnormality of the musculature [HP:0003011]           6/6         100%    11/11       100%   1.000000  1.000000
            Abnormal nervous system physiology [HP:0012638]       9/9         100%    15/15       100%   1.000000  1.000000
            ...                                                   ...      ...        ...      ...       ...       ...
        """
        if category not in self._phenotype_categories:
            raise ValueError(f'Unknown phenotype category: {category}. Use one of {self._phenotype_categories}')

        # Row index: a list of tested HPO terms
        pheno_idx = pd.Index(self._n_usable.keys())
        # Column index: multiindex of counts and percentages for all genotype predicate groups
        geno_idx = pd.MultiIndex.from_product(
            iterables=(self._geno_predicate.get_categories(), ('Count', 'Percent')),
            names=(self._geno_predicate.get_question(), None),
        )

        # We'll fill this frame with data
        df = pd.DataFrame(index=pheno_idx, columns=geno_idx)

        for pf, count in self._all_counts.items():
            gt_totals = count.sum()  # Sum across the phenotype categories (collapse the rows).
            for gt_cat in count.columns:
                cnt = count.loc[category, gt_cat]
                total = gt_totals[gt_cat]
                df.loc[pf, (gt_cat, 'Count')] = f'{cnt}/{total}'
                pct = 0 if total == 0 else round(cnt * 100 / total)
                df.loc[pf, (gt_cat, 'Percent')] = f'{pct}%'

        # Add columns with p values and corrected p values (if present)
        df.insert(df.shape[1], ('', self._pvals.name), self._pvals)
        if self._corrected_pvals is not None:
            df.insert(df.shape[1], ('', self._corrected_pvals.name), self._corrected_pvals)

        # Format the index values: `HP:0001250` -> `Seizure [HP:0001250]` if the index members are HPO terms
        # or just use the term ID CURIE otherwise (e.g. `OMIM:123000`).
        labeled_idx = df.index.map(lambda term_id: GenotypePhenotypeAnalysisResult._format_term_id(hpo, term_id))

        # Last, sort by corrected p value or just p value
        df = df.set_index(labeled_idx)
        if self._corrected_pvals is not None:
            return df.sort_values(by=[('', self._corrected_pvals.name), ('', self._pvals.name)])
        else:
            return df.sort_values(by=('', self._pvals.name))

    @staticmethod
    def _format_term_id(
            hpo: hpotk.MinimalOntology,
            term_id: hpotk.TermId,
    ) -> str:
        """
        Format a `term_id` as a `str`. HPO term ID is formatted as `<name> [<term_id>]` whereas other term IDs
        are formatted as CURIEs (e.g. `OMIM:123000`).
        """
        if term_id.prefix == 'HP':
            min_onto = hpo.get_term(term_id)
            return f'{min_onto.name} [{term_id.value}]'
        else:
            return term_id.value


class PhenotypeScoreAnalysisResult:
    """
    `PhenotypeScoreAnalysisResult` includes results of testing genotypes vs. phenotype scores.

    See :ref:`Mann Whitney U Test for phenotype score <phenotype-score-stats>` for more background.
    """
    # TODO: delete and use `gpsea.analysis.pscore.PhenotypeScoreAnalysisResult`

    def __init__(
        self,
        genotype_phenotype_scores: pd.DataFrame,
        p_value: float,
    ):
        self._genotype_phenotype_scores = genotype_phenotype_scores
        self._p_value = p_value

    @property
    def genotype_phenotype_scores(
        self,
    ) -> pd.DataFrame:
        """
        Get the DataFrame with the genotype group and the phenotype score for each patient.

        The DataFrame has the following structure:

        ==========  ========  =========
        patient_id  genotype  phenotype
        ==========  ========  =========
        patient_1   0         1
        patient_2   0         3
        patient_3   1         2
        ...         ...       ...
        ==========  ========  =========

        The DataFrame index includes the patient IDs, and then there are 2 columns
        with the `genotype` group id (:attr:`~gpsea.analysis.predicate.PatientCategory.cat_id`)
        and the `phenotype` score.
        """
        return self._genotype_phenotype_scores

    @property
    def p_value(self) -> float:
        return self._p_value

    def __str__(self) -> str:
        return 'PhenotypeGroupAnalysisResult(' \
            f'genotype_phenotype_scores={self._genotype_phenotype_scores}, ' \
            f'p_value={self._p_value})'

    def __repr__(self) -> str:
        return str(self)


class CohortAnalysis(metaclass=abc.ABCMeta):
    """
    `CohortAnalysis` is a driver class for running genotype-phenotype correlation analyses.

    The class provides various methods to test genotype-phenotype correlations. All methods wrap results
    into :class:`GenotypePhenotypeAnalysisResult`.
    """
    # TODO: remove and use the analyses described in `User Guide > Statistical tests`.

    def __init__(
        self,
        hpo: hpotk.MinimalOntology,
        protein_service: ProteinMetadataService,
    ):
        self._hpo = hpotk.util.validate_instance(hpo, hpotk.MinimalOntology, 'hpo')
        self._protein_service = protein_service
        self._protein_predicates = ProteinPredicates(self._protein_service)

    @abc.abstractmethod
    def compare_hpo_vs_genotype(
            self,
            predicate: VariantPredicate,
    ) -> GenotypePhenotypeAnalysisResult:
        """
        Bin patients according to a presence of at least one allele that matches `predicate`
        and test for genotype-phenotype correlations.
        """
        pass

    @abc.abstractmethod
    def compare_hpo_vs_recessive_genotype(
        self,
        predicate: VariantPredicate,
    ) -> GenotypePhenotypeAnalysisResult:
        """
        Bin patients according to a presence of zero, one, or two alleles that matche the `predicate`
        and test for genotype-phenotype correlations.
        """
        pass

    @abc.abstractmethod
    def compare_hpo_vs_genotype_groups(
        self,
        predicates: typing.Iterable[VariantPredicate],
        group_names: typing.Iterable[str],
    ) -> GenotypePhenotypeAnalysisResult:
        """
        Bin patients according to a presence of at least one allele that matches
        any of the provided `predicates` and test for genotype-phenotype correlations
        between the groups.

        Note, the patients that pass testing by >1 genotype predicate are *OMITTED* from the analysis!
        """
        pass

    @abc.abstractmethod
    def compare_disease_vs_genotype(
        self,
        predicate: VariantPredicate,
        disease_ids: typing.Optional[typing.Sequence[typing.Union[str, hpotk.TermId]]] = None,
    ) -> GenotypePhenotypeAnalysisResult:
        pass

    def compare_genotype_vs_phenotype_group_count(
        self,
        gt_predicate: GenotypePolyPredicate,
        phenotype_group_terms: typing.Iterable[typing.Union[str, hpotk.TermId]],
    ) -> PhenotypeScoreAnalysisResult:
        # TODO: separate into pscore module
        assert isinstance(gt_predicate, GenotypePolyPredicate)
        assert gt_predicate.n_categorizations() == 2

        counting_scorer = CountingPhenotypeScorer.from_query_curies(
            hpo=self._hpo,
            query=phenotype_group_terms,
        )

        return self.compare_genotype_vs_phenotype_score(
            gt_predicate=gt_predicate,
            phenotype_scorer=counting_scorer,
        )

    @abc.abstractmethod
    def compare_genotype_vs_phenotype_score(
        self,
        gt_predicate: GenotypePolyPredicate,
        phenotype_scorer: PhenotypeScorer,
    ) -> PhenotypeScoreAnalysisResult:
        """
        Score the patients with a phenotype scoring method and test for correlation between the genotype group
        and the phenotype score.

        Args:
            gt_predicate: a genotype predicate for binning the patients along the genotype axis.
            phenotype_scorer: a callable that computes a phenotype score for a given `Patient`.
        """
        pass

    @abc.abstractmethod
    def compare_genotype_vs_cohort_phenotypes(
        self,
        gt_predicate: GenotypePolyPredicate,
    ) -> GenotypePhenotypeAnalysisResult:
        pass

    @abc.abstractmethod
    def compare_genotype_vs_phenotypes(
        self,
        gt_predicate: GenotypePolyPredicate,
        pheno_predicates: typing.Iterable[PhenotypePolyPredicate[P]],
    ):
        """
        All analysis functions go through this function.

        The genotype predicate will partition the individuals into non-overlapping groups
        along the genotype axis.
        The phenotype predicates represent the phenotypes we want to test.
        Less phenotypes may actually be tested thanks to :class:`~gpsea.analysis.PhenotypeMtcFilter`.

        Args:
            gt_predicate: a predicate for binning the individuals along the genotype axis
            pheno_predicates: phenotype predicates for test the individuals along the phenotype axis
        """
        pass

    @staticmethod
    def _check_min_perc_patients_w_hpo(min_perc_patients_w_hpo: typing.Union[int, float],
                                       cohort_size: int) -> float:
        """
        Check if the input meets the requirements.
        """
        if isinstance(min_perc_patients_w_hpo, int):
            if min_perc_patients_w_hpo > 0:
                return min_perc_patients_w_hpo / cohort_size
            else:
                raise ValueError(f'`min_perc_patients_w_hpo` must be a positive `int` '
                                 f'but got {min_perc_patients_w_hpo}')
        elif isinstance(min_perc_patients_w_hpo, float):
            if 0 < min_perc_patients_w_hpo <= 1:
                return min_perc_patients_w_hpo
            else:
                raise ValueError(f'`min_perc_patients_w_hpo` must be a `float` in range (0, 1] '
                                 f'but got {min_perc_patients_w_hpo}')
        else:
            raise ValueError(f'`min_perc_patients_w_hpo` must be a positive `int` or a `float` in range (0, 1] '
                             f'but got {type(min_perc_patients_w_hpo)}')

    @staticmethod
    def _group_patients_by_hpo(phenotypic_features: typing.Iterable[hpotk.TermId],
                               patients: typing.Iterable[Patient],
                               hpo: hpotk.GraphAware,
                               missing_implies_excluded: bool) -> PatientsByHPO:
        all_with_hpo = defaultdict(list)
        all_without_hpo = defaultdict(list)
        for hpo_term in phenotypic_features:
            for patient in patients:
                found = False
                for pf in patient.present_phenotypes():
                    if hpo_term == pf.identifier or hpo.graph.is_ancestor_of(hpo_term, pf):
                        # Patient is annotated with `hpo_term` because `pf` is equal to `hpo_term`
                        # or it is a descendant of `hpo_term`.
                        all_with_hpo[hpo_term].append(patient)

                        # If one `pf` of the patient is found to be a descendant of `hpo`, we must break to prevent
                        # adding the patient to `present_hpo` more than once due to another descendant!
                        found = True
                        break
                if not found:
                    # The patient is not annotated by the `hpo_term`.

                    if missing_implies_excluded:
                        # The `hpo_term` annotation is missing, hence implicitly excluded.
                        all_without_hpo[hpo_term].append(patient)
                    else:
                        # The `hpo_term` must be explicitly excluded patient to be accounted for.
                        for ef in patient.excluded_phenotypes():
                            if hpo_term == ef.identifier or hpo.graph.is_descendant_of(hpo_term, ef):
                                all_with_hpo[hpo_term].append(patient)
                                break

        return PatientsByHPO(all_with_hpo, all_without_hpo)
