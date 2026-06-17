-- ============================================================
-- Nutrition Recommender System - MySQL Schema
-- Database: nutrition_recommender
-- ============================================================

CREATE DATABASE IF NOT EXISTS nutrition_recommender
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE nutrition_recommender;

-- ============================================================
-- TABLE: users
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    full_name   VARCHAR(100)  NOT NULL,
    email       VARCHAR(150)  NOT NULL UNIQUE,
    password    VARCHAR(255)  NOT NULL,
    is_active   BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: user_profiles
-- ============================================================
CREATE TABLE IF NOT EXISTS user_profiles (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT           NOT NULL UNIQUE,
    age             INT           NOT NULL CHECK (age BETWEEN 1 AND 120),
    gender          ENUM('male','female','other') NOT NULL,
    height_cm       DECIMAL(5,2)  NOT NULL,
    weight_kg       DECIMAL(5,2)  NOT NULL,
    bmi             DECIMAL(4,2)  GENERATED ALWAYS AS
                      (ROUND(weight_kg / ((height_cm / 100) * (height_cm / 100)), 2))
                      STORED,
    activity_level  ENUM('sedentary','lightly_active','moderately_active','very_active') NOT NULL,
    nutrition_goal  ENUM('weight_loss','weight_gain','muscle_gain','maintenance') NOT NULL,
    daily_calorie_goal INT         NOT NULL DEFAULT 2000,
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: foods
-- ============================================================
CREATE TABLE IF NOT EXISTS foods (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    food_name       VARCHAR(150)  NOT NULL,
    category        VARCHAR(100)  NOT NULL,
    calories        DECIMAL(7,2)  NOT NULL,
    protein         DECIMAL(6,2)  NOT NULL DEFAULT 0,
    carbohydrates   DECIMAL(6,2)  NOT NULL DEFAULT 0,
    fat             DECIMAL(6,2)  NOT NULL DEFAULT 0,
    fiber           DECIMAL(6,2)  NOT NULL DEFAULT 0,
    serving_size    VARCHAR(50)   NOT NULL DEFAULT '100g',
    image_url       TEXT,
    recommended_goal VARCHAR(50),
    is_active       BOOLEAN       NOT NULL DEFAULT TRUE,
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_recommended_goal (recommended_goal),
    FULLTEXT INDEX idx_food_name_ft (food_name)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: food_logs
-- ============================================================
CREATE TABLE IF NOT EXISTS food_logs (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT           NOT NULL,
    food_id         INT           NOT NULL,
    quantity        DECIMAL(6,2)  NOT NULL DEFAULT 1.0,
    unit            VARCHAR(30)   NOT NULL DEFAULT 'serving',
    meal_type       ENUM('breakfast','lunch','dinner','snack') NOT NULL DEFAULT 'snack',
    calories        DECIMAL(7,2)  NOT NULL,
    protein         DECIMAL(6,2)  NOT NULL DEFAULT 0,
    carbohydrates   DECIMAL(6,2)  NOT NULL DEFAULT 0,
    fat             DECIMAL(6,2)  NOT NULL DEFAULT 0,
    fiber           DECIMAL(6,2)  NOT NULL DEFAULT 0,
    logged_at       DATE          NOT NULL DEFAULT (CURRENT_DATE),
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    INDEX idx_user_date (user_id, logged_at),
    INDEX idx_food_id (food_id)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: recommendations
-- ============================================================
CREATE TABLE IF NOT EXISTS recommendations (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT           NOT NULL,
    food_id         INT           NOT NULL,
    recommendation_type ENUM('rule_based','decision_tree','knn','hybrid') NOT NULL,
    score           DECIMAL(5,4)  NOT NULL DEFAULT 0,
    reason          TEXT,
    generated_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE,
    INDEX idx_user_type (user_id, recommendation_type),
    INDEX idx_generated_at (generated_at)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: meal_plans
-- ============================================================
CREATE TABLE IF NOT EXISTS meal_plans (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT           NOT NULL,
    plan_date       DATE          NOT NULL,
    breakfast_food_id INT,
    lunch_food_id   INT,
    dinner_food_id  INT,
    snack_food_id   INT,
    total_calories  DECIMAL(7,2)  NOT NULL DEFAULT 0,
    nutrition_goal  VARCHAR(50),
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (breakfast_food_id) REFERENCES foods(id) ON DELETE SET NULL,
    FOREIGN KEY (lunch_food_id)     REFERENCES foods(id) ON DELETE SET NULL,
    FOREIGN KEY (dinner_food_id)    REFERENCES foods(id) ON DELETE SET NULL,
    FOREIGN KEY (snack_food_id)     REFERENCES foods(id) ON DELETE SET NULL,
    UNIQUE KEY uq_user_date (user_id, plan_date),
    INDEX idx_user_date (user_id, plan_date)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: nutrition_summaries (pre-aggregated for performance)
-- ============================================================
CREATE TABLE IF NOT EXISTS nutrition_summaries (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT           NOT NULL,
    summary_date    DATE          NOT NULL,
    total_calories  DECIMAL(8,2)  NOT NULL DEFAULT 0,
    total_protein   DECIMAL(7,2)  NOT NULL DEFAULT 0,
    total_carbs     DECIMAL(7,2)  NOT NULL DEFAULT 0,
    total_fat       DECIMAL(7,2)  NOT NULL DEFAULT 0,
    total_fiber     DECIMAL(7,2)  NOT NULL DEFAULT 0,
    meal_count      INT           NOT NULL DEFAULT 0,
    created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uq_user_date (user_id, summary_date),
    INDEX idx_user_date (user_id, summary_date)
) ENGINE=InnoDB;

-- ============================================================
-- TABLE: refresh_tokens
-- ============================================================
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT           NOT NULL,
    token       VARCHAR(512)  NOT NULL UNIQUE,
    expires_at  DATETIME      NOT NULL,
    revoked     BOOLEAN       NOT NULL DEFAULT FALSE,
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_token (token),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB;
