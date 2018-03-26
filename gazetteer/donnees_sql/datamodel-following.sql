DROP TABLE IF EXISTS `gazetteer`.`link_lieu` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`link_lieu` (
  `link_id` INT NOT NULL,
  `link_parent` INT NOT NULL,
  `link_child` INT NOT NULL,
  PRIMARY KEY (`link_id`),
  INDEX `fk_link_1_idx` (`link_parent` ASC),
  CONSTRAINT `fk_link_1`
    FOREIGN KEY (`link_parent`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
COMMIT;
