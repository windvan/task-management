/*
 Navicat Premium Data Transfer

 Source Server         : database
 Source Server Type    : SQLite
 Source Server Version : 3035005 (3.35.5)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3035005 (3.35.5)
 File Encoding         : 65001

 Date: 22/02/2025 12:17:15
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for cro
-- ----------------------------
DROP TABLE IF EXISTS "cro";
CREATE TABLE "cro" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "cro_name" VARCHAR NOT NULL,
  "certification_number" VARCHAR NOT NULL,
  "certification_scope" VARCHAR NOT NULL,
  "certification_expiration_date" DATE NOT NULL,
  "address" VARCHAR,
  "fw_contract_start" DATE,
  "fw_contract_end" DATE,
  "fw_contract_detail" VARCHAR,
  "comments" VARCHAR,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("certification_number" ASC)
);

-- ----------------------------
-- Records of cro
-- ----------------------------
INSERT INTO "cro" VALUES ('2025-02-21 08:49:39.659568', 6, '沈阳沈化院测试技术有限公司安全评价中心', 'SD2024120', 'Residue', '2029-05-19', '辽宁省沈阳市铁西区沈辽路600号', '2025-02-28', '2028-02-28', NULL, NULL, 1);
INSERT INTO "cro" VALUES ('2025-02-22 02:25:01.585455', 6, '北京绿城堡农业科技有限公司', 'SD2020023', '产品化学试验：产品质量检测试验/储存稳定性试验、药效试验：农林用药试验（杀虫剂、杀菌剂、除草剂、植物生长调节剂）、残留试验：农作物留试验（室内检测、田间试验）、环境影响试验：生态毒理试验A类、环境归趋试验A类', '2025-08-03', '北京市海淀区高里掌路3号院21号楼', NULL, NULL, NULL, NULL, 2);

-- ----------------------------
-- Table structure for cro_contact
-- ----------------------------
DROP TABLE IF EXISTS "cro_contact";
CREATE TABLE "cro_contact" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "cro_id" INTEGER NOT NULL,
  "contact_name" VARCHAR NOT NULL,
  "phone_number" VARCHAR NOT NULL,
  "email" VARCHAR,
  "discipline" VARCHAR(7) NOT NULL,
  "remarks" VARCHAR,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("cro_id") REFERENCES "cro" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("contact_name" ASC),
  UNIQUE ("phone_number" ASC)
);

-- ----------------------------
-- Records of cro_contact
-- ----------------------------
INSERT INTO "cro_contact" VALUES ('2025-02-21 08:49:39.669091', 1, 1, '张丹', '17824228516', 'zhangdan15@sinochem.com', 'Other', 'Business', 1);
INSERT INTO "cro_contact" VALUES ('2025-02-21 08:49:39.669091', 1, 1, '刘良月', '18540366250', 'xxx@sinochem.com', 'Residue', 'residue', 2);
INSERT INTO "cro_contact" VALUES ('2025-02-21 10:28:15.969737', NULL, 1, 'zhangsan', '1412325363', 'ethan.yang@syngenta.com', 'Eco_Tox', 'fwef', 5);
INSERT INTO "cro_contact" VALUES ('2025-02-22 02:47:07.762496', NULL, 2, '潘兴鲁', '13051526430', 'pangxinglu@163.com', 'Residue', NULL, 6);

-- ----------------------------
-- Table structure for crop
-- ----------------------------
DROP TABLE IF EXISTS "crop";
CREATE TABLE "crop" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "crop_name_cn" VARCHAR NOT NULL,
  "crop_name_en" VARCHAR,
  "required_trials" INTEGER NOT NULL,
  "comments" VARCHAR,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of crop
-- ----------------------------
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '大麦', 'Barley', 4, NULL, 1);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '青花菜', 'broccoli', 4, NULL, 2);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '人参', 'ginseng', 4, NULL, 3);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '三七', 'sanqi', 4, 'custom', 4);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '生姜', 'ginger', 4, NULL, 5);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '苍术', 'rhizoma atractylodis', 4, NULL, 6);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '水稻', 'Rice', 12, NULL, 7);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '冬小麦', 'Winter Wheat', 10, NULL, 8);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '小麦', 'Wheat', 12, NULL, 9);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '春小麦', 'Spring Wheat', 6, NULL, 10);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '绿豆', 'mung bean', 6, NULL, 11);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '玉米', 'Corn', 12, NULL, 12);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '春玉米', 'Spring Corn', 6, NULL, 13);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '夏玉米', 'Summer Corn', 10, NULL, 14);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '韭菜', 'Chinese chives', 8, NULL, 15);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '大蒜', 'Garlic', 6, NULL, 16);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '结球甘蓝', 'Cabbage', 12, NULL, 17);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '百合', 'Lily', 4, NULL, 18);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '花椰菜', 'Cauliflower', 8, NULL, 19);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '菠菜', 'Spinach', 8, NULL, 20);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '芥蓝', 'Chinese kale', 6, NULL, 21);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '大白菜', 'Chinese cabbage', 10, NULL, 22);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '芹菜', 'Celery', 8, NULL, 23);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '小茴香', 'Cumin seed', 4, NULL, 24);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '普通白菜', NULL, 10, NULL, 25);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '番茄', 'Tomato', 12, NULL, 26);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '辣椒', 'Pepper', 12, NULL, 27);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '茄子', 'Eggplant', 8, NULL, 28);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '黄瓜', 'Cucumber', 12, NULL, 29);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '西葫芦', 'zucchini', 8, NULL, 30);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '豇豆', 'cowpea', 8, NULL, 31);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '节瓜', 'zucchini', 6, NULL, 32);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '冬瓜', 'wax gourd', 8, NULL, 33);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '菜豆', 'kidney bean', 10, NULL, 34);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '萝卜', 'turnip', 8, NULL, 35);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '胡萝卜', 'Carrot', 8, NULL, 36);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '茎用莴苣', 'Stem lettuce', 8, NULL, 37);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '芦笋', 'asparagus', 6, NULL, 38);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '马铃薯', 'Potato', 12, NULL, 39);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '山药', 'Chinese yam', 6, NULL, 40);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '甘薯', 'sweet potato', 8, NULL, 41);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '水芹', 'cress', 6, NULL, 42);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '豆瓣菜', NULL, 4, NULL, 43);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '菱角', NULL, 4, NULL, 44);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '茭白', 'wild rice stem', 6, NULL, 45);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '芡实', NULL, 4, NULL, 46);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '竹笋', 'bamboo shoots', 6, NULL, 47);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '莲藕', 'lotus rhizome', 6, NULL, 48);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '黄花菜', 'Daylily', 4, NULL, 49);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '柑橘', 'Citrus', 12, NULL, 50);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '梨', 'Pear', 12, NULL, 51);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '桃', 'Peach', 8, NULL, 52);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '柿子', 'Persimmon', 6, NULL, 53);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '苹果', 'Apple', 12, NULL, 54);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '枇杷', 'loquat', 6, NULL, 55);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '蓝莓', 'Blueberry', 4, NULL, 56);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '枣', 'jujube', 8, NULL, 57);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '枸杞', 'Matrimony vine', 4, NULL, 58);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '桑葚', 'mulberry', 4, NULL, 59);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '草莓', 'Strawberry', 8, NULL, 60);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '猕猴桃', 'Kiwi Fruit', 8, NULL, 61);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '葡萄', 'Grape', 10, NULL, 62);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '荔枝', 'Litchi', 6, NULL, 63);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '杨梅', 'Waxberry', 6, NULL, 64);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '芒果', 'Mango', 6, NULL, 65);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '橄榄', 'olive', 4, NULL, 66);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '香蕉', 'Banana', 6, NULL, 67);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '石榴', 'pomegranate', 6, NULL, 68);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '椰子', 'coconut', 4, NULL, 69);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '木瓜', 'pawpaw', 6, NULL, 70);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '菠萝', 'pineapple', 6, NULL, 71);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '杏仁', 'almond', 4, NULL, 72);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '西瓜', 'Watermelon', 10, NULL, 73);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '甜瓜', 'melon', 6, NULL, 74);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '油菜', 'Rape', 10, NULL, 75);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '甘蔗', 'sugarcane', 6, NULL, 76);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '甜菜', 'sugarbeet', 6, NULL, 77);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '核桃', 'Walnut', 4, NULL, 78);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '大豆', 'Soya bean', 10, NULL, 79);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '冬油菜', 'Winter Rape', 8, NULL, 80);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '春大豆', 'Spring Soya bean', 6, NULL, 81);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '春油菜', 'soyabena', 4, NULL, 82);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '棉籽', 'Cottonseed', 8, NULL, 83);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '夏大豆', 'Summer Soya bean', 6, NULL, 84);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '葵花籽', 'Sunflower Seeds', 6, NULL, 85);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '花生', 'Peanut', 10, NULL, 86);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '可可豆', NULL, 4, NULL, 87);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '油茶籽', NULL, 4, NULL, 88);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '咖啡豆', 'Coffee Bean', 4, NULL, 89);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '茶', 'Tea', 10, NULL, 90);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '香菇', 'Mushroom', 6, NULL, 91);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '啤酒花', 'hop', 4, NULL, 92);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '菊花', 'chrysanthemum', 4, NULL, 93);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '玫瑰花', 'Rose', 4, NULL, 94);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '烟草', 'Tobacco', 8, NULL, 95);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '平菇', 'oyster mushroom', 6, NULL, 96);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '木耳', 'agarics', 6, NULL, 97);
INSERT INTO "crop" VALUES ('2025-02-21 08:49:39.554817', 1, '金针菇', 'Needle Mushroom', 6, NULL, 98);

-- ----------------------------
-- Table structure for gap
-- ----------------------------
DROP TABLE IF EXISTS "gap";
CREATE TABLE "gap" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "crop_name" VARCHAR,
  "crop_name_cn" VARCHAR,
  "control_target" VARCHAR,
  "control_target_cn" VARCHAR,
  "app_rate_min" NUMERIC,
  "app_rate_max" NUMERIC,
  "water_volumn_min" INTEGER,
  "water_volumn_max" INTEGER,
  "app_method" VARCHAR,
  "app_number" INTEGER,
  "app_interval_min" INTEGER,
  "app_time" VARCHAR,
  "app_time_bbch" VARCHAR,
  "phi" INTEGER,
  "additional_comments" VARCHAR,
  "id" INTEGER NOT NULL,
  "app_rate_unit" VARCHAR NOT NULL,
  "water_volumn_unit" VARCHAR NOT NULL,
  "snapshot_url" VARCHAR,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of gap
-- ----------------------------

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS "message";
CREATE TABLE "message" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "id" INTEGER NOT NULL,
  "sender_id" INTEGER,
  "content" VARCHAR NOT NULL,
  "severity" VARCHAR(6) NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("sender_id") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of message
-- ----------------------------

-- ----------------------------
-- Table structure for message_recipient_rel
-- ----------------------------
DROP TABLE IF EXISTS "message_recipient_rel";
CREATE TABLE "message_recipient_rel" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "id" INTEGER NOT NULL,
  "message_id" INTEGER NOT NULL,
  "recipient_id" INTEGER NOT NULL,
  "is_read" BOOLEAN NOT NULL,
  "read_at" DATETIME,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("message_id") REFERENCES "message" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("recipient_id") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of message_recipient_rel
-- ----------------------------

-- ----------------------------
-- Table structure for note
-- ----------------------------
DROP TABLE IF EXISTS "note";
CREATE TABLE "note" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "id" INTEGER NOT NULL,
  "project_id" INTEGER,
  "task_id" INTEGER,
  "content" VARCHAR NOT NULL,
  "tags" VARCHAR,
  "severity" VARCHAR(6) NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("project_id") REFERENCES "project" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("task_id") REFERENCES "task" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "check_project_or_task" CHECK ((project_id IS NULL AND task_id IS NOT NULL) OR (project_id IS NOT NULL AND task_id IS NULL))
);

-- ----------------------------
-- Records of note
-- ----------------------------

-- ----------------------------
-- Table structure for product
-- ----------------------------
DROP TABLE IF EXISTS "product";
CREATE TABLE "product" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "internal_name" VARCHAR NOT NULL,
  "lead_ai" VARCHAR NOT NULL,
  "stage" VARCHAR(8) NOT NULL,
  "a_number" VARCHAR,
  "product_name" VARCHAR,
  "product_name_cn" VARCHAR,
  "trade_name" VARCHAR,
  "product_origin" VARCHAR,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of product
-- ----------------------------
INSERT INTO "product" VALUES ('2025-02-21 08:49:39.634980', 1, 'Vibrance 500FS/SDX', 'Sedaxane', 'stage_D1', 'A16148F', NULL, NULL, NULL, NULL, 1);
INSERT INTO "product" VALUES ('2025-02-21 08:49:39.634980', 1, 'APN solo 200FS', 'APN', 'stage_D1', 'A19649B', NULL, NULL, NULL, NULL, 2);
INSERT INTO "product" VALUES ('2025-02-21 08:49:39.634980', 1, 'APN+PRS', 'APN', 'stage_D1', 'A25147A', NULL, NULL, NULL, NULL, 3);
INSERT INTO "product" VALUES ('2025-02-21 08:49:39.634980', 1, 'PXD+MTZ EC', 'PXD', 'stage_B', 'A24312A', NULL, NULL, NULL, NULL, 4);
INSERT INTO "product" VALUES ('2025-02-21 08:49:39.634980', 1, 'TYM GR', 'TYM', 'stage_B', 'A23358A', NULL, NULL, NULL, NULL, 5);
INSERT INTO "product" VALUES ('2025-02-21 08:49:39.634980', 1, 'Tymirium 200 FS', 'TYM', 'stage_D1', 'A22940D', NULL, NULL, NULL, NULL, 6);
INSERT INTO "product" VALUES ('2025-02-21 08:49:39.634980', 1, 'Tymirium 450 SC', 'TYM', 'stage_C', 'A22011B', NULL, NULL, NULL, NULL, 7);
INSERT INTO "product" VALUES ('2025-02-21 08:49:39.634980', 1, 'Tymirium 500 FS', 'TYM', 'stage_C', 'A22417C', NULL, NULL, NULL, NULL, 8);

-- ----------------------------
-- Table structure for product_ai
-- ----------------------------
DROP TABLE IF EXISTS "product_ai";
CREATE TABLE "product_ai" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "product_id" INTEGER NOT NULL,
  "abbreviation" VARCHAR,
  "common_name" VARCHAR NOT NULL,
  "common_name_cn" VARCHAR,
  "design_code" VARCHAR,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("product_id") REFERENCES "product" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of product_ai
-- ----------------------------

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS "project";
CREATE TABLE "project" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "project_name" VARCHAR NOT NULL,
  "product_id" INTEGER NOT NULL,
  "indication" VARCHAR(18) NOT NULL,
  "portfolio_contact_id" INTEGER NOT NULL,
  "project_manager" VARCHAR(13) NOT NULL,
  "reg_manager" VARCHAR(12) NOT NULL,
  "project_status" VARCHAR(10) NOT NULL,
  "reg_entity" VARCHAR(13),
  "registration_type" VARCHAR(21) NOT NULL,
  "notification_entrance" VARCHAR,
  "submission_status" VARCHAR(11) NOT NULL,
  "approved_date" DATE,
  "is_three_new" BOOLEAN NOT NULL,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("product_id") REFERENCES "product" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("portfolio_contact_id") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of project
-- ----------------------------
INSERT INTO "project" VALUES ('2025-02-21 08:49:39.650981', 1, 'APN SOLO 200 FS ON RICE', 2, 'Fungicide', 7, 'Siying_Zhu', 'Zheng_Li', 'Finished', NULL, 'FNE', NULL, 'Preparation', NULL, 0, 1);

-- ----------------------------
-- Table structure for project_note_rel
-- ----------------------------
DROP TABLE IF EXISTS "project_note_rel";
CREATE TABLE "project_note_rel" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "project_id" INTEGER NOT NULL,
  "note_id" INTEGER NOT NULL,
  PRIMARY KEY ("project_id", "note_id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("project_id") REFERENCES "project" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("note_id") REFERENCES "note" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of project_note_rel
-- ----------------------------

-- ----------------------------
-- Table structure for sample
-- ----------------------------
DROP TABLE IF EXISTS "sample";
CREATE TABLE "sample" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "product_id" INTEGER NOT NULL,
  "sample_name" VARCHAR NOT NULL,
  "sample_status" VARCHAR(12) NOT NULL,
  "estimated_quantity" INTEGER,
  "estimated_quantity_unit" VARCHAR(14),
  "received_quantity" INTEGER,
  "received_quantity_unit" VARCHAR(14),
  "batch_number" VARCHAR,
  "sealing_number" VARCHAR,
  "production_date" DATE,
  "expiration_date" DATE,
  "shipped_quantity" INTEGER,
  "receiver_information" VARCHAR,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("product_id") REFERENCES "product" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of sample
-- ----------------------------
INSERT INTO "sample" VALUES ('2025-02-21 08:49:39.678590', 1, 1, 'apn 200 sc solo', 'Waiting', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1);

-- ----------------------------
-- Table structure for sample_task_rel
-- ----------------------------
DROP TABLE IF EXISTS "sample_task_rel";
CREATE TABLE "sample_task_rel" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "sample_id" INTEGER NOT NULL,
  "task_id" INTEGER NOT NULL,
  PRIMARY KEY ("sample_id", "task_id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("sample_id") REFERENCES "sample" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("task_id") REFERENCES "task" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of sample_task_rel
-- ----------------------------

-- ----------------------------
-- Table structure for task
-- ----------------------------
DROP TABLE IF EXISTS "task";
CREATE TABLE "task" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "project_id" INTEGER NOT NULL,
  "tags" VARCHAR,
  "task_category" VARCHAR(24),
  "task_name" VARCHAR NOT NULL,
  "task_owner_id" INTEGER NOT NULL,
  "task_status" VARCHAR(10) NOT NULL,
  "expected_delivery_date" DATE,
  "start_year" INTEGER NOT NULL,
  "pi_number" VARCHAR,
  "tk_number" VARCHAR,
  "gap_snapshot" VARCHAR,
  "cost_center" VARCHAR(3),
  "tox_gov_approved" BOOLEAN NOT NULL,
  "ecotox_gov_approved" BOOLEAN NOT NULL,
  "budget_confirmed" BOOLEAN NOT NULL,
  "doc_link" VARCHAR,
  "actual_cost" NUMERIC(10,2),
  "po_placed" BOOLEAN NOT NULL,
  "contract_signed" BOOLEAN NOT NULL,
  "payment_method" VARCHAR(9) NOT NULL,
  "payment_status" VARCHAR(18) NOT NULL,
  "vv_doc_uploaded" BOOLEAN NOT NULL,
  "vv_doc_number" VARCHAR,
  "task_confirmed" BOOLEAN,
  "planned_start" DATE,
  "expected_finish" DATE,
  "actual_start" DATE,
  "actual_finish" DATE,
  "delivery_date" DATE,
  "stuff_days" FLOAT,
  "task_progress" VARCHAR(13) NOT NULL,
  "crop" VARCHAR,
  "target" VARCHAR,
  "cro_id" INTEGER,
  "study_notified" BOOLEAN NOT NULL,
  "estimated_cost" NUMERIC(10,2),
  "analytes" VARCHAR,
  "key_results" VARCHAR(2000),
  "guidelines" VARCHAR,
  "test_item_data_sheet" BOOLEAN NOT NULL,
  "ssd_finished" BOOLEAN NOT NULL,
  "sed_uploaded" BOOLEAN NOT NULL,
  "global_study_manager" VARCHAR,
  "global_study_manager_email" VARCHAR,
  "cro_study_director" VARCHAR,
  "id" INTEGER NOT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("project_id") REFERENCES "project" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("task_owner_id") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("cro_id") REFERENCES "cro" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of task
-- ----------------------------
INSERT INTO "task" VALUES ('2025-02-21 08:49:39.688314', 1, 1, NULL, 'Residue_Study', 'Residue study', 6, 'Idle', '2025-12-31', 2025, NULL, NULL, NULL, NULL, 0, 0, 0, NULL, NULL, 0, 0, 'Half_Half', 'Not_Start', 0, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Not_Start', NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, 1);
INSERT INTO "task" VALUES ('2025-02-21 08:49:39.688314', 1, 1, NULL, 'Tox_Study', 'Acute Oral', 3, 'Go', '2025-12-31', 2025, NULL, NULL, NULL, NULL, 0, 0, 0, NULL, NULL, 0, 0, 'Half_Half', 'Not_Start', 0, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Not_Start', NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, 2);
INSERT INTO "task" VALUES ('2025-02-21 08:49:39.689314', 1, 1, NULL, 'Tox_Study', 'Acute Dermal', 3, 'Go', '2025-12-31', 2025, NULL, NULL, NULL, NULL, 0, 0, 0, NULL, NULL, 0, 0, 'Half_Half', 'Not_Start', 0, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 'Not_Start', NULL, NULL, NULL, 0, NULL, NULL, NULL, NULL, 0, 0, 0, NULL, NULL, NULL, 3);

-- ----------------------------
-- Table structure for task_library
-- ----------------------------
DROP TABLE IF EXISTS "task_library";
CREATE TABLE "task_library" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "id" INTEGER NOT NULL,
  "task_category" VARCHAR(24) NOT NULL,
  "task_name_prefix" VARCHAR NOT NULL,
  "default_task_owner_id" INTEGER,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("default_task_owner_id") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of task_library
-- ----------------------------
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 1, 'Tox_Study', 'Acute Oral', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 2, 'Tox_Study', 'Acute Dermal', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 3, 'Tox_Study', 'Eye Irritation', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 4, 'Tox_Study', 'Skin Irritation', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 5, 'Tox_Study', 'Skin Sensitization', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 6, 'Tox_Study', 'Acute inhalation', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 7, 'Eco_Tox_Study', 'Avian Acute oral toxicity', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 8, 'Eco_Tox_Study', 'Acute toxcity to daphnia', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 9, 'Eco_Tox_Study', 'Algal Growth Inhibition', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 10, 'Eco_Tox_Study', 'Acute toxicity to trichogrammatid', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 11, 'Eco_Tox_Study', 'Acute toxicity to silkworm', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 12, 'Eco_Tox_Study', 'Acute toxicity to ladybird', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 13, 'Eco_Tox_Study', 'Acute oral toxicity to bee', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 14, 'Eco_Tox_Study', 'Acute contact toxicity to bee', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 15, 'Eco_Tox_Study', 'Acute toxicity to earthworm', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 16, 'Eco_Tox_Study', 'Acute fish toxicity', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 17, 'Risk_Assessment', 'Operator risk assessment', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 18, 'Risk_Assessment', 'Environment risk assessment', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 19, 'Risk_Assessment', 'Dietary risk assessment', NULL);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 20, 'Residue_Study', 'Residue study', NULL);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 21, 'Processing_Residue_Study', 'Processing_residue_study', NULL);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 22, 'Unplanned', 'OPEX_SCOPING', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 23, 'Unplanned', 'DRA SCOPING', NULL);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 24, 'Unplanned', 'ERA SCOPING', 2);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 25, 'Unplanned', 'RESIDUE SCOPING', NULL);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 26, 'Unplanned', 'Deco_Doc', 7);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 27, 'Unplanned', 'Statement', NULL);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 28, 'Unplanned', 'Label_Review', 7);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 29, 'Unplanned', 'Check_List', 7);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 30, 'Unplanned', 'Risk_Matrix', 7);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 31, 'Unplanned', 'Gov_Doc_Tox', 3);
INSERT INTO "task_library" VALUES ('2025-02-21 08:49:39.535732', 1, 32, 'Unplanned', 'Gov_Doc_EcoTox', 2);

-- ----------------------------
-- Table structure for task_note_rel
-- ----------------------------
DROP TABLE IF EXISTS "task_note_rel";
CREATE TABLE "task_note_rel" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "task_id" INTEGER NOT NULL,
  "note_id" INTEGER NOT NULL,
  PRIMARY KEY ("task_id", "note_id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("task_id") REFERENCES "task" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("note_id") REFERENCES "note" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of task_note_rel
-- ----------------------------

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "created_at" DATETIME NOT NULL,
  "created_by" INTEGER,
  "email" VARCHAR NOT NULL,
  "name" VARCHAR NOT NULL,
  "role" VARCHAR(16) NOT NULL,
  "id" INTEGER NOT NULL,
  "password_hash" VARCHAR NOT NULL,
  "external_id" VARCHAR,
  "external_auth" VARCHAR,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("created_by") REFERENCES "user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("email" ASC),
  UNIQUE ("name" ASC)
);

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO "user" VALUES ('2025-02-21 08:49:38.047683', 1, 'admin@admin.com', 'Admin', 'Admin', 1, '$2b$12$ThFCuqQCk.ltS3VV.62Lwu8Vbl8lP8nna3MecYxnB5PNOamZh/8y2', NULL, NULL);
INSERT INTO "user" VALUES ('2025-02-21 08:49:38.235079', 1, 'xiaoyan.hu@syngenta.com', 'Xiaoyan Hu', 'Science_Delivery', 2, '$2b$12$bwX5pBqCKqcswHs6c5JZh.yu2Th3rfNzz/NdbNmuPz4j/8q33eNOK', NULL, NULL);
INSERT INTO "user" VALUES ('2025-02-21 08:49:38.416937', 1, 'dandan.ye@syngenta.com', 'Dandan Ye', 'Science_Delivery', 3, '$2b$12$agexl8DYCl8u4j8xCLYz0uzl.bti6aR7NedTEJjbWGvCw9CuinizO', NULL, NULL);
INSERT INTO "user" VALUES ('2025-02-21 08:49:38.594346', 1, 'zhe.dong@syngenta.com', 'Zhe Dong', 'Science_Delivery', 4, '$2b$12$fGkmnsmrtsmEF3GfJfL8We40XoI2BQ1fjUGk2wxx21IAcZgVj.Ww2', NULL, NULL);
INSERT INTO "user" VALUES ('2025-02-21 08:49:38.775000', 1, 'jennifer.zheng@syngenta.com', 'Jennifer Zheng', 'Science_Delivery', 5, '$2b$12$yGBJKoH1.d4yOHUq5xD9tO3ZoVslDreDA2Joyq.LngCMpJn.4U456', NULL, NULL);
INSERT INTO "user" VALUES ('2025-02-21 08:49:38.946152', 1, 'ethan.yang@syngenta.com', 'Ethan Yang', 'Science_Delivery', 6, '$2b$12$SrJu8ZL5HDr.KSYCMKo9UOxF79aDUCMPkAn7tt.9px1yTPYih5ofu', NULL, NULL);
INSERT INTO "user" VALUES ('2025-02-21 08:49:39.146136', 1, 'hank.gao@syngenta.com', 'Hank Gao', 'Portfolio', 7, '$2b$12$9uibJ48bFtCU8Exg2cAaS.4idOhZE2SzgzfgFREoMosC3w/kqkiw.', NULL, NULL);
INSERT INTO "user" VALUES ('2025-02-21 08:49:39.332472', 1, 'niphee.fei@syngenta.com', 'Niphee Fei', 'Operation', 8, '$2b$12$3CQRwfABupl8w4sneJGB6.3sHAK6Zlwq5Dxo8vOk.BH/oTyKVygry', NULL, NULL);
INSERT INTO "user" VALUES ('2025-02-21 08:49:39.512898', 1, 'jessica.zhang@syngenta.com', 'Jessica Zhang', 'Admin', 9, '$2b$12$0owi/CR13ZyBkSJHJduqEuryirtkv1CGR0B5JKIYINmEOfBRbqEKm', NULL, NULL);

-- ----------------------------
-- Indexes structure for table cro
-- ----------------------------
CREATE UNIQUE INDEX "ix_cro_cro_name"
ON "cro" (
  "cro_name" ASC
);

-- ----------------------------
-- Indexes structure for table crop
-- ----------------------------
CREATE UNIQUE INDEX "ix_crop_crop_name_cn"
ON "crop" (
  "crop_name_cn" ASC
);
CREATE INDEX "ix_crop_crop_name_en"
ON "crop" (
  "crop_name_en" ASC
);

PRAGMA foreign_keys = true;
