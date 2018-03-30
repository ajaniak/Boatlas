DROP TABLE IF EXISTS `gazetteer`.`link` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`link` (
  `link_id` INT NOT NULL AUTO_INCREMENT,
  `link_place1_id` INT NOT NULL,
  `link_place2_id` INT NOT NULL,
  `link_relation_type` VARCHAR(45) NOT NULL,
  `link_relation_description`VARCHAR(240),
  INDEX `fk_link_1_idx` (`link_place1_id` ASC),
  INDEX `fk_link_2_idx` (`link_place2_id` ASC),
  PRIMARY KEY (`link_id`),
  CONSTRAINT `fk_link_1`
    FOREIGN KEY (`link_place1_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_link_2`
    FOREIGN KEY (`link_place2_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
