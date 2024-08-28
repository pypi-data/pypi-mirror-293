# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
from .api import quantim

class returns(quantim):
    def __init__(self, username, password, secretpool, env="pdn", api_url=None):
        super().__init__(username, password, secretpool, env, api_url)

    def expected_returns(self, ref_curr, views_df, tickers=None, assets=None, horizon_in_months=12, views_conf=0.75, conf_interv=0.75, median=True, period="monthly", since_date="2008-01-01"):
        '''
        Estimate expected returns.
        '''
        views = views_df.to_dict(orient="records")
        data = {'ref_curr':ref_curr, 'views':views, "ref_curr":ref_curr, "tickers":tickers, "assets":assets, "horizon_in_months":horizon_in_months, "views_conf":views_conf, "conf_interv":conf_interv, "median":median, "period":period, "since_date":since_date}
        try:
            resp = self.api_call('expected_returns', method="post", data=data, verify=False)
        except:
            resp = {'success':False, 'message':'Check permissions!'}

        exp_ret, views_df = pd.DataFrame(resp['expected_rets']), pd.Series(resp['views_abs'])

        return exp_ret, views_df