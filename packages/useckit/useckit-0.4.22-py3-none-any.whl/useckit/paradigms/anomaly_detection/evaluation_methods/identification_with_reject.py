import numpy as np

from ._fixed_false_negative_thresholding_method import FixedFalseNegativeThresholdingMethod
from .anomaly_evaluation_method_base import AnomalyBaseEvaluationMethod, BaseThresholdingMethod
from ..prediction_models.anomaly_prediction_model_base import AnomalyBasePredictionModel
from ....evaluation.identification_with_reject import IdentificationOrRejectModel, \
    perform_identification_or_reject_evaluation
from ....util.dataset import Dataset


class AnomalyIdentificationOrRejectModel(IdentificationOrRejectModel):

    def __init__(self,
                 anomaly_prediction_model: AnomalyBasePredictionModel,
                 rejection_thresholds_per_trained_user: dict,
                 dataset: Dataset):
        self.anomaly_prediction_model = anomaly_prediction_model
        self.rejection_thresholds_per_trained_user = rejection_thresholds_per_trained_user
        self.dataset = dataset

    def identify_or_reject(self, samples: np.ndarray):
        preds, labels = self.anomaly_prediction_model.predict(samples)
        preds = preds.transpose()  # 0-axis = samples, 1-axis = the predictions of the different models for the sample

        result = np.argmin(preds, axis=1)  # reduce to the indices of the model with the minimum prediction
        result_index = np.argmin(preds, axis=1)  # and a copy, please
        for i in range(len(result)):
            result[i] = labels[result[i]]  # pick for each sample the label corresponding to the model with the
            # min prediction

        for i in range(len(preds)):  # iterate all samples
            reject = preds[i][result_index[i]] > self.rejection_thresholds_per_trained_user[labels[result_index[i]]]
            if reject:
                result[i] = -1
        return self.dataset.reverse_label_transform(result)


class IdentificationWithReject(AnomalyBaseEvaluationMethod):

    def __init__(self,
                 output_dir: str = "evaluation_identification_with_reject",
                 threshold_method: BaseThresholdingMethod = None):
        super().__init__(output_dir)
        self.threshold_method = threshold_method

    def evaluate(self, dataset: Dataset, prediction_model: AnomalyBasePredictionModel, **kwargs):
        if self.threshold_method is None:
            self.threshold_method = FixedFalseNegativeThresholdingMethod(prediction_model, self.output_dir)
        thresholds = self.threshold_method.compute_thresholds(dataset.testset_enrollment_data,
                                                              dataset.testset_enrollment_labels)
        identification_or_reject_model = AnomalyIdentificationOrRejectModel(prediction_model, thresholds, dataset)
        perform_identification_or_reject_evaluation(identification_or_reject_model, dataset, self.output_dir)
