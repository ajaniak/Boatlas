DROP TABLE IF EXISTS `gazetteer`.`link` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`link` (
  `link_id` INT NOT NULL AUTO_INCREMENT,
  `link_relation_type` VARCHAR(45) NOT NULL,
  `link_relation_description` VARCHAR(240),
  PRIMARY KEY (`link_id`))
ENGINE = InnoDB;
