DROP TABLE IF EXISTS `gazetteer`.`following` ;

CREATE TABLE IF NOT EXISTS `gazetteer`.`following` (
  `f_connection_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `f_place_from` INT NOT NULL,
  `f_place_to` INT NOT NULL,
  CONSTRAINT `fk_following_1`
    FOREIGN KEY (`f_place_from`)
    REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_following_2`
  FOREIGN KEY (`f_place_to`)
  REFERENCES `gazetteer`.`place` (`place_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
COMMIT;
