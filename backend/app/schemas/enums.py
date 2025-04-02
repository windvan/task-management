from enum import Enum as pyEnum


class Enum(str, pyEnum):
    @classmethod
    def to_list(cls):
        return {cls.__name__: [role.value for role in cls]}

# region User


class RoleEnum(Enum):
    Portfolio = "Portfolio"
    Science_Delivery = "Science_Delivery"
    Operation = "Operation"
    Admin = "Admin"

# endregion

# region Product


class StageEnum(Enum):
    stage_A1 = "stage_A1"  # :Generation;
    stage_A2 = "stage_A2"  # :Proof of Technology;
    stage_A3 = "stage_A3"  # :Proof of Concept;
    stage_B = "stage_B"  # :Early Development;
    stage_C = "stage_C"  # :Late Development;
    stage_D1 = "stage_D1"  # :Commercial;
    stage_D2 = "stage_D2"  # :Discontinue;

# endregion

# region Project


class ProjectManagerEnum(Enum):
    Daiqing_Jiang = "Daiqing_Jiang"
    Siying_Zhu = "Siying_Zhu"
    Daisy_Wan = "Daisy_Wan"


class RegManagerEnum(Enum):
    Hongtao_Jiao = "Hongtao_Jiao"
    Ting_Li = "Ting_Li"
    Shan_Geng = "Shan_Geng"
    Zheng_Li = "Zheng_Li"
    Xiaojing_Li = "Xiaojing_Li"
    Yunqi_Li = "Yunqi_Li"


class IndicationEnum(Enum):
    Herbicide = "H"
    Insecticide = "I"
    Fungicide = "F"
    SeedCare = "SC"
    SanitaryPesticides = "SPS"


class ProjectStatusEnum(Enum):
    Idea_Stage = "Idea_Stage"
    Active = "Active"
    Finished = "Finished"
    Terminated = "Terminated"


class SubmissionStatusEnum(Enum):
    Preparation = "Preparation"
    Submmited = "Submmited"
    Rejected = "Rejected"
    Approved = "Approved"

# endregion

# region Cro


class DisciplineEnum(Enum):
    Tox = "Tox"
    Eco_Tox = "Eco_Tox"
    Residue = "Residue"
    Other = "Other"

# endregion

# region Task


class TaskCategoryEnum(Enum):
    Tox_Study = "Tox_Study"
    Eco_Tox_Study = "Eco_Tox_Study"
    Residue_Study = "Residue_Study"
    Processing_Residue_Study = "Processing_Residue_Study"
    Risk_Assessment = "Risk_Assessment"
    Pre_Scoping = "Pre_Scoping"
    Others = "Others"


class TaskStatusEnum(Enum):
    Idle = "Idle"
    Go = "Go"    # only active is the sign to proceed as planed
    Finished = "Finished"
    Pending = "Pending"
    Terminated = "Terminated"


class TaskProgressEnum(Enum):
    Not_Start = "Not_Start"
    Protocal_Done = "Protocal_Done"
    On_Going = "On_Going"
    Drafting = "Drafting"
    Finished = "Finished"


class RegEntityEnum(Enum):
    Switzerland = "CH"      # offshore
    Great_Britain = "GB"    # offshore
    NanTong = "NT"          # onshore
    KunShan = "KS"          # onshore


class CostCenterEnum(Enum):
    SGC = "420245"  # None-FFP
    KS = "427312"   # FFP
    NT = "424231"   # FFP


class RegistrationTypeEnum(Enum):
    # study and risk assessment only
    FEX = "FEX"
    LEX = "LEX"
    FNE = "FNE"
    Me_Too_Authorization = "Me_Too_Authorization"
    Me_Too_Identification = "Me_Too_Identification"


class PaymentMethodEnum(Enum):
    Half_Half = "Half_Half"
    Pre_Once = "Pre_Once"
    Post_Once = "Post_Once"


class PaymentStatusEnum(Enum):
    Not_Start = "Not_Start"
    First_Payment_Done = "First_Payment_Done"
    Full_Payment_Done = "Full_Payment_Done"


# endregion

# region Sample
class QuantityUnitEnum(Enum):
    g_per_package = "g/package"
    ml_per_package = "mL/package"
    kg_per_package = "kg/package"
    l_per_package = "L/package"


class SampleStatusEnum(Enum):
    Waiting = "Waiting"
    Estimated = "Estimated"
    In_Store = "In_Store"
    CRO_Received = "CRO_Received"


# endregion

# region Message
class MessageSeverityEnum(Enum):
    Danger = "Danger"
    Warn = "Warning"
    Info = "Info"

# endregion


# region Note
class NoteSeverityEnum(Enum):
    Danger = "Danger"
    Warn = "Warning"
    Info = "Info"


# endregon

def get_all_enums():
    all_enums = {}
    class_list = [item[1] for item in globals().items() if item[0].endswith(
        'Enum') and item[0] not in ['dbEnum', 'pyEnum', 'Enum']]

    for obj in class_list:
        all_enums.update(obj.to_list())

    return all_enums
