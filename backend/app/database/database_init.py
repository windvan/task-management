from datetime import date
from ..schemas import *
from ..schemas.enums import *
from ..utils.functions import get_password_hash
from sqlmodel import Session


def create_test_data(engin):

    user_list = [
        User(
            email="admin@admin.com",
            name="Admin",
            role=RoleEnum.Admin,
            password_hash=get_password_hash("admin888"), created_by=1, updated_by=1),
        User(
            email="xiaoyan.hu@syngenta.com",
            name="Xiaoyan Hu",
            role=RoleEnum.Science_Delivery,
            password_hash=get_password_hash("123456"), created_by=1),
        User(
            email="dandan.ye@syngenta.com",
            name="Dandan Ye",
            role=RoleEnum.Science_Delivery,
            password_hash=get_password_hash("123456"), created_by=1),
        User(
            email="zhe.dong@syngenta.com",
            name="Zhe Dong",
            role=RoleEnum.Science_Delivery,
            password_hash=get_password_hash("123456"), created_by=1),
        User(
            email="jennifer.zheng@syngenta.com",
            name="Jennifer Zheng",
            role=RoleEnum.Science_Delivery,
            password_hash=get_password_hash("123456"), created_by=1),
        User(
            email="ethan.yang@syngenta.com",
            name="Ethan Yang",
            role=RoleEnum.Science_Delivery,
            password_hash=get_password_hash("123456"), created_by=1),
        User(
            email="hank.gao@syngenta.com",
            name="Hank Gao",
            role=RoleEnum.Portfolio,
            password_hash=get_password_hash("123456"), created_by=1),
        User(
            email="niphee.fei@syngenta.com",
            name="Niphee Fei",
            role=RoleEnum.Operation,
            password_hash=get_password_hash("123456"), created_by=1),
        User(
            email="jessica.zhang@syngenta.com",
            name="Jessica Zhang",
            role=RoleEnum.Admin,
            password_hash=get_password_hash("123456"), created_by=1)]
    with Session(engin) as session:
        for user in user_list:
            session.add(user)
        session.commit()

    task_library_data = [
        TaskLibrary(task_category="Tox_Study",
                    task_name="Acute Oral", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Tox_Study",
                    task_name="Acute Dermal", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Tox_Study",
                    task_name="Eye Irritation", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Tox_Study",
                    task_name="Skin Irritation", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Tox_Study",
                    task_name="Skin Sensitization", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Tox_Study",
                    task_name="Acute inhalation", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Avian Acute oral toxicity", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Acute toxcity to daphnia", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Algal Growth Inhibition", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Acute toxicity to trichogrammatid", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Acute toxicity to silkworm", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Acute toxicity to ladybird", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Acute oral toxicity to bee", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Acute contact toxicity to bee", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Acute toxicity to earthworm", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Eco_Tox_Study",
                    task_name="Acute fish toxicity", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Risk_Assessment",
                    task_name="Operator risk assessment", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Risk_Assessment",
                    task_name="Environment risk assessment", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Risk_Assessment",
                    task_name="Dietary risk assessment", default_task_owner_id=None, created_by=1),
        TaskLibrary(task_category="Residue_Study",
                    task_name="Residue study", default_task_owner_id=None, created_by=1),
        TaskLibrary(task_category="Processing_Residue_Study",
                    task_name="Processing_residue_study", default_task_owner_id=None, created_by=1),
        TaskLibrary(task_category="Pre_Scoping",
                    task_name="OPEX_Scoping", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Pre_Scoping",
                    task_name="DRA_Scoping", default_task_owner_id=None, created_by=1),
        TaskLibrary(task_category="Pre_Scoping",
                    task_name="ERA_Scoping", default_task_owner_id=2, created_by=1),
        TaskLibrary(task_category="Pre_Scoping",
                    task_name="Residue_Scoping", default_task_owner_id=None, created_by=1),
        TaskLibrary(task_category="Others",
                    task_name="Deco_Doc", default_task_owner_id=7, created_by=1),
        TaskLibrary(task_category="Others",
                    task_name="Statement", default_task_owner_id=None, created_by=1),
        TaskLibrary(task_category="Others",
                    task_name="Label_Review", default_task_owner_id=7, created_by=1),
        TaskLibrary(task_category="Others",
                    task_name="Check_List", default_task_owner_id=7, created_by=1),
        TaskLibrary(task_category="Others",
                    task_name="Risk_Matrix", default_task_owner_id=7, created_by=1),
        TaskLibrary(task_category="Others",
                    task_name="Gov_Doc_Tox", default_task_owner_id=3, created_by=1),
        TaskLibrary(task_category="Others",
                    task_name="Gov_Doc_EcoTox", default_task_owner_id=2, created_by=1),
    ]

    with Session(engin) as session:
        for task_item in task_library_data:
            session.add(task_item)
        session.commit()

    # crop_data = [
    #     Crop(crop_name_cn="大麦", crop_name_en="Barley", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="青花菜", crop_name_en="broccoli", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="人参", crop_name_en="ginseng", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="三七", crop_name_en="sanqi",
    #          required_trials=4, comments="custom", created_by=1),
    #     Crop(crop_name_cn="生姜", crop_name_en="ginger", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="苍术", crop_name_en="rhizoma atractylodis", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="水稻", crop_name_en="Rice", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="冬小麦", crop_name_en="Winter Wheat", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="小麦", crop_name_en="Wheat", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="春小麦", crop_name_en="Spring Wheat", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="绿豆", crop_name_en="mung bean", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="玉米", crop_name_en="Corn", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="春玉米", crop_name_en="Spring Corn", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="夏玉米", crop_name_en="Summer Corn", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="韭菜", crop_name_en="Chinese chives", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="大蒜", crop_name_en="Garlic", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="结球甘蓝", crop_name_en="Cabbage", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="百合", crop_name_en="Lily", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="花椰菜", crop_name_en="Cauliflower", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="菠菜", crop_name_en="Spinach", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="芥蓝", crop_name_en="Chinese kale", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="大白菜", crop_name_en="Chinese cabbage", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="芹菜", crop_name_en="Celery", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="小茴香", crop_name_en="Cumin seed", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="普通白菜", crop_name_en=None, required_trials=10, created_by=1),
    #     Crop(crop_name_cn="番茄", crop_name_en="Tomato", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="辣椒", crop_name_en="Pepper", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="茄子", crop_name_en="Eggplant", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="黄瓜", crop_name_en="Cucumber", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="西葫芦", crop_name_en="zucchini", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="豇豆", crop_name_en="cowpea", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="节瓜", crop_name_en="zucchini", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="冬瓜", crop_name_en="wax gourd", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="菜豆", crop_name_en="kidney bean", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="萝卜", crop_name_en="turnip", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="胡萝卜", crop_name_en="Carrot", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="茎用莴苣", crop_name_en="Stem lettuce", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="芦笋", crop_name_en="asparagus", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="马铃薯", crop_name_en="Potato", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="山药", crop_name_en="Chinese yam", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="甘薯", crop_name_en="sweet potato", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="水芹", crop_name_en="cress", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="豆瓣菜", crop_name_en=None, required_trials=4, created_by=1),
    #     Crop(crop_name_cn="菱角", crop_name_en=None, required_trials=4, created_by=1),
    #     Crop(crop_name_cn="茭白", crop_name_en="wild rice stem", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="芡实", crop_name_en=None, required_trials=4, created_by=1),
    #     Crop(crop_name_cn="竹笋", crop_name_en="bamboo shoots", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="莲藕", crop_name_en="lotus rhizome", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="黄花菜", crop_name_en="Daylily", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="柑橘", crop_name_en="Citrus", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="梨", crop_name_en="Pear", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="桃", crop_name_en="Peach", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="柿子", crop_name_en="Persimmon", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="苹果", crop_name_en="Apple", required_trials=12, created_by=1),
    #     Crop(crop_name_cn="枇杷", crop_name_en="loquat", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="蓝莓", crop_name_en="Blueberry", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="枣", crop_name_en="jujube", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="枸杞", crop_name_en="Matrimony vine", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="桑葚", crop_name_en="mulberry", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="草莓", crop_name_en="Strawberry", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="猕猴桃", crop_name_en="Kiwi Fruit", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="葡萄", crop_name_en="Grape", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="荔枝", crop_name_en="Litchi", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="杨梅", crop_name_en="Waxberry", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="芒果", crop_name_en="Mango", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="橄榄", crop_name_en="olive", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="香蕉", crop_name_en="Banana", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="石榴", crop_name_en="pomegranate", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="椰子", crop_name_en="coconut", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="木瓜", crop_name_en="pawpaw", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="菠萝", crop_name_en="pineapple", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="杏仁", crop_name_en="almond", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="西瓜", crop_name_en="Watermelon", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="甜瓜", crop_name_en="melon", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="油菜", crop_name_en="Rape", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="甘蔗", crop_name_en="sugarcane", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="甜菜", crop_name_en="sugarbeet", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="核桃", crop_name_en="Walnut", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="大豆", crop_name_en="Soya bean", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="冬油菜", crop_name_en="Winter Rape", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="春大豆", crop_name_en="Spring Soya bean", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="春油菜", crop_name_en="soyabena", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="棉籽", crop_name_en="Cottonseed", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="夏大豆", crop_name_en="Summer Soya bean", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="葵花籽", crop_name_en="Sunflower Seeds", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="花生", crop_name_en="Peanut", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="可可豆", crop_name_en=None, required_trials=4, created_by=1),
    #     Crop(crop_name_cn="油茶籽", crop_name_en=None, required_trials=4, created_by=1),
    #     Crop(crop_name_cn="咖啡豆", crop_name_en="Coffee Bean", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="茶", crop_name_en="Tea", required_trials=10, created_by=1),
    #     Crop(crop_name_cn="香菇", crop_name_en="Mushroom", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="啤酒花", crop_name_en="hop", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="菊花", crop_name_en="chrysanthemum", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="玫瑰花", crop_name_en="Rose", required_trials=4, created_by=1),
    #     Crop(crop_name_cn="烟草", crop_name_en="Tobacco", required_trials=8, created_by=1),
    #     Crop(crop_name_cn="平菇", crop_name_en="oyster mushroom", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="木耳", crop_name_en="agarics", required_trials=6, created_by=1),
    #     Crop(crop_name_cn="金针菇", crop_name_en="Needle Mushroom", required_trials=6, created_by=1),
    # ]

    # with Session(engin) as session:
    #     for crop in crop_data:
    #         session.add(crop)
    #     session.commit()

    product_data = [
        Product(internal_name="Vibrance 500FS/SDX", lead_ai="Sedaxane",
                stage="stage_D1", a_number="A16148F", created_by=1),
        Product(internal_name="APN solo 200FS", lead_ai="APN",
                stage="stage_D1", a_number="A19649B", created_by=1),
        Product(internal_name="APN+PRS", lead_ai="APN",
                stage="stage_D1", a_number="A25147A", created_by=1),
        Product(internal_name="PXD+MTZ EC", lead_ai="PXD",
                stage="stage_B", a_number="A24312A", created_by=1),
        Product(internal_name="TYM GR", lead_ai="TYM",
                stage="stage_B", a_number="A23358A", created_by=1),
        Product(internal_name="Tymirium 200 FS", lead_ai="TYM",
                stage="stage_D1", a_number="A22940D", created_by=1),
        Product(internal_name="Tymirium 450 SC", lead_ai="TYM",
                stage="stage_C", a_number="A22011B", created_by=1),
        Product(internal_name="Tymirium 500 FS", lead_ai="TYM",
                stage="stage_C", a_number="A22417C", created_by=1),
    ]

    with Session(engin) as session:
        for product in product_data:
            session.add(product)
        session.commit()

    project_data = [
        Project(product_id=2, registration_type=RegistrationTypeEnum.FNE,
                project_name='APN SOLO 200 FS ON RICE', indication=IndicationEnum.Fungicide,
                project_status=ProjectStatusEnum.Finished, portfolio_contact_id=7, project_manager='Siying_Zhu',
                reg_manager='Zheng_Li', created_by=1),

    ]

    with Session(engin) as session:
        for project in project_data:
            session.add(project)
        session.commit()

    cro_data = [
        Cro(cro_name="沈阳沈化院测试技术有限公司安全评价中心", certification_number="SD2024120", certification_scope="residue,process,tox,eco-tox",
            certification_expiration_date=date(2029, 5, 19), address="辽宁省沈阳市铁西区沈辽路600号", created_by=1),

    ]

    with Session(engin) as session:
        for cro in cro_data:
            session.add(cro)
        session.commit()
    cro_contact_data = [CroContact(cro_id=1, contact_name="张丹", phone_number="17824228516",
                                   email="zhangdan15@sinochem.com", discipline=DisciplineEnum.Other, remarks="Business", created_by=1),
                        CroContact(cro_id=1, contact_name="刘良月", phone_number="18540366250",
                                   email="xxx@sinochem.com", discipline=DisciplineEnum.Residue, remarks="residue", created_by=1)]
    with Session(engin) as session:
        for cro_contact in cro_contact_data:
            session.add(cro_contact)
        session.commit()
    sample_data = [
        Sample(product_id=1, sample_name="apn 200 sc solo", created_by=1)

    ]

    with Session(engin) as session:
        for sample in sample_data:
            session.add(sample)
        session.commit()

    task_data = [
        Task(project_id=1, task_name="Residue study",
             task_category="Residue_Study", task_owner_id=6, task_status="Idle", expected_delivery_date=date(2025, 12, 31), start_year=2025, created_by=1),
        Task(project_id=1, task_name="Acute Oral",
             task_category="Tox_Study", task_owner_id=3, task_status="Go", expected_delivery_date=date(2025, 12, 31), start_year=2025, created_by=1),
        Task(project_id=1, task_name="Acute Dermal",
             task_category="Tox_Study", task_owner_id=3, task_status="Go", expected_delivery_date=date(2025, 12, 31), start_year=2025, created_by=1),


    ]

    with Session(engin) as session:
        for task in task_data:
            session.add(task)
        session.commit()
