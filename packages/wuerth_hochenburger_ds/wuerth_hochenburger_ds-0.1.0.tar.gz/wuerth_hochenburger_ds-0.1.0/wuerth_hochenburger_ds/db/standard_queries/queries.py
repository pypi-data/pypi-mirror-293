import os
from dataclasses import dataclass
from hashlib import md5
from typing import Optional, Union

import pandas as pd
import datetime as dt
import pickle

from peewee import JOIN

from ..domain import *

__all__ = ['Queries']


class Queries:

    @dataclass
    class CacheDump:
        valid_until: dt.datetime
        df: pd.DataFrame

    def __init__(self, cache_validity_minutes: int = 60*12, do_dump_cache: bool = True, do_load_cache: bool = True):
        self._df = None
        self.query_hash = None
        self._query = None
        self.do_dump_cache = do_dump_cache
        self.do_load_cache = do_load_cache
        self.cache_validity_minutes = cache_validity_minutes

    def select(self, *select):
        self._query = SaleTransactions.select(*select)

    def join(self, table, lon, ron, how=None):
        if how is None or how == 'inner':
            join_type = JOIN.INNER
        elif how == 'left':
            join_type = JOIN.LEFT_OUTER
        elif how == 'right':
            join_type = JOIN.RIGHT_OUTER
        elif how == 'full':
            join_type = JOIN.FULL_OUTER
        else:
            raise ValueError(f'Unknown join type: {how}')

        assert len(lon) >= 1, 'Length of lon must be greater than 0'
        assert len(lon) == len(ron), 'Length of lon and ron must be equal'
        on = lon[0] == ron[0]
        for i in range(1, len(lon)):
            on = on & (lon[i] == ron[i])

        self._query = self._query.join(
            table,
            on=on,
            join_type=join_type
        )

    def join_articles(self, how: Optional[str] = None):
        self.join(
            table=Articles,
            lon=[Articles.mandant, Articles.artikel_nr],
            ron=[SaleTransactions.mandant, SaleTransactions.artikel_nr],
            how=how,
        )

    def join_customers(self, how: Optional[str] = None):
        self.join(
            table=Customers,
            lon=[Customers.mandant, Customers.nr],
            ron=[SaleTransactions.mandant, SaleTransactions.kunden_nr],
            how=how,
        )

    def join_discountgroups(self, how: Optional[str] = None):
        self.join(
            table=Discountgroups,
            lon=[Discountgroups.mandant, Discountgroups.rabat_grp_nr],
            ron=[Articles.mandant, Articles.rabat_grp_nr],
            how=how,
        )

    def join_article_groups(self, how: Optional[str] = None):
        self.join(
            table=ArticleGroups,
            lon=[ArticleGroups.mandant, ArticleGroups.artikel_grp_nr],
            ron=[Articles.mandant, Articles.artikel_grp_nr],
            how=how,
        )

    # noinspection DuplicatedCode
    def join_branches(self, on: Optional[str] = None, how: Optional[str] = None):
        if on is None or on == 'st':
            self.join(
                table=Branches,
                lon=[Branches.mandant, Branches.filiale_nr],
                ron=[SaleTransactions.mandant, SaleTransactions.filiale_nr],
                how=how,
            )
        elif on == 'cu':
            self.join(
                table=Branches,
                lon=[Branches.mandant, Branches.filiale_nr],
                ron=[Customers.mandant, Customers.filiale_nr],
                how=how,
            )
        else:
            raise ValueError(f'Unknown on value: {on}. Exptected "st" (Transactions) or "cu" (Customers)')

    # noinspection DuplicatedCode
    def join_agents(self, on: Optional[str] = None, how: Optional[str] = None):
        if on is None or on == 'st':
            self.join(
                table=Agents,
                lon=[Agents.mandant, Agents.vtc],
                ron=[SaleTransactions.mandant, SaleTransactions.vtc1],
                how=how,
            )
        elif on == 'cu':
            self.join(
                table=Agents,
                lon=[Agents.mandant, Agents.vtc],
                ron=[Customers.mandant, Customers.vtc1],
                how=how,
            )
        else:
            raise ValueError(f'Unknown on value: {on}. Exptected "st" (Transactions) or "cu" (Customers)')

    # noinspection DuplicatedCode
    def join_bo_agents(self, on: Optional[str] = None, how: Optional[str] = None):
        if on is None or on == 'st':
            self.join(
                table=BoAgents,
                lon=[BoAgents.mandant, BoAgents.verkaeufer_nr],
                ron=[SaleTransactions.mandant, SaleTransactions.verkaeufer_nr1],
                how=how,
            )
        elif on == 'cu':
            self.join(
                table=BoAgents,
                lon=[BoAgents.mandant, BoAgents.verkaeufer_nr],
                ron=[Customers.mandant, Customers.verkaeufer_nr1],
                how=how,
            )
        else:
            raise ValueError(f'Unknown on value: {on}. Exptected "st" (Transactions) or "cu" (Customers)')

    def join_report_key(self, on: Optional[str] = None, how: Optional[str] = None):
        if on is None or on == 'st':
            self.join(
                table=MapBranchReportKey,
                lon=[MapBranchReportKey.mandant, MapBranchReportKey.filiale_nr],
                ron=[SaleTransactions.mandant, SaleTransactions.filiale_nr],
                how=how,
            )
            self.join(
                table=ReportKeys,
                lon=[ReportKeys.id],
                ron=[MapBranchReportKey.fk_report_key_id],
                how=how,
            )
        elif on == 'cu':
            self.join(
                table=MapBranchReportKey,
                lon=[MapBranchReportKey.mandant, MapBranchReportKey.filiale_nr],
                ron=[Customers.mandant, Customers.filiale_nr],
                how=how,
            )
            self.join(
                table=ReportKeys,
                lon=[ReportKeys.id],
                ron=[MapBranchReportKey.fk_report_key_id],
                how=how,
            )
        else:
            raise ValueError(f'Unknown on value: {on}. Exptected "st" (Transactions) or "cu" (Customers)')

    def join_gewerke(self, on: Optional[str] = None, how: Optional[str] = None):
        if on is None or on == 'cu':
            self.join(
                table=MapCustomerGewerk,
                lon=[MapCustomerGewerk.mandant, MapCustomerGewerk.kunden_nr],
                ron=[Customers.mandant, Customers.nr],
                how=how,
            )
            self.join(
                table=Gewerke,
                lon=[Gewerke.id],
                ron=[MapCustomerGewerk.fk_gewerk_id],
                how=how,
            )
        elif on == 'ag':
            self.join(
                table=MapArticleGroupCcGroupGewerk,
                lon=[MapArticleGroupCcGroupGewerk.mandant, MapArticleGroupCcGroupGewerk.artikel_grp_nr],
                ron=[ArticleGroups.mandant, ArticleGroups.artikel_grp_nr],
                how=how,
            )
            self.join(
                table=Gewerke,
                lon=[Gewerke.id],
                ron=[MapArticleGroupCcGroupGewerk.fk_gewerk_id],
                how=how,
            )
        else:
            raise ValueError(f'Unknown on value: {on}. Exptected "cu" (Customers) or "ag" (ArticleGroups)')

    def where_mandant(self, mandant: str):
        self._query = self._query.where(SaleTransactions.mandant == str(mandant))

    def where_date(
            self,
            date_from: Optional[Union[dt.date, str, dt.datetime]] = None,
            date_to: Optional[Union[dt.date, str, dt.datetime]] = None
    ):
        if date_from is not None:
            self._query = self._query.where(SaleTransactions.rechnungs_date >= date_from)
        if date_to is not None:
            self._query = self._query.where(SaleTransactions.rechnungs_date <= date_to)

    def where_gewerbe(self, is_gewerbe: bool):
        if is_gewerbe:
            self._query = self._query.where(~Customers.auswertungs_key.like('P%'))
        else:
            self._query = self._query.where(Customers.auswertungs_key.like('P%'))

    def join_standard(self):
        self.join_customers()
        self.join_articles()
        self.join_article_groups()

    def where(self, condition):
        self._query = self._query.where(condition)

    def group_by(self, *args):
        self._query = self._query.group_by(*args)

    @property
    def query(self):
        return self._query

    def set_query(self, query):
        self._query = query

    def dump2cache(self):
        os.makedirs('cache', exist_ok=True)
        d = self.CacheDump(
            valid_until=dt.datetime.now() + dt.timedelta(minutes=self.cache_validity_minutes),
            df=self.df,
        )
        os.makedirs('cache', exist_ok=True)
        with open(f'cache/{self.query_hash}.pkl', 'wb') as f:
            pickle.dump(d, f)

    def load_cache(self):
        if not os.path.exists(f'cache/{self.query_hash}.pkl'):
            return False
        with open(f'cache/{self.query_hash}.pkl', 'rb') as f:
            d = pickle.load(f)
        try:
            if d.valid_until < dt.datetime.now():
                return False
            self._df = d.df
            return True
        except AttributeError:
            return False

    @staticmethod
    def clear_cache(invalid_only: bool = True):
        file_list = [f for f in os.listdir('cache') if f.endswith(".pkl")]
        for f in file_list:
            is_valid = False
            if invalid_only:
                try:
                    with open(os.path.join('cache', f), 'rb') as h:
                        d = pickle.load(h)
                        is_valid = (d.valid_until >= dt.datetime.now())
                except Exception as e:  # noqa
                    is_valid = False
            if not is_valid:
                os.remove(os.path.join('cache', f))

    def execute(self):
        # md5 hash of the query
        query_hash = md5(str(self._query).encode()).hexdigest()
        if query_hash != self.query_hash:
            self.query_hash = query_hash
            if not (self.do_load_cache and self.load_cache()):
                df = pd.DataFrame(list(self._query.dicts()))
                if df.empty:
                    df = pd.DataFrame(columns=[c.name for c in self._query.selected_columns])
                self._df = df
                if self.do_dump_cache:
                    self.dump2cache()

    @property
    def df(self) -> pd.DataFrame:
        self.execute()
        return self._df.copy()

    @staticmethod
    def _sanitize_filename(filename: str):
        filename = filename.replace(' ', '_').replace(':', '_').replace('-', '_')
        if not filename.endswith('.pkl'):
            filename += '.pkl'
        return filename

    def dump(self, filename: str):
        with open(self._sanitize_filename(filename), 'wb') as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filename: str):
        with open(cls._sanitize_filename(filename), 'rb') as f:
            return pickle.load(f)
