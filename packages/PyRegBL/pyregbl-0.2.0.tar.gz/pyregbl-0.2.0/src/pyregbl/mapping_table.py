from .tables.GBAUP import GBAUP
from .tables.GENH import GENH
from .tables.GENW import GENW
from .tables.GKAT import GKAT
from .tables.GKLAS import GKLAS
from .tables.GKSCE import GKSCE
from .tables.GSTAT import GSTAT
from .tables.GVOLNORM import GVOLNORM
from .tables.GVOLSCE import GVOLSCE
from .tables.GWAERZH import GWAERZH
from .tables.GWAERSCEH import GWAERSCEH
from .tables.GWAERZW import GWAERZW
from .tables.GWAERSCEW import GWAERSCEW
from .tables.LTYP import LTYP
from .tables.PARTAB import PARTAB
from .tables.PARTBZ import PARTBZ
from .tables.PSTAT import PSTAT
from .tables.PTYPAG import PTYPAG
from .tables.PTYPBW import PTYPBW
from .tables.SREAL import SREAL
from .tables.STRART import STRART
from .tables.STRSP import STRSP
from .tables.WGBANMERKUNG import WGBANMERKUNG
from .tables.WNART import WNART
from .tables.WNARTSCE import WNARTSCE
from .tables.WSTAT import WSTAT

"""
This module contains the mapping table for the different tables in the REGBL database.
"""

mapping_table = {
    "gbaup": GBAUP,
    # GENH1 and 2
    "genh1": GENH,
    "genh2": GENH,
    # GENW1 and 2
    "genw1": GENW,
    "genw2": GENW,
    "gkat": GKAT,
    "gklas": GKLAS,
    "gksce": GKSCE,
    "gstat": GSTAT,
    "gvolnorm": GVOLNORM,
    "gvolsce": GVOLSCE,
    # GWAERSCEH1 and 2
    "gwaersceh1": GWAERSCEH,
    "gwaersceh2": GWAERSCEH,
    # GWAERZW1 and 2
    "gwaerzw1": GWAERZW,
    "gwaerzw2": GWAERZW,
    # GWAERZH1 and 2
    "gwaerzh1": GWAERZH,
    "gwaerzh2": GWAERZH,
    # GWAERSCEW1 and 2
    "gwaerscew1": GWAERSCEW,
    "gwaerscew2": GWAERSCEW,
    "ltyp": LTYP,
    "partab": PARTAB,
    "partbz": PARTBZ,
    "pstat": PSTAT,
    "ptypag": PTYPAG,
    "ptypbw": PTYPBW,
    "sreal": SREAL,
    "strart": STRART,
    "strsp": STRSP,
    "wgbanmerkung": WGBANMERKUNG,
    "wnart": WNART,
    "wnartsce": WNARTSCE,
    "wstat": WSTAT,
}
