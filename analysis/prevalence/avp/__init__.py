from .detector import Detector, ADetector

from .acuant import Acuant
from .agechecked import AgeChecked
from .agechecker_net import AgeCheckerNet
from .agecheckpro import AgeCheckPro
from .agego import AgeGo
from .ageverif import AgeVerif
from .ageverifydev import AgeVerifyDev
from .agekey import AgeKey
from .agemin import AgeMin
from .airisident import AirisIdent
from .amie import Amie
from .aristotle import Aristotle
from .authenteq import Authenteq
from .aware import Aware
from .bioid import BioId
from .bluecheck import BlueCheck
from .borderage import BorderAge
from .catchall import CatchAll
from .cmp import CmpAgeVerif
from .complycube import ComplyCube
from .daon import Daon
from .didit import Didit
from .earthid import EarthId
from .everypixel import Everypixel
from .emblem import Emblem
from .ep import Ep
from .gbg import Gbg
from .gocam import GoCam
from .generic import Generic
from .hyperverge import Hyperverge
from .id_me import IdMe
from .idemia import Idemia
from .idenfy import Idenfy
from .identomat import Identomat
from .idnow import IdNow
from .idology import Idology
from .idrnd import IdRnd
from .ike import Ike
from .incode import Incode
from .iproov import IProov
from .jumio import Jumio
from .kid import Kid
from .kws import KidsWebServices
from .luciditi import Luciditi
from .luxand import Luxand
from .mitek import Mitek
from .ondato import Ondato
from .one_account import OneAccount
from .oneid import OneId
from .onespan import OneSpan
from .onfido import Onfido
from .opale import Opale
from .paravision import Paravision
from .persona import Persona
from .privateav import PrivateAV
from .privately import Privately
from .privo import Privo
from .regula import Regula
from .roc import Roc
from .scytales import Scytales
from .sharering import ShareRing
from .shufti import Shufti
from .socure import Socure
from .sumsub import Sumsub
from .surepass import SurePassIo
from .tot import TokenOfTrust
from .trulioo import Trulioo
from .trustmatic import Trustmatic
from .veratad import Veratad
from .veridas import Veridas
from .veriff import Veriff
from .verifymyage import VerifyMyAge
from .yoti import Yoti


DETECTORS = [
    Acuant,
    AgeChecked,
    AgeCheckerNet,
    AgeCheckPro,
    AgeGo,
    AgeKey,
    AgeMin,
    AgeVerif,
    AgeVerifyDev,
    AirisIdent,
    Amie,
    Aristotle,
    Authenteq,
    Aware,
    BioId,
    BlueCheck,
    BorderAge,
    CatchAll,
    CmpAgeVerif,
    ComplyCube,
    Daon,
    Didit,
    EarthId,
    Emblem,
    Ep,
    Everypixel,
    Gbg,
    Generic,
    GoCam,
    Hyperverge,
    Idemia,
    Idenfy,
    Identomat,
    IdMe,
    IdNow,
    Idology,
    IdRnd,
    Ike,
    Incode,
    IProov,
    Jumio,
    Kid,
    KidsWebServices,
    Luciditi,
    Luxand,
    Mitek,
    Ondato,
    OneAccount,
    OneId,
    OneSpan,
    Onfido,
    Opale,
    Paravision,
    Persona,
    PrivateAV,
    Privately,
    Privo,
    Regula,
    Roc,
    Scytales,
    ShareRing,
    Shufti,
    Socure,
    Sumsub,
    SurePassIo,
    TokenOfTrust,
    Trulioo,
    Trustmatic,
    Veratad,
    Veridas,
    Veriff,
    VerifyMyAge,
    Yoti,
]

DETECTOR_NAMES = [test.name() for test in DETECTORS]
PROVIDER_NAMES = list(
    set(DETECTOR_NAMES)
    - set([d.name() for d in [CatchAll, Ep, CmpAgeVerif, Ep, Generic]])
)
COLUMN_NAMES = [
    "is_empty",
    "parse_error",
    "cloudflare",
    "rta",
    "meta_info",
] + DETECTOR_NAMES

# re-exports
Detector, ADetector
