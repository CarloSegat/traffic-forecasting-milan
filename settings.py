import os
from datetime import datetime, timedelta

HOMEDIR = os.path.abspath(os.path.join(__file__, '..'))
DATADIR = os.path.join(HOMEDIR, 'data')
COMPUTEDDIR = os.path.join(HOMEDIR, 'computed')

TRAFFIC_TYPES = ['sms_in', 'sms_out', 'call_in', 'call_out', 'internet']

# data aggregated by hour, sum of values within 1 hour range
RAW_HOUR_AGGREGATION_FILE = os.path.join(COMPUTEDDIR, 'h-aggregated.csv')

Z_NORMALISED_HOUR_AGGREGATION_FILE = os.path.join(COMPUTEDDIR, 'znorm-h-aggregated.csv')
Z_NORMALISED_HOUR_FILE = os.path.join(COMPUTEDDIR, 'znorm-nonaggregated.csv')

ID_TRAFFIC_MAP_FILE = os.path.join(COMPUTEDDIR, 'square_id_mean_traffic.csv')
LINEAR_REGRESSION_FILE = os.path.join(COMPUTEDDIR, 'linear_regression.csv')
REDUCED_LINEAR_REGRESSION_FILE = os.path.join(COMPUTEDDIR, 'reduced_lr.csv')

EPSILON =  1e-10

HIGH_CELL_ID = 5161
LOW_CELL_ID = 1207


national_holidays = [(1, 11), (8, 12), (25, 12), (26,12), (31,12)]
training_days = int(61 * 0.8)
test_days = 61 - training_days
start_timestamp = datetime(2013, 11, 1, 0, 0, 0)
end_timestamp = datetime(2013, 12, 31, 23, 0, 0)
end_training = start_timestamp + timedelta(days=training_days)

def get_adjacent_cell_ids(cell_id):

        up_down = -100 if cell_id > 100 else 100
        left_right = -1 if cell_id % 100 == 0 else 1

        if cell_id in [1, 100, 9901, 10000]:
            adj_ids = [cell_id + left_right, cell_id + up_down,
                       cell_id + up_down + left_right]
        elif cell_id > 9901 or cell_id < 100:
            adj_ids = [cell_id + 1, cell_id -1, cell_id + up_down,
                       cell_id + up_down + left_right, cell_id + up_down - left_right]
        elif cell_id % 100 == 0 or cell_id % 100 == 1:
            adj_ids = [cell_id + 100, cell_id - 100, cell_id + left_right,
                       cell_id - up_down + left_right, cell_id + up_down + left_right]
        else:
            adj_ids = [cell_id + 1, cell_id - 1, cell_id + 100, cell_id - 100,
                       cell_id + up_down + left_right, cell_id + up_down - left_right,
                       cell_id - up_down + left_right, cell_id - up_down - left_right]

        return adj_ids

assert set(get_adjacent_cell_ids(1)) == set([2, 101, 102])
assert set(get_adjacent_cell_ids(10000)) == set([9999, 9900, 9899])
assert set(get_adjacent_cell_ids(102)) == set([1,2,3,101,103,201,202,203])