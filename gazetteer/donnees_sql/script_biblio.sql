
-- ----------------------------------------------------
-- Table `gazetteer`.`biblio`
-- ----------------------------------------------------
DROP TABLE IF EXISTS `gazetteer`.`biblio` ;
CREATE TABLE IF NOT EXISTS `gazetteer`.`biblio` (
  `biblio_id` INT NOT NULL AUTO_INCREMENT COMMENT '	',
  `biblio_titre` TEXT NOT NULL,
  `biblio_auteur` TEXT NOT NULL,
  `biblio_date` TEXT NULL,
  `biblio_lieu` TEXT NULL,
  `biblio_type` TEXT NOT NULL,
  PRIMARY KEY (`biblio_id`))
ENGINE = InnoDB;
COMMIT;
