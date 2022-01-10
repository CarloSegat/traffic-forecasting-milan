import os
import matplotlib.pyplot as plt

from settings import DATADIR, COMPUTEDDIR, RAW_HOUR_AGGREGATION_FILE, Z_NORMALISED_HOUR_AGGREGATION_FILE, \
    Z_NORMALISED_HOUR_FILE, ID_TRAFFIC_MAP_FILE, LINEAR_REGRESSION_FILE, TRAFFIC_TYPES, HIGH_CELL_ID
from src.abstract.stage import Stage
from src.abstract.stage_output import StageOutput
from src.stages.aggregate_cell import AggregateCell
from src.stages.aggregate_timestamp import AggregateTimestamp
from src.stages.augmented_lr import PerformAugmentedLinearRegression
from src.stages.create_features import CreateFeatures
from src.stages.full_aggregation_hour import FullHourAggregation
from src.stages.load_data import LoadData
from src.abstract.pipeline import Pipeline
from src.stages.merge_files import MergeFiles
from src.stages.no_negative import NoNegative
from src.stages.one_hot_encoder import OneHotEncode
from src.stages.perform_dickey_fuller import PerformDickeyFuller
from src.stages.perform_linear_regression import PerformLinearRegression
from src.stages.plot_acf_pacf import PlotACF
from src.stages.plot_global_cf import PlotGlobalCF
from src.stages.run_ar_model import RunARModel
from src.stages.tbats import RunTBATS
from src.stages.train_data_augmented_lr import MakeTrainDataAugmentedLR
from src.stages.train_test_split import TestTrainSplit
from src.stages.z_normalise_traffic import ZNormaliseTraffics
from src.stages.plot_geo import PlotGeo
from src.stages.plot_hourly_weekend import PlotHourlyWeekend
from src.stages.plot_mean_day import PlotMeanDay


def ensure_aggregation_exists():
    if os.path.exists(RAW_HOUR_AGGREGATION_FILE):
        print(f"Aggregated data exists af location: {RAW_HOUR_AGGREGATION_FILE}")
    else:
        pipeline = Pipeline("Aggregate raw data hourly")
        pipeline.add_stage(FullHourAggregation(DATADIR, 'sms-call-internet-mi-2013-*.txt'))
        pipeline.run()


def ensure_znormalised_aggregated_exists():
    if os.path.exists(Z_NORMALISED_HOUR_AGGREGATION_FILE):
        print(f"Normalised-aggregated data exists af location: {Z_NORMALISED_HOUR_AGGREGATION_FILE}")
    else:
        pipeline = Pipeline("Z normalisation-hour-aggregation")
        pipeline.add_stage(LoadData(RAW_HOUR_AGGREGATION_FILE))
        pipeline.add_stage(AggregateTimestamp())
        # pipeline.add_stage(ComputeStats())
        pipeline.add_stage(ZNormaliseTraffics())
        pipeline.run()
        pipeline.get().to_csv(Z_NORMALISED_HOUR_AGGREGATION_FILE, index=True)


def plot_daily_pattern(begin):
    pipeline = Pipeline("Compute mean plot")
    pipeline.add_stage(LoadData(Z_NORMALISED_HOUR_AGGREGATION_FILE))
    pipeline.add_stage(PlotMeanDay(3, begin))
    # pipeline.add_stage(LoadData(DATADIR, 'sms-call-internet-mi*.txt'))
    # pipeline.add_stage(ComputeStats())
    pipeline.run()
    pipeline.get().get_figure().savefig(COMPUTEDDIR + f'/3_days_hourly_from_{begin}.png')


def plot_weekday_vs_weekend():
    pipeline = Pipeline("Weekday vs weekend")
    pipeline.add_stage(LoadData(Z_NORMALISED_HOUR_AGGREGATION_FILE))
    pipeline.add_stage(CreateFeatures())
    pipeline.add_stage(PlotHourlyWeekend())
    pipeline.run()
    pipeline.get().get_figure().savefig(COMPUTEDDIR + '/weekday_vs_weekend.png')


def plot_geo_heatmap():
    pipeline = Pipeline("Spatial plot")
    pipeline.add_stage(LoadData(RAW_HOUR_AGGREGATION_FILE))
    pipeline.add_stage(AggregateCell())
    pipeline.add_stage(PlotGeo())
    pipeline.run()


def ensure_square_mean_traffic_file():
    if os.path.exists(ID_TRAFFIC_MAP_FILE):
        print(f"Square ID to mean-aggregated traffic exists af location: {ID_TRAFFIC_MAP_FILE}")
    else:
        pipeline = Pipeline("Create square_id to mean traffic csv")
        pipeline.add_stage(LoadData(RAW_HOUR_AGGREGATION_FILE))
        pipeline.add_stage(AggregateCell())
        pipeline.run()
        pipeline.get()[['mean', 'square_id']].to_csv(ID_TRAFFIC_MAP_FILE, index=False)

def ensure_non_aggregated_normalised_file():
    if os.path.exists(Z_NORMALISED_HOUR_FILE):
        print(f"Normalised data exists af location: {Z_NORMALISED_HOUR_FILE}")
    else:
        pipeline = Pipeline("Ensure NON-aggregated normalised data exists")
        pipeline.add_stage(LoadData(RAW_HOUR_AGGREGATION_FILE))
        pipeline.add_stage(ZNormaliseTraffics(remove_square_id=False))
        pipeline.add_stage(CreateFeatures(features=['hour', 'day', 'national_holidays']))
        pipeline.run()
        df = pipeline.get()
        # df = df.drop(columns=['timestamp'])
        df.to_csv(Z_NORMALISED_HOUR_FILE, index=False)
        print(3)

def ensure_lr_file():
    if os.path.exists(LINEAR_REGRESSION_FILE):
        print(f"File for linear regression exists af location: {LINEAR_REGRESSION_FILE}")
    else:
        pipeline = Pipeline("Prepare data for linear regression")
        pipeline.add_stage(MergeFiles())
        pipeline.add_stage(NoNegative())
        pipeline.add_stage(OneHotEncode(['day', 'hour', 'national_holiday']))
        pipeline.run()
        pipeline.get().to_csv(LINEAR_REGRESSION_FILE, index=False)


class PlotPredicitonResults(Stage):

    def __init__(self, plot_title):
        self.plot_title = plot_title

    def compute(self, previous: StageOutput) -> StageOutput:
        # previous.get_data().mean_abs_percent_error
        # previous.get_data().rmse
        # previous.get_data().residuals
        for f in TRAFFIC_TYPES:
            plt.figure(figsize=(10, 4))
            plt.plot(previous.get_data().y_test[f])
            plt.plot(previous.get_data().predictions[f])
            plt.legend(("Data", "Predictions"))
            plt.title(self.plot_title + f" for {f}\n RMSE: {previous.get_data().rmse[f]}")
            plt.savefig(os.path.join(COMPUTEDDIR, self.plot_title + f'_{f}'))


def run_lr(cell_id):
    pipeline = Pipeline("Linear Regression")
    pipeline.add_stage(LoadData(LINEAR_REGRESSION_FILE))
    pipeline.add_stage(TestTrainSplit(TRAFFIC_TYPES, cell_id))
    pipeline.add_stage(PerformLinearRegression())
    pipeline.add_stage(PlotPredicitonResults(f'lr/lr_{cell_id}'))
    pipeline.run()


def plot_acf_and_pacf(cell_id):
    pipeline = Pipeline(f"ACF & PACF plots for cell id {cell_id}")
    pipeline.add_stage(LoadData(LINEAR_REGRESSION_FILE))
    pipeline.add_stage(PerformDickeyFuller(cell_id))
    pipeline.add_stage(PlotACF(cell_id))
    pipeline.run()

def plot_global_cf():
    pipeline = Pipeline(f"ACF & PACF global")
    pipeline.add_stage(LoadData(Z_NORMALISED_HOUR_AGGREGATION_FILE))
    pipeline.add_stage(PlotGlobalCF())
    pipeline.run()

def run_ar(order, cell_id):
    pipeline = Pipeline(f"AR Model, single cell")
    pipeline.add_stage(LoadData(Z_NORMALISED_HOUR_FILE))
    pipeline.add_stage(RunARModel(order, cell_id))
    pipeline.add_stage(PlotPredicitonResults(f'ar/ar_{order}_{cell_id}'))
    pipeline.run()

def run_augmented_lr(cell_id, model):
    pipeline = Pipeline("Augmented Linear Regression")
    pipeline.add_stage(LoadData(LINEAR_REGRESSION_FILE))
    pipeline.add_stage(MakeTrainDataAugmentedLR(cell_id))
    pipeline.add_stage(TestTrainSplit(TRAFFIC_TYPES, cell_id))
    pipeline.add_stage(PerformAugmentedLinearRegression(model))
    pipeline.add_stage(PlotPredicitonResults(f'lr_augmented/lr_{cell_id}'))
    pipeline.run()


### preprocessing & visualisation
ensure_aggregation_exists()
ensure_znormalised_aggregated_exists()
plot_daily_pattern(0)
plot_daily_pattern(58)
plot_weekday_vs_weekend()
plot_geo_heatmap()
ensure_square_mean_traffic_file()
ensure_non_aggregated_normalised_file()
ensure_lr_file()

# run_lr(LOW_CELL_ID, True)
# run_lr(HIGH_CELL_ID, True)

# plot_acf_and_pacf(high_traffic_cell_id)
# plot_acf_and_pacf(low_traffic_cell_id)
# plot_global_cf()


# run_ar(14, HIGH_CELL_ID)
# run_ar(14, LOW_CELL_ID)
# run_ar(28, HIGH_CELL_ID)
# run_ar(28, LOW_CELL_ID)

# run_augmented_lr(LOW_CELL_ID, Ridge(alpha=0.1))
# run_augmented_lr(HIGH_CELL_ID, Lasso(alpha=0.2))

pipeline = Pipeline("Test Integerated")
pipeline.add_stage(LoadData(LINEAR_REGRESSION_FILE))

# pipeline.add_stage(TestIntegratedARIMA(LOW_CELL_ID))


pipeline.add_stage(RunTBATS(HIGH_CELL_ID))
pipeline.run()