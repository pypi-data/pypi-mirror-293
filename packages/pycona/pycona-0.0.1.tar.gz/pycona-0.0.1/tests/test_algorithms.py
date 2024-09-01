import unittest

import pytest

from QuAcq import QuAcq
from MQuAcq import MQuAcq
from MQuAcq2 import MQuAcq2
from GrowAcq import GrowAcq
from benchmarks import *
from main import construct_classifier

test_benchmarks = [
    "murder",
    "4sudoku",
    "golomb8",
    "job_shop_scheduling",
    "exam_timetabling",
    "nurse_rostering_adv",
]

bench_parameters = {
    # Small job shop instance
    "num_jobs": 6,
    "num_machines": 3,
    "horizon": 10,
    "seed": 0,
    # Small Exam timetabling instance
    "num_semesters": 6,
    "num_courses_per_semester": 3,
    "num_rooms": 1,
    "num_timeslots_per_day": 2,
    "num_days_for_exams": 10,
    "num_professors": None,
    # Small Nurse rostering instance
    "num_nurses": 10,
    "num_shifts_per_day": 3,
    "num_days_for_schedule": 3,
    "nurses_per_shift": 2
}

alg_parameters = {
        "qg": "pqgen",
        "obj": "max",
        "findscope_version": 2,
        "findc_version": 1
    }

proba_parameters = {
    "qg": "pqgen",
    "obj": "proba",
    "findscope_version": 2,
    "findc_version": 1,
    "gqg": True,
    "gfs": True,
    "gfc": True,
    "classifier": None,
    "classifier_name": None
}

classifier_names = ["counts", "random_forest", "MLP", "GaussianNB", "CategoricalNB", "SVM"]

def _generate_classifiers():
    classfiers = []
    for cls in classifier_names:
         classfiers += (cls, construct_classifier(cls))
    return classfiers

class TestAlgorithms:

    @pytest.mark.parametrize("bench", test_benchmarks, ids=str)
    def test_quacq(self,bench):
        benchmark = Benchmark(bench, **bench_parameters)
        benchmark.construct_benchmark()
        ca_system = QuAcq(gamma=benchmark.gamma,grid=benchmark.grid,C_T=benchmark.C_T,**alg_parameters)
        ca_system.learn()
        assert len(ca_system.C_l.constraints) > 0
        assert ca_system.C_l.solve()

    @pytest.mark.parametrize("bench", test_benchmarks, ids=str)
    def test_mquacq(self,bench):
        benchmark = Benchmark(bench, **bench_parameters)
        benchmark.construct_benchmark()
        ca_system = MQuAcq(gamma=benchmark.gamma,grid=benchmark.grid,C_T=benchmark.C_T,**alg_parameters)
        ca_system.learn()
        assert len(ca_system.C_l.constraints) > 0
        assert ca_system.C_l.solve()

    @pytest.mark.parametrize("bench", test_benchmarks, ids=str)
    def test_mquacq2(self, bench):
        benchmark = Benchmark(bench, **bench_parameters)
        benchmark.construct_benchmark()
        ca_system = MQuAcq2(gamma=benchmark.gamma, grid=benchmark.grid, C_T=benchmark.C_T, **alg_parameters)
        ca_system.learn()
        assert len(ca_system.C_l.constraints) > 0
        assert ca_system.C_l.solve()

    @pytest.mark.parametrize("bench", test_benchmarks, ids=str)
    def test_growacq(self,bench):
        benchmark = Benchmark(bench, **bench_parameters)
        benchmark.construct_benchmark()
        ca_system = GrowAcq(gamma=benchmark.gamma,grid=benchmark.grid,C_T=benchmark.C_T,**alg_parameters)
        ca_system.learn()
        assert len(ca_system.C_l.constraints) > 0
        assert ca_system.C_l.solve()

    @pytest.mark.parametrize("classifier_name", classifier_names, ids=str)
    def test_proba(self, classifier_name):
        classifier = construct_classifier(classifier_name)
        proba_parameters['classifier_name'] = classifier_name
        proba_parameters['classifier'] = classifier

        benchmark = Benchmark("nurse_rostering", **bench_parameters)
        benchmark.construct_benchmark()

        ca_system = GrowAcq(gamma=benchmark.gamma,grid=benchmark.grid,C_T=benchmark.C_T,**proba_parameters)
        ca_system.learn()

        assert len(ca_system.C_l.constraints) > 0
        assert ca_system.C_l.solve()
