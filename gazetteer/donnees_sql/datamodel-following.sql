DROP TABLE IF EXISTS `gazetteer`.`link_type` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`link_type` (
  `link_type_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `link_type_name`  VARCHAR(45) NOT NULL,
  `link_type_description`VARCHAR(240) NOT NULL,
  PRIMARY KEY (`link_type_id`))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `gazetteer`.`link` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`link` (
  `link_id` SMALLINT NOT NULL AUTO_INCREMENT,
  `link_place1_id` SMALLINT NOT NULL,
  `link_relation_type_id` SMALLINT NOT NULL,
  `link_place2_id` SMALLINT NOT NULL,

  PRIMARY KEY (`link_id`),
  CONSTRAINT `fk_link_1`
    FOREIGN KEY (`link_place1_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    CONSTRAINT `fk_link_2`
        FOREIGN KEY (`link_relation_type_id`)
        REFERENCES `gazetteer`.`link_type` (`link_type_id`)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION,
  CONSTRAINT `fk_link_3`
    FOREIGN KEY (`link_place2_id`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
