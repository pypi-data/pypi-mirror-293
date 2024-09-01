from cpmpy.expressions.core import Expression

from ..problem_instance import ProblemInstance
from ..answering_queries import Oracle
from ..metrics import Metrics
from ..predictor.feature_representation import FeatureRepresentation, FeaturesRelDim
from .active_ca import ActiveCA


class ActiveCAPredict(ActiveCA):
    """
    Class interface for the prediction based interactive CA system, using predictions for the constraints.
    Storing the necessary elements and providing functionality to update the state of the system as needed.
    """

    def __init__(self, instance: 'ProblemInstance', algorithm: 'ICA_Algorithm' = None, qgen: 'QGenBase' = None,
                 find_scope: 'FindScopeBase' = None, findc: 'FindCBase' = None, oracle: Oracle = None, *,
                 metrics: Metrics = None, classifier=None, feature_representation: FeatureRepresentation = None,
                 verbose=0, training_frequency=1):
        """
        Initialize with an optional problem instance, oracle, and metrics.

        :param instance: An instance of ProblemInstance, default is None.
        :param algorithm: An instance of ICA_Algorithm, default is None.
        :param qgen: An instance of QGenBase, default is None.
        :param find_scope: An instance of FindScopeBase, default is None.
        :param findc: An instance of FindCBase, default is None.
        :param oracle: An instance of Oracle, default is None.
        :param metrics: An instance of Metrics, default is a new Metrics object.
        :param verbose: Verbosity level, default is 0.
        :param classifier: A classifier for predicting constraints, default is None.
        :param feature_representation: A feature representation object, default is a new FeaturesRelDim object.
        :param training_frequency: Frequency of training the classifier, default is 1.
        """
        super().__init__(instance, algorithm=algorithm, qgen=qgen, find_scope=find_scope, findc=findc, oracle=oracle,
                         metrics=metrics, verbose=verbose)

        self.classifier = classifier
        self._classifier_trained = False

        self.feature_representation = feature_representation
        self.bias_proba = {c: 0.01 for c in self.instance.bias}
        self._datasetX = []  # Constraint dataset
        self._datasetY = []  # Labels

        self._training_frequency = training_frequency

    def init_state(self):
        """ Initialize the state of the CA system. """
        super().init_state()
        if self.training_frequency >= 0 and len(self.instance.cl) > 0:
            self._train_classifier()
        if self._classifier_trained:
            self._predict_bias_proba()
        else:
            self._bias_proba = {c: 0.01 for c in self.instance.bias}

    def run_query_generation(self):
        """ Run the query generation process. """
        if self.training_frequency > 0 and len(self.instance.cl) > 0:
            self._train_classifier()
        if self._classifier_trained:
            self._predict_bias_proba()
        return super().run_query_generation()

    def run_find_scope(self, Y):
        """ Run the find scope process. """
        if self.training_frequency > 1 and len(self.instance.cl) > 0:
            self._train_classifier()
            self._predict_bias_proba()
        return super().run_find_scope(Y)

    def run_findc(self, scope):
        """ Run the find constraint process. """
        if self.training_frequency > 2 and len(self.instance.cl) > 0:
            self._train_classifier()
            self._predict_bias_proba()
        return super().run_findc(scope)

    @ActiveCA.qgen.setter
    def qgen(self, qgen: 'QGenBase'):
        """ Setter method for _qgen """
        from ..query_generation import QGenBase, PQGen
        from ..query_generation.qgen_obj import obj_proba
        assert isinstance(qgen, QGenBase) or qgen is None
        self._qgen = qgen if qgen is not None else PQGen(objective_function=obj_proba)
        self._qgen.ca = self

    @property
    def bias_proba(self):
        """ Get the probabilities of candidate constraints.

        :return: A dictionary of probabilities for candidate constraints.
        """
        return self._bias_proba

    @bias_proba.setter
    def bias_proba(self, bias_proba):
        """ Set the probabilities of candidate constraints.

        :param bias_proba: A dictionary of probabilities for the candidate constraints.
        """
        assert len(bias_proba) == len(self._instance.bias), "bias_proba needs to be the same size as the set of " \
                                                            "candidate constraints."
        self._bias_proba = bias_proba

    @property
    def datasetX(self):
        """ Get the constructed dataset instances.

        :return: A list of dataset instances.
        """
        return self._datasetX

    @datasetX.setter
    def datasetX(self, datasetX):
        """ Set the constructed dataset instances.

        :param datasetX: A list of dataset instances.
        """
        self._datasetX = datasetX

    @property
    def datasetY(self):
        """ Get the constructed dataset labels.

        :return: A list of dataset labels.
        """
        return self._datasetY

    @datasetY.setter
    def datasetY(self, datasetY):
        """ Set the constructed dataset labels.

        :param datasetY: A list of dataset labels.
        """
        self._datasetY = datasetY

    @property
    def classifier(self):
        """ Get the classifier used for predicting constraints.

        :return: The classifier object.
        """
        return self._classifier

    @classifier.setter
    def classifier(self, classifier):
        """ Set the classifier used for predicting constraints.

        :param classifier: A classifier object.
        """
        from sklearn.tree import DecisionTreeClassifier
        self._classifier = classifier if classifier is not None else DecisionTreeClassifier()

    @property
    def classifier_trained(self):
        """ Get the trained status of the classifier.

        :return: A bool indicating if the classifier is trained.
        """
        return self._classifier_trained

    @classifier_trained.setter
    def classifier_trained(self, trained):
        """ Set the trained status of the classifier.

        :param trained: A bool indicating if the classifier is trained.
        """
        self._classifier_trained = trained

    @property
    def feature_representation(self):
        """ Get the feature representation of the problem instance.

        :return: The feature representation object.
        """
        return self._feature_repr

    @feature_representation.setter
    def feature_representation(self, feature_representation):
        """ Set the feature representation of the problem instance.

        :param feature_representation: A feature representation object.
        """
        self._feature_repr = feature_representation \
            if feature_representation is not None else FeaturesRelDim(instance=self.instance)
        if hasattr(self._feature_repr, 'instance'):
            self._feature_repr.instance = self.instance

    @property
    def training_frequency(self):
        """ Get the training frequency of the classifier.

        :return: The training frequency.
        """
        return self._training_frequency

    @training_frequency.setter
    def training_frequency(self, training_frequency):
        """ Set the training frequency of the classifier.

        :param training_frequency: The training frequency.
        """
        self._training_frequency = training_frequency

    def remove_from_bias(self, C):
        """
        Remove given constraints from the bias (candidates)

        :param C: list of constraints to be removed from B
        """
        if isinstance(C, Expression):
            C = [C]
        assert isinstance(C, list), "remove_from_bias accepts as input a list of constraints or a constraint"

        super().remove_from_bias(C)

        for c in C:
            self.bias_proba.pop(c)

        # featurize constraints and add them to the dataset
        self.datasetX.extend(self.feature_representation.featurize_constraints(C))
        self.datasetY.extend([0] * len(C))  # add the respective amount of negative labels

    def add_to_cl(self, C):
        """
        Add the given constraints to the list of learned constraints

        :param C: Constraints to add to CL
        """
        if isinstance(C, Expression):
            C = [C]
        assert isinstance(C, list), "add_to_cl accepts as input a list of constraints or a constraint"

        super().add_to_cl(C)

        # featurize constraints and add them to the dataset
        self.datasetX.extend(self.feature_representation.featurize_constraints(C))
        self.datasetY.extend([1] * len(C))  # add the respective amount of positive labels

    def _train_classifier(self):
        """ Train the classifier with the dataset of learned and excluded constraints """
        self.classifier.fit(self.datasetX, self.datasetY)
        self.classifier_trained = True

    def _predict_bias_proba(self):
        """ Predict the probabilities of candidate constraints using the trained classifier """
        featuresB = {c: self.feature_representation.featurize_constraint(c) for c in self.instance.bias}
        self.bias_proba = {c: self.classifier.predict_proba([featuresB[c]])[0][1]+0.01 for c in self.instance.bias}
