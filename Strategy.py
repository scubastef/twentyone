from Enums import Action
import os
import numpy as np
import pandas as pd

class PlayerStrategy:
        
    def __init__(self, strategy_path : str) -> None:

        self._hard_totals_table = self._load_strat_table(strategy_path + '/hard_totals.csv')
        self._soft_totals_init_table = self._load_strat_table(strategy_path + '/soft_totals_init.csv')
        self._soft_totals_post_table = self._load_strat_table(strategy_path + '/soft_totals_post.csv')
        self._pair_splitting_table = self._load_strat_table(strategy_path + '/pair_splitting.csv')

    def _load_strat_table(self, table_path : str):
        table = pd.read_csv(table_path, index_col=0)
        table.columns = table.columns.astype(int)

        table[table=='H'] = Action.HIT
        table[table=='S'] = Action.STAND
        table[table=='Y'] = Action.SPLIT
        table[table=='N'] = Action.NO_SPLIT
        table[table=='D'] = Action.DD

        return table
    
    def get_hard_totals_table(self):
        return self._hard_totals_table
    
    def get_soft_totals_init_table(self):
        return self._soft_totals_init_table

    def get_soft_totals_post_table(self):
        return self._soft_totals_post_table

    def get_pair_splitting_table(self):
        return self._pair_splitting_table
    


if __name__ == '__main__':
    sss = PlayerStrategy('Strategies/BasicStrategy')
    df = sss._hard_totals_table.copy()
    print(df)
    df[df=='H'] = Action.HIT
    df[df=='S'] = Action.STAND
    df[df=='D'] = Action.SPLIT
    print(df)
    # print(sss._soft_totals_init_table)
    # print(sss._soft_totals_post_table)
    # print(sss._pair_splitting_table)