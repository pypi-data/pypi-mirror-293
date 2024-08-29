[![Build status](https://github.com/monarch-initiative/gpsea/workflows/CI/badge.svg)](https://github.com/monarch-initiative/gpsea/actions/workflows/python_ci.yml)
[![GitHub release](https://img.shields.io/github/release/monarch-initiative/gpsea.svg)](https://github.com/monarch-initiative/gpsea/releases)
![PyPi downloads](https://img.shields.io/pypi/dm/gpsea.svg?label=Pypi%20downloads)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gpsea)

GPSEA is a Python library for discovery of genotype-phenotype associations.

An example of simple genotype-phenotype association analysis

```python
# Load HPO
import hpotk

store = hpotk.configure_ontology_store()
hpo = store.load_minimal_hpo()

# Load a cohort of phenopackets
from gpsea.data import get_toy_cohort

cohort = get_toy_cohort()

# Analyze genotype-phenotype associations
from gpsea.analysis import configure_cohort_analysis
from gpsea.analysis.predicate import PatientCategories

from gpsea.model import VariantEffect

cohort_analysis = configure_cohort_analysis(cohort, hpo)
frameshift = cohort_analysis.compare_by_variant_effect(VariantEffect.FRAMESHIFT_VARIANT, tx_id='NM_1234.5')

frameshift.summarize(hpo, category=PatientCategories.YES)
```

provides a pandas data frame with genotype-phenotype correlations:

```text
FRAMESHIFT_VARIANT on NM_1234.5                                    No                Yes
                                                                Count   Percent    Count   Percent    p value    Corrected p value
    Arachnodactyly [HP:0001166]                                  1/10       10%    13/16       81%   0.000781             0.020299
    Abnormality of the musculature [HP:0003011]                   6/6      100%    11/11      100%   1.000000             1.000000
    Abnormal nervous system physiology [HP:0012638]               9/9      100%    15/15      100%   1.000000             1.000000
    ...                                                           ...       ...      ...       ...        ...                  ...
```

## Documentation

Check out the User guide and the API reference for more info:

- [Stable documentation](https://monarch-initiative.github.io/gpsea/stable/) (last release on `main` branch)
- [Latest documentation](https://monarch-initiative.github.io/gpsea/latest) (bleeding edge, latest commit on `develop` branch)
