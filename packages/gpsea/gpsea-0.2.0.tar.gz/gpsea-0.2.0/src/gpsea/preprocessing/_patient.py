import abc

import typing

import hpotk

from gpsea.model import Patient, Cohort

from ._audit import Auditor, Notepad

T = typing.TypeVar('T')
"""
The input for `PatientCreator`.

It can be any object that contains the patient data (e.g. a phenopacket).
"""


class PatientCreator(typing.Generic[T], Auditor[T, Patient], metaclass=abc.ABCMeta):
    """
    `PatientCreator` can create a `Patient` from some input `T`.

    `PatientCreator` is an `Auditor`, hence the input is sanitized and any errors are reported to the caller.
    """
    pass


class CohortCreator(typing.Generic[T], Auditor[typing.Iterable[T], Cohort]):
    """
    `CohortCreator` creates a cohort from an iterable of some `T` where `T` represents a cohort member.
    """

    def __init__(self, patient_creator: PatientCreator[T]):
        # Check that we're getting a `PatientCreator`.
        # Unfortunately, we cannot check that `T`s of `PatientCreator` and `CohortCreator` actually match
        # due to Python's loosey-goosey nature.
        self._pc = hpotk.util.validate_instance(patient_creator, PatientCreator, 'patient_creator')

    def process(self, inputs: typing.Iterable[T], notepad: Notepad) -> Cohort:
        patients = []

        for i, pp in enumerate(inputs):
            sub = notepad.add_subsection(f'patient #{i}')
            patient = self._pc.process(pp, sub)
            patients.append(patient)

        # What happens if a sample has

        # We should have >1 patients in the cohort, right?
        if len(patients) <= 1:
            notepad.add_warning(f'Cohort must include {len(patients)}>1 members',
                                'Fix issues in patients to enable the analysis')

        return Cohort.from_patients(patients)
