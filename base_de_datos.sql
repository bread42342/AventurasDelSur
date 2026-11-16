CREATE DATABASE IF NOT EXISTS aventurasbd CHARACTER SET utf8mb4;
CREATE USER IF NOT EXISTS 'adminaventura'@'localhost' IDENTIFIED BY '2026';
GRANT ALL PRIVILEGES ON aventurasbd.* TO 'adminaventura'@'localhost';
FLUSH PRIVILEGES;
USE aventurasbd;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS=0;
DELETE FROM `core_configuracionecoparque`;
DELETE FROM `cuentas_usuario`;
DELETE FROM `cuentas_perfil`;
DELETE FROM `experiencias_categoria`;
DELETE FROM `experiencias_experiencia`;
DELETE FROM `experiencias_inscripcion`;

INSERT INTO `core_configuracionecoparque` (`id`, `nombre`, `descripcion`, `direccion`, `telefono`, `correo`, `horario_apertura`, `horario_cierre`, `politica_cancelacion`) VALUES (1, 'Aventuras del Sur', 'Ecoparque y reserva natural con experiencias guiadas en el sur de Chile.', 'Camino a Volcán Osorno km 12, Puerto Varas', '+56965001122', 'contacto@aventurasdelsur.cl', '09:00:00', '18:00:00', 'Las reservas con pago pendiente se pueden cancelar sin costo. Las reservas con pago confirmado se gestionan con el administrador.');

INSERT INTO `cuentas_usuario` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `rol`) VALUES (1, 'pbkdf2_sha256$1200000$gW2QOYg1KXuQ7idhzlkrnZ$iaFEfFCWZ57qYGkcRceBADhe6ygVNIUiy1GHyanrSrY=', NULL, 1, 'admin', 'Sebastian', 'Gatica', 'SebastianGatica@aventurasdelsur.cl', 1, 1, '2026-11-15 21:50:29', 'admin');
INSERT INTO `cuentas_usuario` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `rol`) VALUES (2, 'pbkdf2_sha256$1200000$NbtEqMWP1sgGENkxlx2Mge$3Xs0bwnIQ25uWGGQpK8VF4doeyFsrkM6+kztZ2sK00k=', NULL, 0, 'trabajador1', 'Rick', 'Grimes', 'RickGrimes@aventurasdelsur.cl', 0, 1, '2026-11-15 21:50:29', 'guia');
INSERT INTO `cuentas_usuario` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `rol`) VALUES (3, 'pbkdf2_sha256$1200000$MfVWzIZc5BvLAzdNN8CfLa$sNFC6lAqY43i/HsMhKWXzxCJmVFN0jdqVhXOwB1gNIU=', NULL, 0, 'trabajador2', 'Daryl', 'Dixon', 'DarylDixon@aventurasdelsur.cl', 0, 1, '2026-11-15 21:50:29', 'guia');
INSERT INTO `cuentas_usuario` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `rol`) VALUES (4, 'pbkdf2_sha256$1200000$xn69lyO8MZAlqzw1P9KKyR$Pv5lTsnq4fIqFwMz+zaoOcAcs9KReBmtufT6GFy1fNU=', NULL, 0, 'cliente1', 'Carol', 'Peletier', 'CarolPeletier@gmail.com', 0, 1, '2026-11-15 21:50:29', 'turista');
INSERT INTO `cuentas_usuario` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `rol`) VALUES (5, 'pbkdf2_sha256$1200000$BfK6OA9TB96sEM8MV31jbI$9tW97a43+M2O8fA0Mfa3/b+I3cyaDZ1WqzpXbsfCIN4=', NULL, 0, 'cliente2', 'Maggie', 'Greene', 'MaggieGreene@gmail.com', 0, 1, '2026-11-15 21:50:30', 'turista');

INSERT INTO `cuentas_perfil` (`id`, `usuario_id`, `telefono`, `documento`, `ciudad`) VALUES (1, 1, '+56982345671', '', 'Puerto Varas');
INSERT INTO `cuentas_perfil` (`id`, `usuario_id`, `telefono`, `documento`, `ciudad`) VALUES (2, 2, '+56991234502', '', 'Puerto Varas');
INSERT INTO `cuentas_perfil` (`id`, `usuario_id`, `telefono`, `documento`, `ciudad`) VALUES (3, 3, '+56978451263', '', 'Puerto Montt');
INSERT INTO `cuentas_perfil` (`id`, `usuario_id`, `telefono`, `documento`, `ciudad`) VALUES (4, 4, '+56965432198', '', 'Santiago');
INSERT INTO `cuentas_perfil` (`id`, `usuario_id`, `telefono`, `documento`, `ciudad`) VALUES (5, 5, '+56957123864', '', 'Concepción');

INSERT INTO `experiencias_categoria` (`id`, `nombre`, `descripcion`, `activo`) VALUES (1, 'Trekking', 'Caminatas guiadas por volcanes, cerros y bosque nativo del sur de Chile.', 1);
INSERT INTO `experiencias_categoria` (`id`, `nombre`, `descripcion`, `activo`) VALUES (2, 'Canopy', 'Tirolesas entre las copas de los árboles.', 1);
INSERT INTO `experiencias_categoria` (`id`, `nombre`, `descripcion`, `activo`) VALUES (3, 'Arriendo de equipos', 'Arriendo de bicicletas, bastones y equipo de camping.', 1);
INSERT INTO `experiencias_categoria` (`id`, `nombre`, `descripcion`, `activo`) VALUES (4, 'Kayak y rafting', 'Remo en lagos y descenso de ríos de aguas claras.', 1);
INSERT INTO `experiencias_categoria` (`id`, `nombre`, `descripcion`, `activo`) VALUES (5, 'Observación de aves', 'Salidas de avistamiento con guía especializado.', 1);
INSERT INTO `experiencias_categoria` (`id`, `nombre`, `descripcion`, `activo`) VALUES (6, 'Termas y relajo', 'Baños termales rodeados de bosque y volcanes.', 1);
INSERT INTO `experiencias_categoria` (`id`, `nombre`, `descripcion`, `activo`) VALUES (7, 'Cabalgatas', 'Recorridos a caballo por valles y orillas de lago.', 1);
INSERT INTO `experiencias_categoria` (`id`, `nombre`, `descripcion`, `activo`) VALUES (8, 'Turismo cultural', 'Visitas a ferias, museos y rutas gastronómicas de la región.', 1);

INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (1, 'Trekking Volcán Osorno, Puerto Varas', 'Ascenso guiado hasta el refugio con vista al lago Llanquihue.', 32000, 12, '2026-11-21 00:00:00', 1, 2, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (2, 'Trekking Parque Nacional Villarrica, Pucón', 'Caminata de 5 horas por bosque de araucarias y coladas de lava.', 35000, 10, '2026-11-25 00:00:00', 1, 2, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (3, 'Trekking Reserva Altos de Lircay, Talca', 'Recorrido hasta el Mirador del Valle del Venado en la precordillera.', 22000, 15, '2026-11-22 00:00:00', 1, 2, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (4, 'Canopy Lago Calafquén, Villarrica', 'Circuito de 8 tirolesas con vista al lago y al volcán.', 38000, 8, '2026-11-23 00:00:00', 2, 2, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (5, 'Cabalgata Valle del Río Maullín, Puerto Montt', 'Paseo a caballo de 3 horas por el valle y la ribera.', 30000, 8, '2026-11-28 00:00:00', 7, 2, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (6, 'Termas Geométricas, Panguipulli', 'Jornada de relajo en pozones termales entre pasarelas de madera.', 45000, 20, '2026-12-01 00:00:00', 6, 2, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (7, 'Trekking Parque Nacional Conguillío, Temuco', 'Sendero Sierra Nevada entre araucarias milenarias y lagunas.', 34000, 12, '2026-11-27 00:00:00', 1, 2, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (8, 'Kayak Lago Panguipulli, Los Ríos', 'Remada de 3 horas por las aguas del lago con picnic incluido.', 28000, 10, '2026-11-22 00:00:00', 4, 3, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (9, 'Rafting Río Trancura, Pucón', 'Descenso de aguas bravas clase III con equipo completo.', 36000, 10, '2026-11-26 00:00:00', 4, 3, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (10, 'Navegación en kayak Río Calle-Calle, Valdivia', 'Paseo tranquilo entre humedales y lobos marinos.', 26000, 10, '2026-11-24 00:00:00', 4, 3, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (11, 'Avistamiento de aves Santuario Río Cruces, Valdivia', 'Salida de amanecer con binoculares para ver cisnes de cuello negro.', 18000, 8, '2026-11-20 00:00:00', 5, 3, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (12, 'Ruta de los Humedales de Chiloé, Ancud', 'Avistamiento de aves migratorias y visita a palafitos.', 24000, 8, '2026-11-29 00:00:00', 5, 3, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (13, 'Ruta gastronómica Mercado Fluvial, Valdivia', 'Recorrido por el mercado, cervecerías y productos locales.', 20000, 15, '2026-11-25 00:00:00', 8, 3, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (14, 'Arriendo Pack Camping, Puerto Montt', 'Carpa, saco y aislante para una noche en Cochamó.', 15000, 15, '2026-11-30 00:00:00', 3, 3, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (15, 'Arriendo de bicicletas, Temuco', 'Bicicleta de montaña con casco por el día para rutas urbanas y rurales.', 12000, 15, '2026-11-19 00:00:00', 3, 3, 1, 'programada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (16, 'Trekking Cerro Mariposas, Talca', 'Ascenso al cerro con vista a la ciudad y al valle del Maule.', 18000, 12, '2026-11-06 21:00:00', 1, 2, 1, 'finalizada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (17, 'Kayak Río Maule, Talca', 'Remada por el río entre humedales y bosque de ribera.', 24000, 10, '2026-11-11 21:00:00', 4, 3, 1, 'finalizada');
INSERT INTO `experiencias_experiencia` (`id`, `titulo`, `descripcion`, `precio`, `cupo_maximo`, `fecha_hora`, `categoria_id`, `creador_id`, `activa`, `estado`) VALUES (18, 'Canopy Bosque Valdiviano, Valdivia', 'Circuito de 10 tirolesas entre árboles nativos con instructores certificados.', 34000, 8, '2026-11-15 17:00:00', 2, 2, 1, 'en_curso');

INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (1, 4, 16, 2, 2, 5, '2026-11-15 21:50:30', 'confirmado');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (2, 5, 16, 1, 1, 4, '2026-11-15 21:50:30', 'confirmado');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (3, 5, 17, 1, 1, 4, '2026-11-15 21:50:30', 'confirmado');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (4, 4, 18, 3, 0, NULL, '2026-11-15 21:50:30', 'confirmado');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (5, 4, 1, 1, 0, NULL, '2026-11-15 21:50:30', 'confirmado');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (6, 4, 4, 2, 0, NULL, '2026-11-15 21:50:30', 'pendiente');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (7, 4, 8, 3, 0, NULL, '2026-11-15 21:50:30', 'confirmado');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (8, 4, 11, 1, 0, NULL, '2026-11-15 21:50:30', 'pendiente');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (9, 5, 2, 1, 0, NULL, '2026-11-15 21:50:30', 'confirmado');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (10, 5, 9, 2, 0, NULL, '2026-11-15 21:50:30', 'pendiente');
INSERT INTO `experiencias_inscripcion` (`id`, `usuario_id`, `experiencia_id`, `cantidad`, `asistentes`, `puntaje`, `fecha_inscripcion`, `estado_pago`) VALUES (11, 5, 6, 3, 0, NULL, '2026-11-15 21:50:30', 'confirmado');

SET FOREIGN_KEY_CHECKS=1;
