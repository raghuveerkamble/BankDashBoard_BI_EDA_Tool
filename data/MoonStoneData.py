
# =============================================================================
# Master Data File
# =============================================================================

import pandas as pd
import numpy as np
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)


# =============================================================================
# Data
# =============================================================================


csv_file = "data/Dec22a.csv"
csv_data = pd.read_csv(csv_file)
table = pd.DataFrame(csv_data)

MoonStoneData = DplyFrame(table)