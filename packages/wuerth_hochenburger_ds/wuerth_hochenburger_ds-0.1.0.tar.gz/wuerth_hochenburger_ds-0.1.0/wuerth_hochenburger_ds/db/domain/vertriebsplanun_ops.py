"""
This File is (semi) machine generated.
.\venv\Scripts\python.exe -m pwiz -e postgresql -u schwarz  -p 5432 -H WHDEV01 -s dwh -P 'Asdf' dwh_dev
"""
from dynaconf import Dynaconf
from peewee import *
from playhouse.pool import PooledPostgresqlDatabase


__all__ = [
    'CustomerAdditionalInfo', 'CustomerReport', 'CustomerReportQuestions', 'IgnoreVtc4Kundenbetreuung',
    'MapCustomerAgent', 'MapCustomerBoAgent', 'MapCustomerBranch', 'TargetDiscounts', 'YearlyPlanning', 'Years'
]

settings = Dynaconf(
    envvar_prefix="DB",
    load_dotenv=True
)

database = PooledPostgresqlDatabase(
    settings.DB,
    user=settings.USER,
    password=settings.PW,
    host=settings.HOST,
    port=5432
)

class BaseModel(Model):
    class Meta:
        database = database

class CustomerAdditionalInfo(BaseModel):
    is_report_required = BooleanField(constraints=[SQL("DEFAULT true")])
    kunden_nr = TextField()
    mandant = TextField()

    class Meta:
        table_name = 'customer_additional_info'
        indexes = (
            (('mandant', 'kunden_nr'), True),
        )
        schema = 'vertriebsplanung_ops'
        primary_key = CompositeKey('kunden_nr', 'mandant')

class CustomerReport(BaseModel):
    answer = TextField()
    created_on = DateTimeField(constraints=[SQL("DEFAULT now()")])
    fk_customer_report_questions_id = TextField()
    is_valid = BooleanField()
    kunden_nr = TextField()
    mandant = TextField()
    modified_on = DateTimeField(constraints=[SQL("DEFAULT now()")])
    report_date = DateTimeField()

    class Meta:
        table_name = 'customer_report'
        indexes = (
            (('mandant', 'kunden_nr', 'report_date', 'fk_customer_report_questions_id'), True),
        )
        schema = 'vertriebsplanung_ops'
        primary_key = CompositeKey('fk_customer_report_questions_id', 'kunden_nr', 'mandant', 'report_date')

class CustomerReportQuestions(BaseModel):
    created_on = DateTimeField(constraints=[SQL("DEFAULT now()")])
    id = TextField(primary_key=True)
    is_aktiv = BooleanField()
    max_laenge = IntegerField(null=True)
    min_laenge = IntegerField(null=True)
    modified_on = DateTimeField(constraints=[SQL("DEFAULT now()")])
    text = TextField(null=True)

    class Meta:
        table_name = 'customer_report_questions'
        schema = 'vertriebsplanung_ops'

class IgnoreVtc4Kundenbetreuung(BaseModel):
    mandant = TextField(null=True)
    vertreter = TextField(null=True)
    vtc = TextField(null=True)

    class Meta:
        table_name = 'ignore_vtc_4_kundenbetreuung'
        indexes = (
            (('mandant', 'vtc'), True),
        )
        schema = 'vertriebsplanung_ops'
        primary_key = False

class MapCustomerAgent(BaseModel):
    kunden_nr = TextField()
    mandant = TextField()
    vtc1 = TextField(null=True)

    class Meta:
        table_name = 'map_customer_agent'
        indexes = (
            (('mandant', 'kunden_nr'), True),
            (('mandant', 'kunden_nr'), True),
        )
        schema = 'vertriebsplanung_ops'
        primary_key = CompositeKey('kunden_nr', 'mandant')

class MapCustomerBoAgent(BaseModel):
    kunden_nr = TextField()
    mandant = TextField()
    verkaeufer_nr = TextField(null=True)

    class Meta:
        table_name = 'map_customer_bo_agent'
        indexes = (
            (('mandant', 'kunden_nr'), True),
            (('mandant', 'kunden_nr'), True),
        )
        schema = 'vertriebsplanung_ops'
        primary_key = CompositeKey('kunden_nr', 'mandant')

class MapCustomerBranch(BaseModel):
    filiale_nr = TextField(null=True)
    kunden_nr = TextField()
    mandant = TextField()

    class Meta:
        table_name = 'map_customer_branch'
        indexes = (
            (('mandant', 'kunden_nr'), True),
            (('mandant', 'kunden_nr'), True),
        )
        schema = 'vertriebsplanung_ops'
        primary_key = CompositeKey('kunden_nr', 'mandant')

class TargetDiscounts(BaseModel):
    fk_customer_rating_label_id = BigIntegerField(null=True)
    fk_gewerk_id = BigIntegerField(null=True)
    fk_pricing_zone_id = BigIntegerField(null=True)
    kunden_grp_nr = TextField(null=True)
    mandant = TextField(null=True)
    rabat = DoubleField(null=True)
    rabat_grp_nr = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'target_discounts'
        schema = 'vertriebsplanung_ops'

class YearlyPlanning(BaseModel):
    created_on = DateTimeField(constraints=[SQL("DEFAULT now()")], null=True)
    fk_cc_groups_id = BigIntegerField(null=True)
    fk_years_jahr = IntegerField()
    kunden_nr = TextField()
    mandant = TextField()
    massnahmen = TextField(null=True)
    modified_on = DateTimeField(constraints=[SQL("DEFAULT now()")], null=True)
    pk = TextField(primary_key=True)
    planhandelsspanne = DoubleField(null=True)
    planumsatz = BigIntegerField(null=True)
    umsatz_prognose = BigIntegerField(null=True)

    class Meta:
        table_name = 'yearly_planning'
        indexes = (
            (('mandant', 'kunden_nr', 'fk_years_jahr', 'fk_cc_groups_id'), True),
        )
        schema = 'vertriebsplanung_ops'

class Years(BaseModel):
    jahr = AutoField()
    kundenzuordnung_editable = BooleanField(constraints=[SQL("DEFAULT true")], null=True)
    planumsatz_editable = BooleanField(constraints=[SQL("DEFAULT true")], null=True)
    umsatz_schaetzung_isvisible = BooleanField(constraints=[SQL("DEFAULT true")], null=True)

    class Meta:
        table_name = 'years'
        schema = 'vertriebsplanung_ops'

