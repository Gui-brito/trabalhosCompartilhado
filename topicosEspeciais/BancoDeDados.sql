CREATE DATABASE 'topicosEspeciais'; --Ou CREATE SCHEMA (no meu foi SCHEMA)
CREATE TABLE `topicosEspeciais`.`userLogin` (
  `usuario` VARCHAR(25) CHARACTER SET 'ascii' NOT NULL,
  `senha` VARCHAR(25) NOT NULL,
  `user_admin` TINYINT NULL,
  PRIMARY KEY (`usuario`));
INSERT INTO `topicosEspeciais`.`login` (`usuario`, `senha`, `admin`) VALUES ('guibrito', 'guibrito', '1');
INSERT INTO `topicosEspeciais`.`login` (`usuario`, `senha`, `admin`) VALUES ('otavio', '123456', '1');

