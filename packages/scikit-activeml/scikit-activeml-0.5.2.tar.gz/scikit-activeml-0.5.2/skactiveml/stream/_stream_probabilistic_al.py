import numpy as np
from sklearn import clone
from sklearn.utils import check_array, check_consistent_length

from ..classifier import ParzenWindowClassifier
from .budgetmanager import BalancedIncrementalQuantileFilter
from ..base import (
    SingleAnnotatorStreamQueryStrategy,
    SkactivemlClassifier,
    BudgetManager,
)
from ..pool import cost_reduction
from ..utils import (
    check_type,
    check_random_state,
    check_scalar,
    call_func,
    check_budget_manager,
)


class StreamProbabilisticAL(SingleAnnotatorStreamQueryStrategy):
    """StreamProbabilisticAL

    Probabilistic Active Learning in Datastreams (StreamProbabilisticAL) is an
    extension to Multi-Class Probabilistic Active Learning (McPAL)
    (see pool.ProbabilisticAL). It assesses McPAL spatial to assess the spatial
    utility. The Balanced Incremental Quantile Filter
    (BalancedIncrementalQuantileFilter), that is implemented within the
    default budget manager, is used to evaluate the temporal utility
    (see stream.budgetmanager.BalancedIncrementalQuantileFilter).

    Parameters
    ----------
    budget : float, optional (default=None)
        The budget which models the budgeting constraint used in
        the stream-based active learning setting.
    budget_manager : BudgetManager, optional (default=None)
        The BudgetManager which models the budgeting constraint used in
        the stream-based active learning setting. if set to None,
        BalancedIncrementalQuantileFilter will be used by default. The budget
        manager will be initialized based on the following conditions:
            If only a budget is given the default budget manager is initialized
            with the given budget.
            If only a budget manager is given use the budget manager.
            If both are not given the default budget manager with the
            default budget.
            If both are given and the budget differs from budgetmanager.budget
            a warning is thrown.
    metric : str or callable, optional (default=None)
        The metric must a be None or a valid kernel as defined by the function
        `sklearn.metrics.pairwise.pairwise_kernels`. The kernel is used to
        calculate the frequency of labels near the candidates and multiplied
        with the probabilities returned by the `clf` to get a kernel frequency
        estimate for each class.
        If metric is set to None, the `predict_freq` function of the `clf` will
        be used instead. If this is not defined, an Exception is raised.
    metric_dict : dict, optional (default=None)
        Any further parameters are passed directly to the kernel function.
        If metric_dict is None and metric is 'rbf' metric_dict is set to
        {'gamma': 'mean'}.
    random_state : int, RandomState instance, optional (default=None)
        Controls the randomness of the query strategy.
    prior : float, optional (default=1.0e-3)
        The prior value that is passed onto ProbabilisticAL
        (see pool.ProbabilisticAL).
    m_max : float, optional (default=2)
        The m_max value that is passed onto ProbabilisticAL
        (see pool.ProbabilisticAL).

    References
    ----------
    [1] Kottke, M. (2015). Probabilistic Active Learning in Datastreams. In
        Advances in Intelligent Data Analysis XIV (pp. 145–157). Springer.
    """

    def __init__(
        self,
        budget_manager=None,
        budget=None,
        metric=None,
        metric_dict=None,
        random_state=None,
        prior=1.0e-3,
        m_max=2,
    ):
        super().__init__(budget=budget, random_state=random_state)
        self.budget_manager = budget_manager
        self.prior = prior
        self.m_max = m_max
        self.metric = metric
        self.metric_dict = metric_dict

    def query(
        self,
        candidates,
        clf,
        X=None,
        y=None,
        sample_weight=None,
        fit_clf=False,
        utility_weight=None,
        return_utilities=False,
    ):
        """Ask the query strategy which instances in candidates to acquire.

        Parameters
        ----------
        candidates : {array-like, sparse matrix} of shape
        (n_samples, n_features)
            The instances which may be queried. Sparse matrices are accepted
            only if they are supported by the base query strategy.

        clf : SkactivemlClassifier
            Model implementing the methods `fit` and `predict_proba`. If
            `self.metric` is None, the `clf` must also implement
            `predict_freq`.

        X : array-like of shape (n_samples, n_features), optional
        (default=None)
            Input samples used to fit the classifier.

        y : array-like of shape (n_samples), optional (default=None)
            Labels of the input samples 'X'. There may be missing labels.

        sample_weight : array-like of shape (n_samples,), optional
        (default=None)
            Sample weights for X, used to fit the clf.

        fit_clf : bool,optional (default=False)
            If True, refit the classifier also requires X and y to be given.

        utility_weight : array-like of shape (n_candidate_samples), optional
        (default=None)
            Densities for each sample in `candidates`.

        return_utilities : bool, optional (default=False)
            If true, also return the utilities based on the query strategy.
            The default is False.

        Returns
        -------
        queried_indices : ndarray of shape (n_queried_instances,)
            The indices of instances in candidates which should be queried,
            with 0 <= n_queried_instances <= n_samples.
        utilities: ndarray of shape (n_samples,), optional
            The utilities based on the query strategy. Only provided if
            return_utilities is True.
        """
        (
            candidates,
            clf,
            X,
            y,
            sample_weight,
            fit_clf,
            utility_weight,
            return_utilities,
        ) = self._validate_data(
            candidates=candidates,
            clf=clf,
            X=X,
            y=y,
            sample_weight=sample_weight,
            fit_clf=fit_clf,
            utility_weight=utility_weight,
            return_utilities=return_utilities,
        )
        if self.metric is not None:
            if self.metric_dict is None and self.metric == "rbf":
                self.metric_dict = {"gamma": "mean"}
            pwc = ParzenWindowClassifier(
                metric=self.metric,
                metric_dict=self.metric_dict,
                missing_label=clf.missing_label,
                classes=clf.classes,
            )
            pwc.fit(X=X, y=y, sample_weight=sample_weight)
            n = pwc.predict_freq(candidates).sum(axis=1, keepdims=True)
            pred_proba = clf.predict_proba(candidates)
            k_vec = n * pred_proba
        else:
            k_vec = clf.predict_freq(candidates)

        utilities = cost_reduction(k_vec, prior=self.prior, m_max=self.m_max)

        utilities *= utility_weight

        queried_indices = self.budget_manager_.query_by_utility(utilities)

        if return_utilities:
            return queried_indices, utilities
        else:
            return queried_indices

    def update(
        self, candidates, queried_indices, budget_manager_param_dict=None
    ):
        """Updates the budget manager.

        Parameters
        ----------
        candidates : {array-like, sparse matrix} of shape
        (n_samples, n_features)
            The instances which could be queried. Sparse matrices are accepted
            only if they are supported by the base query strategy.

        queried_indices : array-like of shape (n_samples,)
            Indicates which instances from candidates have been queried.

        budget_manager_param_dict : kwargs, optional (default=None)
            Optional kwargs for budgetmanager.

        Returns
        -------
        self : StreamProbabilisticAL
            PALS returns itself, after it is updated.
        """
        # check if a budgetmanager is set
        if not hasattr(self, "budget_manager_"):
            check_type(
                self.budget_manager,
                "budget_manager_",
                BudgetManager,
                type(None),
            )
            self.budget_manager_ = check_budget_manager(
                self.budget,
                self.budget_manager,
                BalancedIncrementalQuantileFilter,
            )
        budget_manager_param_dict = (
            {}
            if budget_manager_param_dict is None
            else budget_manager_param_dict
        )
        call_func(
            self.budget_manager_.update,
            candidates=candidates,
            queried_indices=queried_indices,
            **budget_manager_param_dict
        )
        return self

    def _validate_data(
        self,
        candidates,
        clf,
        X,
        y,
        sample_weight,
        fit_clf,
        utility_weight,
        return_utilities,
        reset=True,
        **check_candidates_params
    ):
        """Validate input data and set or check the `n_features_in_` attribute.

        Parameters
        ----------
        candidates: array-like, shape (n_candidates, n_features)
            Candidate samples.
        clf : SkactivemlClassifier
            Model implementing the methods `fit` and `predict_proba`. If
            `self.metric` is None, the `clf` must also implement
            `predict_freq`.
        X : array-like of shape (n_samples, n_features)
            Input samples used to fit the classifier.
        y : array-like of shape (n_samples)
            Labels of the input samples 'X'. There may be missing labels.
        sample_weight : array-like of shape (n_samples,)
            Sample weights for X, used to fit the clf.
        fit_clf : bool,
            If true, refit the classifier also requires X and y to be given.
        utility_weight: array-like of shape (n_candidate_samples)
            Densities for each sample in `candidates`.
        return_utilities : bool,
            If true, also return the utilities based on the query strategy.
        reset : bool, optional (default=True)
            Whether to reset the `n_features_in_` attribute.
            If False, the input will be checked for consistency with data
            provided when reset was last True.
        **check_candidates_params : kwargs
            Parameters passed to :func:`sklearn.utils.check_array`.

        Returns
        -------
        candidates: np.ndarray, shape (n_candidates, n_features)
            Checked candidate samples
        clf : SkactivemlClassifier
            Checked model implementing the methods `fit` and `predict_freq`.
        X: np.ndarray, shape (n_samples, n_features)
            Checked training samples
        y: np.ndarray, shape (n_candidates)
            Checked training labels
        sampling_weight: np.ndarray, shape (n_candidates)
            Checked training sample weight
        fit_clf : bool,
            Checked boolean value of `fit_clf`
        utility_weight: array-like of shape (n_candidate_samples)
            Checked densities for each sample in `candidates`.
        candidates: np.ndarray, shape (n_candidates, n_features)
            Checked candidate samples
        return_utilities : bool,
            Checked boolean value of `return_utilities`.
        """
        candidates, return_utilities = super()._validate_data(
            candidates,
            return_utilities,
            reset=reset,
            **check_candidates_params
        )
        # check if a budgetmanager is set

        if not hasattr(self, "budget_manager_"):
            check_type(
                self.budget_manager,
                "budget_manager_",
                BudgetManager,
                type(None),
            )
            self.budget_manager_ = check_budget_manager(
                self.budget,
                self.budget_manager,
                BalancedIncrementalQuantileFilter,
            )

        X, y, sample_weight = self._validate_X_y_sample_weight(
            X, y, sample_weight
        )
        clf = self._validate_clf(clf, X, y, sample_weight, fit_clf)
        utility_weight = self._validate_utility_weight(
            utility_weight, candidates
        )

        if self.metric is None and not hasattr(clf, "predict_freq"):
            raise TypeError(
                "clf has no predict_freq and metric was set to None"
            )

        check_scalar(
            self.prior, "prior", float, min_val=0, min_inclusive=False
        )
        check_scalar(self.m_max, "m_max", int, min_val=0, min_inclusive=False)
        self._validate_random_state()

        return (
            candidates,
            clf,
            X,
            y,
            sample_weight,
            fit_clf,
            utility_weight,
            return_utilities,
        )

    def _validate_X_y_sample_weight(self, X, y, sample_weight):
        """Validate if X, y and sample_weight are numeric and of equal length.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            Input samples used to fit the classifier.
        y : array-like of shape (n_samples)
            Labels of the input samples 'X'. There may be missing labels.
        sample_weight : array-like of shape (n_samples,)
            Sample weights for X, used to fit the clf.

        Returns
        -------
        X : array-like of shape (n_samples, n_features)
            Checked Input samples.
        y : array-like of shape (n_samples)
            Checked Labels of the input samples 'X'. Converts y to a numpy
            array
        """
        if sample_weight is not None:
            sample_weight = np.array(sample_weight)
            check_consistent_length(sample_weight, y)
        if X is not None and y is not None:
            X = check_array(X)
            y = np.array(y)
            check_consistent_length(X, y)
        return X, y, sample_weight

    def _validate_clf(self, clf, X, y, sample_weight, fit_clf):
        """Validate if clf is a valid SkactivemlClassifier. If clf is
        untrained, clf is trained using X, y and sample_weight.

        Parameters
        ----------
        clf : SkactivemlClassifier
            Model implementing the methods `fit` and `predict_freq`.
        X : array-like of shape (n_samples, n_features)
            Input samples used to fit the classifier.
        y : array-like of shape (n_samples)
            Labels of the input samples 'X'. There may be missing labels.
        sample_weight : array-like of shape (n_samples,)
            Sample weights for X, used to fit the clf.

        Returns
        -------
        clf : SkactivemlClassifier
            Checked model implementing the methods `fit` and `predict_freq`.
        """
        # Check if the classifier and its arguments are valid.
        check_type(clf, "clf", SkactivemlClassifier)
        check_type(fit_clf, "fit_clf", bool)
        if fit_clf:
            if sample_weight is None:
                clf = clone(clf).fit(X, y)
            else:
                clf = clone(clf).fit(X, y, sample_weight)
        return clf

    def _validate_utility_weight(self, utility_weight, candidates):
        """Validate if utility_weight is numeric and of equal length as
        candidates.

        Parameters
        ----------
        candidates: np.ndarray, shape (n_candidates, n_features)
            Checked candidate samples
        utility_weight: array-like of shape (n_candidate_samples)
            Densities for each sample in `candidates`.

        Returns
        -------
        utility_weight : array-like of shape (n_candidate_samples)
            Checked densities for each sample in `candidates`.
        """
        if utility_weight is None:
            utility_weight = np.ones(len(candidates))
        utility_weight = check_array(utility_weight, ensure_2d=False)
        check_consistent_length(utility_weight, candidates)
        return utility_weight

    def _validate_random_state(self):
        """Creates a copy 'random_state_' if random_state is an instance of
        np.random_state. If not create a new random state. See also
        :func:`~sklearn.utils.check_random_state`
        """
        if not hasattr(self, "random_state_"):
            self.random_state_ = self.random_state
        self.random_state_ = check_random_state(self.random_state_)
