-- -----------------------------------------------------
-- Table `gazetteer`.`relation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`relation` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`relation` (
  `relation_id` INT NOT NULL AUTO_INCREMENT,
  `relation_biblio_id` INT NOT NULL,
  `relation_place_id` INT NOT NULL,
  PRIMARY KEY (`relation_id`),
  INDEX `fk_relation_1_idx` (`relation_place_id` ASC),
  INDEX `fk_relation_2_idx` (`relation_biblio_id` ASC),
  CONSTRAINT `fk_relation_1`
    FOREIGN KEY (`relation_place_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_relation_2`
    FOREIGN KEY (`relation_biblio_id`)
    REFERENCES `gazetteer`.`biblio` (`biblio_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;