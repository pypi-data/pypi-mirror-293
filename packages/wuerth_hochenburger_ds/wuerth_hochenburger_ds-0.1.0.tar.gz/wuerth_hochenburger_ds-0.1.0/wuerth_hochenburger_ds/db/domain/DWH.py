"""
This File is (semi) machine generated.
.\venv\Scripts\python.exe -m pwiz -e postgresql -u schwarz  -p 5432 -H WHDEV01 -s dwh -P 'Asdf' dwh_dev
"""
from dynaconf import Dynaconf
from peewee import *
from playhouse.pool import PooledPostgresqlDatabase


__all__ = [
    'Agents', 'ArticleGroups', 'Articles', 'BoAgents', 'Branches', 'CcGroups', 'CustomerGroups',
    'CustomerRatingLabels', 'Customers', 'Discountgroups', 'Discounts', 'Gewerke',
    'MapArticleGroupCcGroup', 'MapArticleGroupCcGroupGewerk', 'MapBranchReportKey',
    'MapCoreArticleSuperGroupGewerk', 'MapCustomerGewerk', 'MapCustomerHauptgewerk',
    'MapDiscountgroupGewerk', 'MapFocusArticleGroupGewerk', 'Pricetag', 'PricingZones',
    'PurchaseTranscations', 'ReportKeys', 'SaleTransactions', 'Stocks', 'StocksTag', 'Suppliers',
    'MapPricingZonesCustomerGroups', 'StocksMonthly', 'CreditLimit', 'Bonus', 'BaustatGesamt',
    'BaustatWh'
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


class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Agents(BaseModel):
    anrede = TextField(null=True)
    mandant = TextField(null=True)
    sperr_kz = TextField(null=True)
    uuid = UUIDField(primary_key=True)
    vertreter = TextField(null=True)
    vtc = TextField(null=True)

    class Meta:
        table_name = 'agents'
        schema = 'dwh'

class ArticleGroups(BaseModel):
    artikel_grp = TextField(null=True)
    artikel_grp_nr = TextField(null=True)
    artikel_og = TextField(null=True)
    artikel_og_nr = TextField(null=True)
    artikel_sg = TextField(null=True)
    artikel_sg_nr = TextField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'article_groups'
        indexes = (
            (('artikel_grp_nr', 'mandant'), False),
        )
        schema = 'dwh'

class Articles(BaseModel):
    anlagedatum = DateTimeField(null=True)
    artikel = TextField(null=True)
    artikel_grp_nr = TextField(null=True)
    artikel_nr = TextField(null=True)
    auslauf_kz = TextField(null=True)
    bestands_eh = TextField(null=True)
    einkaufs_eh = TextField(null=True)
    gewicht = TextField(null=True)
    haupt_lieferant = TextField(null=True)
    is_pseudo = TextField(null=True)
    lagerbestand = TextField(null=True)
    lieferzeit_days = TextField(null=True)
    mandant = TextField(null=True)
    pex = TextField(null=True)
    preis_eh = BigIntegerField(null=True)
    rabat_grp_nr = TextField(null=True)
    sperr_kz = TextField(null=True)
    statistik_lieferant = TextField(null=True)
    type = TextField(null=True)
    uuid = UUIDField(primary_key=True)
    verkaufs_eh = TextField(null=True)

    class Meta:
        table_name = 'articles'
        indexes = (
            (('artikel_grp_nr', 'mandant'), False),
            (('artikel_nr', 'mandant'), False),
        )
        schema = 'dwh'

class BaustatGesamt(BaseModel):
    handelsbetrieb = TextField(null=True)
    jahr = TextField(null=True)
    klasse_grp = TextField(null=True)
    klasse_kurz = TextField(null=True)
    klasse_sektor = TextField(null=True)
    monat = TextField(null=True)
    summe_netto = DoubleField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'baustat_gesamt'
        schema = 'dwh'

class BaustatWh(BaseModel):
    handelsbetrieb = TextField(null=True)
    jahr = TextField(null=True)
    klasse_grp = TextField(null=True)
    klasse_kurz = TextField(null=True)
    klasse_sektor = TextField(null=True)
    monat = TextField(null=True)
    summe_netto = DoubleField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'baustat_wh'
        schema = 'dwh'

class BoAgents(BaseModel):
    filiale_nr = TextField(null=True)
    mandant = TextField(null=True)
    sperr_kz = TextField(null=True)
    uuid = UUIDField(primary_key=True)
    verkaeufer = TextField(null=True)
    verkaeufer_nr = TextField(null=True)

    class Meta:
        table_name = 'bo_agents'
        schema = 'dwh'

class Bonus(BaseModel):
    bonus_gesamt = DoubleField(null=True)
    bonus_lager = DoubleField(null=True)
    bonus_strecke = DoubleField(null=True)
    jahr = TextField(null=True)
    lieferant_nr = TextField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'bonus'
        indexes = (
            (('mandant', 'lieferant_nr', 'jahr'), False),
        )
        schema = 'dwh'

class Branches(BaseModel):
    art = TextField(null=True)
    bereichs_leiter = TextField(null=True)
    bestell_verantwortlicher = TextField(null=True)
    bestell_verantwortlicher_stv = TextField(null=True)
    filial_ort = TextField(null=True)
    filial_ort_kurz = TextField(null=True)
    filiale = TextField(null=True)
    filiale_nr = TextField(null=True)
    gebiet = TextField(null=True)
    id = BigIntegerField(null=True, unique=True)
    mandant = TextField(null=True)
    niederlassungs_leiter = TextField(null=True)
    region1 = TextField(null=True)
    region2 = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'branches'
        schema = 'dwh'

class CcGroups(BaseModel):
    cc_grp = TextField(null=True)
    id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'cc_groups'
        schema = 'dwh'

class CreditLimit(BaseModel):
    auftraege_offen = DoubleField(null=True)
    auftraege_offen_waehrung = TextField(null=True)
    d_w = TextField(null=True)
    kreditlimit = DoubleField(null=True)
    kreditlimit_waehrung = TextField(null=True)
    mandant = TextField(null=True)
    name = TextField(null=True)
    nr = TextField(null=True)
    posten_offen = DoubleField(null=True)
    uuid = UUIDField(primary_key=True)
    versicherung = DoubleField(null=True)
    versicherungs_waehrung = TextField(null=True)

    class Meta:
        table_name = 'credit_limit'
        indexes = (
            (('mandant', 'nr'), False),
        )
        schema = 'dwh'

class CustomerGroups(BaseModel):
    is_kunden_gruppe_kunde = TextField(null=True)
    mandant = TextField(null=True)
    name = TextField(null=True)
    nr = TextField(null=True)
    sperr_kz = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'customer_groups'
        indexes = (
            (('nr', 'mandant'), False),
        )
        schema = 'dwh'

class CustomerRatingLabels(BaseModel):
    abc_class = TextField(null=True)
    abc_label = TextField(null=True)
    id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'customer_rating_labels'
        schema = 'dwh'

class Customers(BaseModel):
    anlege_date = DateTimeField(null=True)
    auswertungs_key = TextField(null=True)
    branchen_nrs = TextField(null=True)
    filiale_nr = TextField(null=True)
    kunden_grp_nrs = TextField(null=True)
    land = TextField(null=True)
    mandant = TextField(null=True)
    name = TextField(null=True)
    nr = TextField(null=True)
    ort = TextField(null=True)
    plz = TextField(null=True)
    sperr_kz = TextField(null=True)
    standard_kunden_grp = TextField(null=True)
    strasse = TextField(null=True)
    uuid = UUIDField(primary_key=True)
    verkaeufer_nr1 = TextField(null=True)
    verkaeufer_nr2 = TextField(null=True)
    vtc1 = TextField(null=True)
    vtc2 = TextField(null=True)
    wkv_gruppe = TextField(null=True)

    class Meta:
        table_name = 'customers'
        indexes = (
            (('nr', 'mandant'), False),
        )
        schema = 'dwh'

class Discountgroups(BaseModel):
    mandant = TextField(null=True)
    rabat_grp = TextField(null=True)
    rabat_grp_nr = TextField(null=True)
    sperr_kz = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'discountgroups'
        schema = 'dwh'

class Discounts(BaseModel):
    filiale_nr = TextField(null=True)
    gueltig_ab_date = DateTimeField(null=True)
    gueltig_bis_date = DateTimeField(null=True)
    kunden_grp_nr = TextField(null=True)
    mandant = TextField(null=True)
    rabat_grp_nr = TextField(null=True)
    rabat_lager_abhohlung1 = DoubleField(null=True)
    rabat_lager_abhohlung2 = DoubleField(null=True)
    rabat_lager_abhohlung3 = DoubleField(null=True)
    rabat_lager_zustellung1 = DoubleField(null=True)
    rabat_lager_zustellung2 = DoubleField(null=True)
    rabat_lager_zustellung3 = DoubleField(null=True)
    rabat_strecke_abhohlung1 = DoubleField(null=True)
    rabat_strecke_abhohlung2 = DoubleField(null=True)
    rabat_strecke_abhohlung3 = DoubleField(null=True)
    rabat_strecke_zustellung1 = DoubleField(null=True)
    rabat_strecke_zustellung2 = DoubleField(null=True)
    rabat_strecke_zustellung3 = DoubleField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'discounts'
        schema = 'dwh'

class Gewerke(BaseModel):
    gewerk = TextField(null=True)
    id = BigIntegerField(null=True, unique=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'gewerke'
        schema = 'dwh'

class MapArticleGroupCcGroup(BaseModel):
    artikel_grp_nr = TextField(null=True)
    fk_cc_group_id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'map_article_group_cc_group'
        schema = 'dwh'

class MapArticleGroupCcGroupGewerk(BaseModel):
    artikel_grp_nr = TextField(null=True)
    fk_cc_group_id = BigIntegerField(null=True)
    fk_gewerk_id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'map_article_group_cc_group_gewerk'
        schema = 'dwh'

class MapBranchReportKey(BaseModel):
    filiale_nr = TextField(null=True)
    fk_report_key_id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'map_branch_report_key'
        schema = 'dwh'

class MapCoreArticleSuperGroupGewerk(BaseModel):
    artikel_og_nr = TextField(null=True)
    fk_gewerk_id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'map_core_article_super_group_gewerk'
        schema = 'dwh'

class MapCustomerGewerk(BaseModel):
    fk_gewerk_id = BigIntegerField(index=True)
    id = IntegerField(constraints=[SQL("DEFAULT nextval('dwh.map_customer_gewerk_id_seq'::regclass)")])
    kunden_nr = CharField()
    mandant = CharField()

    class Meta:
        table_name = 'map_customer_gewerk'
        indexes = (
            (('mandant', 'kunden_nr'), False),
        )
        schema = 'dwh'
        primary_key = False

class MapCustomerHauptgewerk(BaseModel):
    fk_gewerk_id = BigIntegerField(null=True)
    kunden_nr = CharField(null=True)
    mandant = CharField(null=True)

    class Meta:
        table_name = 'map_customer_hauptgewerk'
        schema = 'dwh'
        primary_key = False

class MapDiscountgroupGewerk(BaseModel):
    fk_gewerk_id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    rabat_grp_nr = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'map_discountgroup_gewerk'
        schema = 'dwh'

class MapFocusArticleGroupGewerk(BaseModel):
    artikel_grp_nr = TextField(null=True)
    fk_gewerk_id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'map_focus_article_group_gewerk'
        schema = 'dwh'

class MapPricingZonesCustomerGroups(BaseModel):
    ausfuehrungs_date = TextField(null=True)
    benutzer_waehrung = TextField(null=True)
    beschreibung = TextField(null=True)
    einheit = TextField(null=True)
    fahrzeug_fahrer = TextField(null=True)
    fin = TextField(null=True)
    herstreller = TextField(null=True)
    innenauftrags_nr = TextField(null=True)
    kilometer_stand = TextField(null=True)
    kosten_art = TextField(null=True)
    kosten_grp = TextField(null=True)
    kosten_quelle = TextField(null=True)
    kostenstelle = TextField(null=True)
    land = TextField(null=True)
    menge = DoubleField(null=True)
    modell = TextField(null=True)
    mwst_frei = TextField(null=True)
    produkt = TextField(null=True)
    rechnungs_date = TextField(null=True)
    rechnungs_nr = TextField(null=True)
    rechnungs_waehrung = TextField(null=True)
    ust = DoubleField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'map_pricing_zones_customer_groups'
        schema = 'dwh'

class Pricetag(BaseModel):
    preis_kz = TextField(null=True)
    preis_kz_name = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'pricetag'
        schema = 'dwh'

class PricingZones(BaseModel):
    id = BigIntegerField(null=True)
    mandant = TextField(null=True)
    pricing_zone = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'pricing_zones'
        schema = 'dwh'

class PurchaseTranscations(BaseModel):
    a_z = TextField(null=True)
    artikel_nr = TextField(null=True)
    auftrags_date = DateTimeField(null=True)
    bearbeitungs_nr = TextField(null=True)
    bearbeitungs_nr_erw = TextField(null=True)
    ek = DoubleField(null=True)
    filiale_nr = TextField(null=True)
    is_kommission = TextField(null=True)
    l_s = TextField(null=True)
    liefer_adr_name1 = TextField(null=True)
    liefer_adr_nr = TextField(null=True)
    lieferanten_nr = TextField(null=True)
    lieferschein_date = DateTimeField(null=True)
    lieferschein_nr = TextField(null=True)
    mandant = TextField(null=True)
    menge = DoubleField(null=True)
    ort = TextField(null=True)
    plz = TextField(null=True)
    pos_ek = DoubleField(null=True)
    positions_nr = TextField(null=True)
    positions_nr_erw = TextField(null=True)
    rechnungs_date = DateTimeField(index=True, null=True)
    rechnungs_nr = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'purchase_transcations'
        indexes = (
            (('artikel_nr', 'mandant', 'rechnungs_date'), False),
            (('lieferanten_nr', 'mandant', 'rechnungs_date'), False),
        )
        schema = 'dwh'

class ReportKeys(BaseModel):
    id = BigIntegerField(null=True)
    report_key = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'report_keys'
        schema = 'dwh'

class SaleTransactions(BaseModel):
    a_z = TextField(null=True)
    artikel_nr = TextField(null=True)
    auftrags_date = DateTimeField(null=True)
    bar_rechnung = TextField(null=True)
    bearbeitungs_nr = TextField(null=True)
    bearbeitungs_nr_erw = TextField(null=True)
    erm_preis = DoubleField(null=True)
    filiale_nr = TextField(null=True)
    is_bestellung = TextField(null=True)
    kunden_grp_nr = TextField(null=True)
    kunden_nr = TextField(null=True)
    l_s = TextField(null=True)
    liefer_adr_name1 = TextField(null=True)
    liefer_adr_nr = TextField(null=True)
    lieferanten_nr = TextField(null=True)
    lieferschein_date = DateTimeField(null=True)
    lieferschein_nr = TextField(null=True)
    mandant = TextField(null=True)
    marge_eur = DoubleField(null=True)
    menge = DoubleField(null=True)
    ort = TextField(null=True)
    plz = TextField(null=True)
    pos_vk = DoubleField(null=True)
    positions_art = TextField(null=True)
    positions_fracht = DoubleField(null=True)
    positions_nr = TextField(null=True)
    positions_nr_erw = TextField(null=True)
    preis_date = DateTimeField(null=True)
    preis_eh = BigIntegerField(null=True)
    preis_kz = TextField(null=True)
    preis_kz_algo = TextField(null=True)
    rabat_grp_nr = TextField(null=True)
    rechnungs_date = DateTimeField(index=True, null=True)
    rechnungs_nr = TextField(null=True)
    uuid = UUIDField(primary_key=True)
    verkaeufer_nr = TextField(null=True)
    vk = DoubleField(null=True)
    vk_liste = DoubleField(null=True)
    vtc1 = TextField(null=True)
    vtc2 = TextField(null=True)

    class Meta:
        table_name = 'sale_transactions'
        indexes = (
            (('artikel_nr', 'mandant', 'rechnungs_date'), False),
            (('filiale_nr', 'mandant', 'rechnungs_date'), False),
            (('kunden_nr', 'mandant', 'rechnungs_date'), False),
        )
        schema = 'dwh'

class Stocks(BaseModel):
    artikel_nr = TextField(null=True)
    datum_l_ek = DateTimeField(null=True)
    datum_l_vk = DateTimeField(null=True)
    durchschn_ek = DoubleField(null=True)
    filiale_nr = TextField(null=True)
    kz_nul_rw = TextField(null=True)
    lagerbestand = TextField(null=True)
    lagerwert = DoubleField(null=True)
    mandant = TextField(null=True)
    menge = DoubleField(null=True)
    preis_eh = BigIntegerField(null=True)
    reserviert = DoubleField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'stocks'
        indexes = (
            (('mandant', 'artikel_nr'), False),
            (('mandant', 'artikel_nr', 'filiale_nr'), False),
        )
        schema = 'dwh'

class StocksMonthly(BaseModel):
    artikel_nr = TextField(null=True)
    filiale_nr = TextField(null=True)
    jahr = TextField(null=True)
    lagerwert_01 = DoubleField(null=True)
    lagerwert_02 = DoubleField(null=True)
    lagerwert_03 = DoubleField(null=True)
    lagerwert_04 = DoubleField(null=True)
    lagerwert_05 = DoubleField(null=True)
    lagerwert_06 = DoubleField(null=True)
    lagerwert_07 = DoubleField(null=True)
    lagerwert_08 = DoubleField(null=True)
    lagerwert_09 = DoubleField(null=True)
    lagerwert_10 = DoubleField(null=True)
    lagerwert_11 = DoubleField(null=True)
    lagerwert_12 = DoubleField(null=True)
    mandant = TextField(null=True)
    menge_01 = DoubleField(null=True)
    menge_02 = DoubleField(null=True)
    menge_03 = DoubleField(null=True)
    menge_04 = DoubleField(null=True)
    menge_05 = DoubleField(null=True)
    menge_06 = DoubleField(null=True)
    menge_07 = DoubleField(null=True)
    menge_08 = DoubleField(null=True)
    menge_09 = DoubleField(null=True)
    menge_10 = DoubleField(null=True)
    menge_11 = DoubleField(null=True)
    menge_12 = DoubleField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'stocks_monthly'
        indexes = (
            (('mandant', 'artikel_nr'), False),
            (('mandant', 'artikel_nr', 'filiale_nr'), False),
        )
        schema = 'dwh'

class StocksTag(BaseModel):
    artikel_nr = TextField(null=True)
    filiale_nr = TextField(null=True)
    lager_kz = TextField(null=True)
    mandant = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'stocks_tag'
        indexes = (
            (('mandant', 'artikel_nr', 'filiale_nr'), False),
        )
        schema = 'dwh'

class Suppliers(BaseModel):
    abcd_klassifizierung = TextField(null=True)
    anrede = TextField(null=True)
    fh_text = TextField(null=True)
    fh_wert = DoubleField(null=True)
    kennzeichen_intern = TextField(null=True)
    kennzeichen_intern_bezeichnung = TextField(null=True)
    kg_g_bez = TextField(null=True)
    kz_g = TextField(null=True)
    kz_h = TextField(null=True)
    kz_h_bez = TextField(null=True)
    land = TextField(null=True)
    lief_all = TextField(null=True)
    lieferzeit_days = TextField(null=True)
    mandant = TextField(null=True)
    name = TextField(null=True)
    netto_days = TextField(null=True)
    nr = TextField(null=True)
    ort = TextField(null=True)
    plz = TextField(null=True)
    skonto_days = TextField(null=True)
    skonto_ptc = DoubleField(null=True)
    sperr_kz = TextField(null=True)
    strasse = TextField(null=True)
    uuid = UUIDField(primary_key=True)

    class Meta:
        table_name = 'suppliers'
        indexes = (
            (('nr', 'mandant'), False),
        )
        schema = 'dwh'
