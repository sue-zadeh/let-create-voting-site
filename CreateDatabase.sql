-- SET SQL_SAFE_UPDATES = 0;

SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `user_competition_roles` ;
DROP TABLE IF EXISTS `votes` ;
DROP TABLE IF EXISTS `user_last_message` ;
DROP TABLE IF EXISTS `instant_messages` ;
DROP TABLE IF EXISTS `donation_receipts` ;
DROP TABLE IF EXISTS `charities` ;
DROP TABLE IF EXISTS `announcements` ;
DROP TABLE IF EXISTS `appeals` ;
DROP TABLE IF EXISTS `bans` ;
DROP TABLE IF EXISTS `competitors` ;
DROP TABLE IF EXISTS `events` ;
DROP TABLE IF EXISTS `replies` ;
DROP TABLE IF EXISTS `messages` ;
DROP TABLE IF EXISTS `site_wide_ban_appeals` ;
DROP TABLE IF EXISTS `site_wide_bans` ;
DROP TABLE IF EXISTS `competitions` ;
DROP TABLE IF EXISTS `applications` ;
DROP TABLE IF EXISTS `users` ;
DROP TABLE IF EXISTS `user_competition_moderators`;
DROP TABLE IF EXISTS `themes`;

DROP TABLE IF EXISTS `gallery_themes`;



DROP VIEW IF EXISTS `user_ban_status`;




-- -----------------------------------------------------
-- Table `competitions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `competitions` (
  `competition_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `description` TEXT NOT NULL,
  `charity_id` INT NULL,
  PRIMARY KEY (`competition_id`),
  INDEX `fk2_idx` (`charity_id` ASC) VISIBLE);


-- -----------------------------------------------------
-- Table `announcements`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `announcements` (
  `announcement_id` INT NOT NULL AUTO_INCREMENT,
  `competition_id` INT NULL DEFAULT NULL,
  `text` TEXT NOT NULL,
  `expiry_date` DATE NOT NULL,
  `announcement_time` DATETIME NOT NULL,
  PRIMARY KEY (`announcement_id`),
  INDEX `fk1_idx` (`competition_id` ASC) VISIBLE,
  CONSTRAINT `announcements_ibfk_1`
    FOREIGN KEY (`competition_id`)
    REFERENCES `competitions` (`competition_id`)
    ON DELETE CASCADE);

-- -----------------------------------------------------
-- Table `users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL,
  `username_visible` TINYINT NOT NULL DEFAULT 0,
  `password_hash` VARCHAR(64) NOT NULL,
  `email` VARCHAR(320) NOT NULL,
  `email_visible` TINYINT NOT NULL DEFAULT 0,
  `first_name` VARCHAR(50) NOT NULL DEFAULT '',
  `first_name_visible` TINYINT NOT NULL DEFAULT 0,
  `last_name` VARCHAR(50) NOT NULL DEFAULT '',
  `last_name_visible` TINYINT NOT NULL DEFAULT 0,
  `location` VARCHAR(50) NOT NULL DEFAULT '',
  `location_visible` TINYINT NOT NULL DEFAULT 0,
  `description` VARCHAR(255) NOT NULL DEFAULT '',

  `description_visible` TINYINT NOT NULL DEFAULT 0,
  `profile_image` VARCHAR(255) NOT NULL DEFAULT '',

  `is_active` TINYINT(1) NOT NULL DEFAULT '1',
  `site_role` ENUM('voter', 'site admin') NOT NULL,
  `publicly_visible` TINYINT NOT NULL DEFAULT 1,
  PRIMARY KEY (`user_id`));


-- -----------------------------------------------------
-- Table `instant_messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `instant_messages` (
  `im_id` INT NOT NULL AUTO_INCREMENT,
  `to_user` INT NOT NULL,
  `from_user` INT NOT NULL,
  `message` TEXT NOT NULL,
  `sent` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`im_id`),
  INDEX `fk_idx` (`to_user` ASC) VISIBLE,
  INDEX `fk1_idx` (`from_user` ASC) VISIBLE,
  CONSTRAINT `fk`
    FOREIGN KEY (`to_user`)
    REFERENCES `users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk1`
    FOREIGN KEY (`from_user`)
    REFERENCES `users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `user_last_viewed`
-- -----------------------------------------------------
-- CREATE TABLE user_last_viewed (
--     user_id VARCHAR(255) PRIMARY KEY,
--     last_viewed_time TIMESTAMP
-- );

CREATE TABLE IF NOT EXISTS `user_last_message` (
    user_id INT PRIMARY KEY,
    last_message_id INT,
    FOREIGN KEY (last_message_id) REFERENCES instant_messages(im_id) ON DELETE SET NULL
);


-- -----------------------------------------------------
-- Table `charities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `charities` (
  `charity_id` INT NOT NULL AUTO_INCREMENT,
  `competition_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `services_registration` VARCHAR(45) NOT NULL,
  `bank_account_number` VARCHAR(25) NOT NULL,
  `ird_number` CHAR(11) NOT NULL,
  `date_submitted` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('pending', 'not approved', 'active', 'revoked') NOT NULL,
  `official_stamp` MEDIUMBLOB NOT NULL,
  `authorisor_name` VARCHAR(100) NOT NULL,
  `authorisor_designation` VARCHAR(100) NOT NULL,
  `authorisor_signature` BLOB NOT NULL,
  PRIMARY KEY (`charity_id`),
  INDEX `fk_idx` (`competition_id` ASC) VISIBLE,
  CONSTRAINT `charities_fk`
    FOREIGN KEY (`competition_id`)
    REFERENCES `competitions` (`competition_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

ALTER TABLE competitions
ADD CONSTRAINT `fk2`
    FOREIGN KEY (`charity_id`)
    REFERENCES `charities` (`charity_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION;

-- -----------------------------------------------------
-- Table `bans`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bans` (
  `ban_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `competition_id` INT NOT NULL,
  `ban_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `reason` TEXT NOT NULL,
  `active` TINYINT(1) NOT NULL DEFAULT 1,
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  INDEX `competition_id` (`competition_id` ASC) VISIBLE,
  PRIMARY KEY (`ban_id`),
  CONSTRAINT `bans_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`)
    ON DELETE CASCADE,
  CONSTRAINT `bans_ibfk_2`
    FOREIGN KEY (`competition_id`)
    REFERENCES `competitions` (`competition_id`)
    ON DELETE CASCADE
);


-- -----------------------------------------------------
-- Table `appeals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `appeals` (
  `appeal_id` INT NOT NULL AUTO_INCREMENT,
  `ban_id` INT NOT NULL,
  `competition_id` INT NOT NULL,
  `appeal_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('pending', 'approved', 'denied') NOT NULL DEFAULT 'pending',
  `reason` TEXT NULL DEFAULT NULL,
  `response` TEXT NULL DEFAULT NULL,
  `response_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appeal_id`),
  INDEX `fk_idx` (`ban_id` ASC) VISIBLE,
  CONSTRAINT `appeals_fk`
    FOREIGN KEY (`ban_id`)
    REFERENCES `bans` (`ban_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `appeals_competition_fk`
    FOREIGN KEY (`competition_id`)
    REFERENCES `competitions` (`competition_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    );


-- -----------------------------------------------------
-- Table `applications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `applications` (
  `application_id` INT NOT NULL AUTO_INCREMENT,
  `application_by_user` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `description` TEXT NOT NULL,
  `visible` TINYINT NOT NULL DEFAULT '1',
  `application_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('pending', 'rejected', 'cancelled', 'approved') NOT NULL DEFAULT 'pending',
  `reason` VARCHAR(45) NOT NULL DEFAULT '',
  PRIMARY KEY (`application_id`),
  INDEX `fk2_idx` (`application_by_user` ASC) VISIBLE,
  CONSTRAINT `applications_ibfk_1`
    FOREIGN KEY (`application_by_user`)
    REFERENCES `users` (`user_id`)
    ON DELETE CASCADE);


-- -----------------------------------------------------
-- Table `events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `events` (
  `event_id` INT NOT NULL AUTO_INCREMENT,
  `competition_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `description` TEXT NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `is_visible` BOOLEAN NOT NULL DEFAULT FALSE, -- Deprecated: Do not use, going to be deleted
  `status` ENUM('active', 'closed', 'finalised') NOT NULL,
  PRIMARY KEY (`event_id`),
  INDEX `fk1_idx` (`competition_id` ASC) VISIBLE,
  CONSTRAINT `events_ibfk_1`
    FOREIGN KEY (`competition_id`)
    REFERENCES `competitions` (`competition_id`));


-- -----------------------------------------------------
-- Table `competitors`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `competitors` (
  `competitor_id` INT NOT NULL AUTO_INCREMENT,
  `event_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `description` TEXT NOT NULL,
  `image` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`competitor_id`),
  INDEX `competition_id` (`event_id` ASC) VISIBLE,
  CONSTRAINT `competitors_ibfk_1`
    FOREIGN KEY (`event_id`)
    REFERENCES `events` (`event_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);


-- -----------------------------------------------------
-- Table `donation_receipts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `donation_receipts` (
  `receipt_no` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `charity_id` INT NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  `donation_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `donor_full_name` VARCHAR(100) NOT NULL,
  `pay_provider_confirmation` VARCHAR(100) NOT NULL,
  `cancelled` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`receipt_no`),
  INDEX `fk_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk1_idx` (`charity_id` ASC) VISIBLE,
  CONSTRAINT `donation_receipts_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `donation_receipts_fk1`
    FOREIGN KEY (`charity_id`)
    REFERENCES `charities` (`charity_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `messages` (
  `message_id` INT NOT NULL AUTO_INCREMENT,
  `competition_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`),
  INDEX `competition_id` (`competition_id` ASC) VISIBLE,
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `messages_ibfk_1`
    FOREIGN KEY (`competition_id`)
    REFERENCES `competitions` (`competition_id`),
  CONSTRAINT `messages_ibfk_2`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`));


-- -----------------------------------------------------
-- Table `replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `replies` (
  `reply_id` INT NOT NULL AUTO_INCREMENT,
  `message_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reply_id`),
  INDEX `message_id` (`message_id` ASC) VISIBLE,
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `replies_ibfk_1`
    FOREIGN KEY (`message_id`)
    REFERENCES `messages` (`message_id`)
    ON DELETE CASCADE,
  CONSTRAINT `replies_ibfk_3`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`));


-- -----------------------------------------------------
-- Table `site_wide_bans`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `site_wide_bans` (
  `site_wide_ban_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `ban_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `reason` TEXT NOT NULL,
  `active` TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`site_wide_ban_id`),
  INDEX `user_id` (`user_id` ASC) VISIBLE,
  CONSTRAINT `site_wide_bans_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`)
);



-- -----------------------------------------------------
-- Table `site_wide_ban_appeals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `site_wide_ban_appeals` (
  `appeal_id` INT NOT NULL AUTO_INCREMENT,
  `site_wide_ban_id` INT NOT NULL,
  `appeal_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('pending', 'approved', 'denied') NOT NULL DEFAULT 'pending',
  `reason` TEXT NULL DEFAULT NULL,
  `response` TEXT NULL DEFAULT NULL,
  `response_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`appeal_id`),
  INDEX `site_wide_ban_id` (`site_wide_ban_id` ASC) VISIBLE,
  CONSTRAINT `site_wide_ban_appeals_ibfk_1`
    FOREIGN KEY (`site_wide_ban_id`)
    REFERENCES `site_wide_bans` (`site_wide_ban_id`)
    ON DELETE CASCADE);


-- -----------------------------------------------------
-- Table `user_competition_roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user_competition_roles` (
  `user_id` INT NOT NULL,
  `competition_id` INT NOT NULL,
  `role` ENUM('admin', 'scrutineer') NOT NULL,
  PRIMARY KEY (`user_id`, `competition_id`),
  INDEX `f2_idx` (`competition_id` ASC) VISIBLE,
  CONSTRAINT `user_competition_roles_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`),
  CONSTRAINT `user_competition_roles_ibfk_2`
    FOREIGN KEY (`competition_id`)
    REFERENCES `competitions` (`competition_id`));

    -- -----------------------------------------------------
-- Table `user_competition_moderators`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user_competition_moderators` (
  `user_id` INT NOT NULL,
  `competition_id` INT NOT NULL,
  PRIMARY KEY (`user_id`, `competition_id`),
  INDEX `f2_idx` (`competition_id` ASC) VISIBLE,
  CONSTRAINT `user_competition_moderators_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`),
  CONSTRAINT `user_competition_moderators_ibfk_2`
    FOREIGN KEY (`competition_id`)
    REFERENCES `competitions` (`competition_id`)
);


-- -----------------------------------------------------
-- Table `votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `votes` (
  `user_id` INT NOT NULL,
  `competitor_id` INT NOT NULL,
  `event_id` INT NOT NULL, -- Deprecated: Do not use, going to be deleted
  `vote_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ip_address` VARCHAR(45) NOT NULL,
  `invalid` TINYINT NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`, `competitor_id`),
  INDEX `competitor_id` (`competitor_id` ASC) VISIBLE,
  CONSTRAINT `votes_ibfk_1`
    FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`),
  CONSTRAINT `votes_ibfk_2`
    FOREIGN KEY (`competitor_id`)
    REFERENCES `competitors` (`competitor_id`));


-- -----------------------------------------------------
-- Table `themes`
-- -----------------------------------------------------
   CREATE TABLE themes (
    style_id INT AUTO_INCREMENT PRIMARY KEY,
    competition_id INT,
    theme_name VARCHAR(100),
    background_color VARCHAR(20),
    topic_text_color VARCHAR(20),
    topic_font_size VARCHAR(10),
    main_text_color VARCHAR(20),
    main_font_size VARCHAR(10),
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (competition_id) REFERENCES competitions(competition_id)
);


-- -----------------------------------------------------
-- Table `gallery_themes`
-- -----------------------------------------------------

CREATE TABLE gallery_themes (
    gallery_id INT AUTO_INCREMENT PRIMARY KEY,
    competition_id INT,
    theme_name VARCHAR(100),
    screenshot_path VARCHAR(255),
    background_color VARCHAR(20),
    topic_text_color VARCHAR(20),
    topic_font_size VARCHAR(10),
    main_text_color VARCHAR(20),
    main_font_size VARCHAR(10)
);

-- ------------------------------------------------------
-- View `user_ban_status`
-- ------------------------------------------------------
CREATE VIEW user_ban_status AS
SELECT 
    u.user_id,
    c.competition_id,
    c.name AS competition_name,
    CASE 
        WHEN b.user_id IS NOT NULL THEN 'Banned'
        ELSE 'Active'
    END AS status,
    CASE 
        WHEN b.user_id IS NOT NULL THEN 1
        ELSE 0
    END AS banned,
    IFNULL(b.reason,'N/A') AS reason,
    IFNULL(b.ban_date, "N/A") AS ban_date
FROM users u
CROSS JOIN competitions c 
LEFT JOIN bans b ON b.user_id = u.user_id AND b.competition_id = c.competition_id AND b.active;  



  
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;