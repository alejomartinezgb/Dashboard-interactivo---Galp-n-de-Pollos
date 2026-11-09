-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-10-2026 a las 18:16:31
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `galpon_avicola`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignacion`
--

CREATE TABLE `asignacion` (
  `id_asignacion` int(11) NOT NULL,
  `id_trabajador` int(11) DEFAULT NULL,
  `id_tarea` int(11) DEFAULT NULL,
  `horas_asignadas` decimal(5,2) DEFAULT NULL,
  `rol` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `asignacion`
--

INSERT INTO `asignacion` (`id_asignacion`, `id_trabajador`, `id_tarea`, `horas_asignadas`, `rol`) VALUES
(1, 3, 1, 8.00, 'Operario de campo 1'),
(2, 4, 2, 4.00, 'Operario de campo 2'),
(3, 5, 3, 6.00, 'Mantenimiento'),
(4, 3, 4, 8.00, 'Operario de campo 1'),
(5, 4, 5, 5.00, 'Operario de campo 2'),
(6, 3, 6, 8.00, 'Operario de campo 1'),
(7, 4, 7, 5.00, 'Operario de campo 2'),
(8, 5, 8, 10.00, 'Mantenimiento'),
(9, 3, 9, 8.00, 'Operario de campo 1'),
(10, 3, 10, 8.00, 'Operario de campo 1'),
(11, 1, 1, 2.00, 'Administrador'),
(12, 2, 4, 8.00, 'Ventas y gasolina logistica'),
(13, 2, 9, 8.00, 'Ventas y gasolina logistica');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria_tarea`
--

CREATE TABLE `categoria_tarea` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `categoria_tarea`
--

INSERT INTO `categoria_tarea` (`id_categoria`, `nombre`, `descripcion`) VALUES
(1, 'Alimentación', 'Suministro diario de alimento y agua'),
(2, 'Sanidad', 'Vacunación y control sanitario'),
(3, 'Limpieza', 'Lavado y desinfección de galpón');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo_cliente` varchar(50) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `nombre`, `tipo_cliente`, `telefono`, `direccion`) VALUES
(1, 'Comercializadora de Pollo Fresco', 'Mayorista', '3109998877', 'Plaza de Mercado Local 4'),
(2, 'Asados y Carbón S.A.S.', 'Restaurante', '3128887766', 'Av. Central # 8-50'),
(3, 'Frigorífico del Norte', 'Industrial', '3147776655', 'Km 4 Vía al Mar'),
(4, 'Supermercados El Ahorro', 'Supermercado', '3165554433', 'Calle 50 # 15-20');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `compra`
--

CREATE TABLE `compra` (
  `id_compra` int(11) NOT NULL,
  `id_proveedor` int(11) DEFAULT NULL,
  `id_insumo` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `cantidad_comprada` decimal(10,2) DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `compra`
--

INSERT INTO `compra` (`id_compra`, `id_proveedor`, `id_insumo`, `fecha`, `cantidad_comprada`, `precio_unitario`) VALUES
(1, 1, 1, '2024-03-01', 55.00, 3000.00),
(2, 2, 2, '2024-03-02', 2.00, 75000.00),
(3, 1, 1, '2024-05-01', 60.00, 3000.00),
(4, 1, 1, '2024-07-01', 50.00, 3100.00),
(5, 1, 1, '2024-09-01', 65.00, 3100.00),
(6, 1, 1, '2024-11-01', 58.00, 3200.00),
(7, 1, 1, '2025-01-05', 60.00, 3200.00),
(8, 2, 2, '2025-01-06', 2.00, 78000.00),
(9, 1, 1, '2025-03-01', 50.00, 3200.00),
(10, 1, 1, '2025-05-10', 50.00, 3300.00),
(11, 1, 1, '2025-07-01', 70.00, 3300.00),
(12, 1, 1, '2025-09-01', 45.00, 3400.00),
(13, 1, 1, '2025-11-05', 65.00, 3400.00),
(14, 1, 1, '2026-01-10', 60.00, 3500.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id_detalle` int(11) NOT NULL,
  `id_venta` int(11) DEFAULT NULL,
  `id_lote` int(11) DEFAULT NULL,
  `cantidad_aves` int(11) DEFAULT NULL,
  `peso_total_kg` decimal(10,2) DEFAULT NULL,
  `precio_kg` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `detalle_venta`
--

INSERT INTO `detalle_venta` (`id_detalle`, `id_venta`, `id_lote`, `cantidad_aves`, `peso_total_kg`, `precio_kg`) VALUES
(1, 1, 1, 53, 132.50, 10800.00),
(2, 2, 2, 58, 144.00, 10400.00),
(3, 3, 3, 48, 120.00, 10500.00),
(4, 4, 4, 63, 157.50, 10700.00),
(5, 5, 5, 56, 140.00, 10150.00),
(6, 6, 6, 58, 145.00, 11000.00),
(7, 7, 7, 48, 120.00, 11200.00),
(8, 8, 8, 48, 120.00, 11300.00),
(9, 9, 9, 68, 171.48, 11500.00),
(10, 10, 10, 44, 109.00, 11500.00),
(11, 11, 12, 58, 145.00, 12200.00),
(12, 12, 11, 63, 157.50, 12000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `distribucion_gasto`
--

CREATE TABLE `distribucion_gasto` (
  `id_distribucion` int(11) NOT NULL,
  `id_gasto` int(11) DEFAULT NULL,
  `id_lote` int(11) DEFAULT NULL,
  `monto_asignado` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `distribucion_gasto`
--

INSERT INTO `distribucion_gasto` (`id_distribucion`, `id_gasto`, `id_lote`, `monto_asignado`) VALUES
(1, 1, 1, 170000.00),
(2, 2, 2, 180000.00),
(3, 3, 3, 185000.00),
(4, 4, 4, 190000.00),
(5, 5, 5, 195000.00),
(6, 6, 6, 210000.00),
(7, 7, 7, 90000.00),
(8, 8, 8, 190000.00),
(9, 9, 9, 195000.00),
(10, 10, 10, 220000.00),
(11, 11, 11, 180000.00),
(12, 12, 12, 210000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gasto_general`
--

CREATE TABLE `gasto_general` (
  `id_gasto` int(11) NOT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `monto` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `gasto_general`
--

INSERT INTO `gasto_general` (`id_gasto`, `tipo`, `descripcion`, `fecha`, `monto`) VALUES
(1, 'Operativo', 'Servicios y Gasolina Lote 1 (2024)', '2024-04-20', 170000.00),
(2, 'Operativo', 'Servicios y Gasolina Lote 2 (2024)', '2024-06-25', 180000.00),
(3, 'Operativo', 'Servicios y Gasolina Lote 3 (2024)', '2024-08-30', 185000.00),
(4, 'Operativo', 'Servicios y Gasolina Lote 4 (2024)', '2024-10-25', 190000.00),
(5, 'Operativo', 'Servicios y Gasolina Lote 5 (2024)', '2024-12-20', 195000.00),
(6, 'Operativo', 'Servicios y Gasolina Lote 6 (2025)', '2025-02-28', 210000.00),
(7, 'Mantenimiento', 'Reparación bebederos 2025', '2025-04-15', 90000.00),
(8, 'Operativo', 'Servicios y Gasolina Lote 7 (2025)', '2025-06-20', 190000.00),
(9, 'Operativo', 'Servicios y Gasolina Lote 8 (2025)', '2025-08-30', 195000.00),
(10, 'Operativo', 'Servicios y Gasolina Lote 9 (2025)', '2025-10-15', 220000.00),
(11, 'Operativo', 'Servicios y Gasolina Lote 10 (2025)', '2025-12-10', 180000.00),
(12, 'Operativo', 'Servicios y Gasolina Lote 11 (2026)', '2026-02-15', 210000.00),
(13, 'Operativo', 'Servicios y Gasolina Lote 12 (2026)', '2026-04-20', 205000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `insumo`
--

CREATE TABLE `insumo` (
  `id_insumo` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `categoria` varchar(50) DEFAULT NULL,
  `unidad_medida` varchar(20) DEFAULT NULL,
  `stock_actual` decimal(10,2) DEFAULT NULL,
  `stock_minimo` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `insumo`
--

INSERT INTO `insumo` (`id_insumo`, `nombre`, `categoria`, `unidad_medida`, `stock_actual`, `stock_minimo`) VALUES
(1, 'Pollito de 1 Día', 'Ave Viva', 'Unidad', 70.00, 10.00),
(2, 'Alimento Iniciación', 'Alimento', 'Bulto 40kg', 150.00, 20.00),
(3, 'Alimento Engorde', 'Alimento', 'Bulto 40kg', 400.00, 50.00),
(4, 'Vacuna Newcasttle', 'Sanidad', 'Dosis', 600.00, 100.00),
(5, 'Desinfectante Amonio', 'Limpieza', 'Galón', 80.00, 15.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lote`
--

CREATE TABLE `lote` (
  `id_lote` int(11) NOT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `cantidad_inicial` int(11) DEFAULT NULL,
  `raza` varchar(50) DEFAULT NULL,
  `ubicacion_galpon` varchar(50) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `lote`
--

INSERT INTO `lote` (`id_lote`, `fecha_ingreso`, `cantidad_inicial`, `raza`, `ubicacion_galpon`, `estado`) VALUES
(1, '2024-03-01', 55, 'Gallina Criolla Pura', 'Galpón 1 - Pollitos', 'Finalizado'),
(2, '2024-05-01', 60, 'Gallina Amarilla Isa Brown', 'Galpón 2 - Producción', 'Finalizado'),
(3, '2024-07-01', 50, 'Gallina Blanca Lohmann', 'Galpón 3 - Venta', 'Finalizado'),
(4, '2024-09-01', 65, 'Gallina Amarilla Isa Brown', 'Galpón 1 - Pollitos', 'Finalizado'),
(5, '2024-11-01', 58, 'Gallina Criolla Pura', 'Galpón 2 - Producción', 'Finalizado'),
(6, '2025-01-05', 60, 'Gallina Blanca Lohmann', 'Galpón 3 - Venta', 'Finalizado'),
(7, '2025-03-01', 50, 'Gallina Amarilla Isa Brown', 'Galpón 1 - Pollitos', 'Finalizado'),
(8, '2025-05-10', 50, 'Gallina Criolla Pura', 'Galpón 2 - Producción', 'Finalizado'),
(9, '2025-07-01', 70, 'Gallina Blanca Lohmann', 'Galpón 3 - Venta', 'Finalizado'),
(10, '2025-09-01', 45, 'Gallina Amarilla Isa Brown', 'Galpón 1 - Pollitos', 'Finalizado'),
(11, '2025-11-05', 65, 'Gallina Criolla Pura', 'Galpón 2 - Producción', 'Finalizado'),
(12, '2026-01-10', 60, 'Gallina Blanca Lohmann', 'Galpón 3 - Venta', 'Finalizado'),
(13, '2026-06-01', 55, 'Gallina Amarilla Isa Brown', 'Galpón 1 - Pollitos', 'En Proceso'),
(14, '2026-06-15', 60, 'Gallina Criolla Pura', 'Galpón 2 - Producción', 'En Proceso'),
(15, '2026-07-01', 50, 'Gallina Blanca Lohmann', 'Galpón 3 - Venta', 'En Proceso');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `lote_tarea`
--

CREATE TABLE `lote_tarea` (
  `id_lote_tarea` int(11) NOT NULL,
  `id_lote` int(11) DEFAULT NULL,
  `id_tarea` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `lote_tarea`
--

INSERT INTO `lote_tarea` (`id_lote_tarea`, `id_lote`, `id_tarea`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 5, 3),
(4, 6, 4),
(5, 7, 5),
(6, 9, 6),
(7, 11, 7),
(8, 12, 8),
(9, 12, 9),
(10, 13, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `monitoreo_ambiental`
--

CREATE TABLE `monitoreo_ambiental` (
  `id_monitoreo_amb` int(11) NOT NULL,
  `id_lote` int(11) DEFAULT NULL,
  `fecha_hora` datetime DEFAULT NULL,
  `temperatura` decimal(5,2) DEFAULT NULL,
  `humedad` decimal(5,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `monitoreo_ambiental`
--

INSERT INTO `monitoreo_ambiental` (`id_monitoreo_amb`, `id_lote`, `fecha_hora`, `temperatura`, `humedad`) VALUES
(1, 1, '2024-03-10 08:00:00', 28.00, 65.00),
(2, 3, '2024-07-05 08:00:00', 29.50, 68.00),
(3, 6, '2025-01-10 08:00:00', 28.50, 65.00),
(4, 9, '2025-07-05 08:00:00', 30.50, 70.00),
(5, 12, '2026-01-15 08:00:00', 29.20, 67.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mortalidad`
--

CREATE TABLE `mortalidad` (
  `id_mortalidad` int(11) NOT NULL,
  `id_lote` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `causa` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `mortalidad`
--

INSERT INTO `mortalidad` (`id_mortalidad`, `id_lote`, `fecha`, `cantidad`, `causa`) VALUES
(1, 1, '2024-03-20', 2, 'Natural'),
(2, 2, '2024-05-20', 2, 'Natural'),
(3, 3, '2024-07-20', 2, 'Natural'),
(4, 4, '2024-09-20', 2, 'Natural'),
(5, 5, '2024-11-20', 2, 'Natural'),
(6, 6, '2025-01-20', 2, 'Natural'),
(7, 7, '2025-03-15', 2, 'Natural'),
(8, 8, '2025-05-25', 2, 'Natural'),
(9, 9, '2025-07-15', 2, 'Natural'),
(10, 10, '2025-09-20', 1, 'Natural'),
(11, 11, '2025-11-20', 2, 'Natural'),
(12, 12, '2026-01-25', 2, 'Natural');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `precio_mercado`
--

CREATE TABLE `precio_mercado` (
  `id_precio` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `precio_referencia_kg` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `precio_mercado`
--

INSERT INTO `precio_mercado` (`id_precio`, `fecha`, `precio_referencia_kg`) VALUES
(1, '2024-04-15', 10200.00),
(2, '2024-06-15', 10400.00),
(3, '2024-08-15', 10500.00),
(4, '2024-10-15', 10700.00),
(5, '2024-12-15', 10900.00),
(6, '2025-03-01', 11000.00),
(7, '2025-04-25', 11200.00),
(8, '2025-07-01', 11300.00),
(9, '2025-08-25', 11500.00),
(10, '2025-10-25', 11800.00),
(11, '2026-01-01', 12000.00),
(12, '2026-03-05', 12200.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `id_proveedor` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo_suministro` varchar(50) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`id_proveedor`, `nombre`, `tipo_suministro`, `telefono`, `direccion`, `email`) VALUES
(1, 'Incubadora y Pollo Colombiano S.A.', 'Pollitos de 1 día', '3112223344', 'Km 2 Vía Medellín', 'ventas@incubadora.com'),
(2, 'Nutrición Avícola Andina', 'Alimento concentrado', '3154445566', 'Calle 10 # 20-30', 'pedidos@nutricionandina.com'),
(3, 'Sanidad Veterinaria del Llano', 'Medicinas y Vacunas', '3187776655', 'Carrera 15 # 45-12', 'contacto@sanidadllano.com'),
(4, 'Estación de Servicio Terpel Local', 'Combustible y Logística', '3101234567', 'Av. Principal # 5-20', 'facturacion@terpel.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `seguimiento_peso`
--

CREATE TABLE `seguimiento_peso` (
  `id_seguimiento` int(11) NOT NULL,
  `id_lote` int(11) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `peso_promedio` decimal(5,2) DEFAULT NULL,
  `cantidad_viva` int(11) DEFAULT NULL,
  `alimento_consumido` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `seguimiento_peso`
--

INSERT INTO `seguimiento_peso` (`id_seguimiento`, `id_lote`, `fecha`, `peso_promedio`, `cantidad_viva`, `alimento_consumido`) VALUES
(1, 1, '2024-04-15', 2.45, 53, 180.00),
(2, 2, '2024-06-15', 2.50, 58, 195.00),
(3, 3, '2024-08-15', 2.48, 48, 160.00),
(4, 4, '2024-10-15', 2.52, 63, 210.00),
(5, 5, '2024-12-15', 2.40, 56, 185.00),
(6, 6, '2025-02-25', 2.50, 58, 200.00),
(7, 7, '2025-04-20', 2.45, 48, 160.00),
(8, 8, '2025-07-01', 2.52, 48, 170.00),
(9, 9, '2025-08-15', 2.55, 68, 240.00),
(10, 10, '2025-10-15', 2.40, 44, 150.00),
(11, 11, '2025-12-15', 2.48, 63, 215.00),
(12, 12, '2026-03-05', 2.52, 58, 200.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarea`
--

CREATE TABLE `tarea` (
  `id_tarea` int(11) NOT NULL,
  `id_categoria` int(11) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `tarea`
--

INSERT INTO `tarea` (`id_tarea`, `id_categoria`, `descripcion`, `fecha`, `estado`) VALUES
(1, 1, 'Alimentación Lote 1 (2024)', '2024-03-05', 'Completada'),
(2, 2, 'Sanidad Lote 2 (2024)', '2024-05-05', 'Completada'),
(3, 3, 'Limpieza Galpón 2024', '2024-12-15', 'Completada'),
(4, 1, 'Alimentación Lote 6 (2025)', '2025-01-10', 'Completada'),
(5, 2, 'Vacunación Lote 7', '2025-03-05', 'Completada'),
(6, 1, 'Alimentación Lote 9', '2025-07-05', 'Completada'),
(7, 2, 'Control sanitario Lote 11', '2025-11-10', 'Completada'),
(8, 3, 'Limpieza general galpones 2026', '2026-01-05', 'Completada'),
(9, 1, 'Alimentación Lote 12', '2026-01-15', 'Completada'),
(10, 1, 'Alimentación Lote 13 (En proceso)', '2026-06-05', 'Completada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajador`
--

CREATE TABLE `trabajador` (
  `id_trabajador` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `cargo` varchar(50) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `fecha_contratacion` date DEFAULT NULL,
  `salario` decimal(10,2) DEFAULT NULL,
  `tarifa_hora` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `trabajador`
--

INSERT INTO `trabajador` (`id_trabajador`, `nombre`, `cargo`, `telefono`, `fecha_contratacion`, `salario`, `tarifa_hora`) VALUES
(1, 'Carlos Pérez', 'Administrador', '3201112233', '2024-01-01', 1600000.00, 9000.00),
(2, 'Ana Gómez', 'Operaria de Ventas y Gasolina/Logística', '3202223344', '2024-01-01', 1350000.00, 7800.00),
(3, 'Luis Torres', 'Operario de Campo 1', '3203334455', '2024-01-01', 1300000.00, 7500.00),
(4, 'Juan Morales', 'Operario de Campo 2', '3204445566', '2024-01-01', 1300000.00, 7500.00),
(5, 'Pedro Cárdenas', 'Operario de Mantenimiento', '3205556677', '2024-01-01', 1300000.00, 7500.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `uso_insumo`
--

CREATE TABLE `uso_insumo` (
  `id_uso` int(11) NOT NULL,
  `id_tarea` int(11) DEFAULT NULL,
  `id_insumo` int(11) DEFAULT NULL,
  `cantidad_usada` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `uso_insumo`
--

INSERT INTO `uso_insumo` (`id_uso`, `id_tarea`, `id_insumo`, `cantidad_usada`) VALUES
(1, 1, 1, 55.00),
(2, 2, 2, 2.00),
(3, 3, 5, 1.00),
(4, 4, 1, 60.00),
(5, 5, 4, 2.00),
(6, 6, 3, 3.00),
(7, 7, 4, 2.00),
(8, 8, 5, 1.00),
(9, 9, 2, 2.00),
(10, 10, 3, 2.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `id_venta` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `metodo_pago` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `venta`
--

INSERT INTO `venta` (`id_venta`, `fecha`, `id_cliente`, `total`, `metodo_pago`) VALUES
(1, '2024-04-20', 1, 1428000.00, 'Transferencia'),
(2, '2024-06-25', 2, 1497600.00, 'Transferencia'),
(3, '2024-08-30', 1, 1260000.00, 'Transferencia'),
(4, '2024-10-25', 3, 1690500.00, 'Transferencia'),
(5, '2024-12-20', 4, 1421200.00, 'Transferencia'),
(6, '2025-02-28', 1, 1595000.00, 'Transferencia'),
(7, '2025-04-25', 2, 1344000.00, 'Transferencia'),
(8, '2025-07-01', 1, 1356000.00, 'Transferencia'),
(9, '2025-08-25', 3, 1972000.00, 'Transferencia'),
(10, '2025-10-25', 4, 1254000.00, 'Transferencia'),
(11, '2026-01-01', 1, 1890000.00, 'Transferencia'),
(12, '2026-03-05', 2, 1769000.00, 'Transferencia');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asignacion`
--
ALTER TABLE `asignacion`
  ADD PRIMARY KEY (`id_asignacion`),
  ADD KEY `id_trabajador` (`id_trabajador`),
  ADD KEY `id_tarea` (`id_tarea`);

--
-- Indices de la tabla `categoria_tarea`
--
ALTER TABLE `categoria_tarea`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `compra`
--
ALTER TABLE `compra`
  ADD PRIMARY KEY (`id_compra`),
  ADD KEY `id_proveedor` (`id_proveedor`),
  ADD KEY `id_insumo` (`id_insumo`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_venta` (`id_venta`),
  ADD KEY `id_lote` (`id_lote`);

--
-- Indices de la tabla `distribucion_gasto`
--
ALTER TABLE `distribucion_gasto`
  ADD PRIMARY KEY (`id_distribucion`),
  ADD KEY `id_gasto` (`id_gasto`),
  ADD KEY `id_lote` (`id_lote`);

--
-- Indices de la tabla `gasto_general`
--
ALTER TABLE `gasto_general`
  ADD PRIMARY KEY (`id_gasto`);

--
-- Indices de la tabla `insumo`
--
ALTER TABLE `insumo`
  ADD PRIMARY KEY (`id_insumo`);

--
-- Indices de la tabla `lote`
--
ALTER TABLE `lote`
  ADD PRIMARY KEY (`id_lote`);

--
-- Indices de la tabla `lote_tarea`
--
ALTER TABLE `lote_tarea`
  ADD PRIMARY KEY (`id_lote_tarea`),
  ADD KEY `id_lote` (`id_lote`),
  ADD KEY `id_tarea` (`id_tarea`);

--
-- Indices de la tabla `monitoreo_ambiental`
--
ALTER TABLE `monitoreo_ambiental`
  ADD PRIMARY KEY (`id_monitoreo_amb`),
  ADD KEY `id_lote` (`id_lote`);

--
-- Indices de la tabla `mortalidad`
--
ALTER TABLE `mortalidad`
  ADD PRIMARY KEY (`id_mortalidad`),
  ADD KEY `id_lote` (`id_lote`);

--
-- Indices de la tabla `precio_mercado`
--
ALTER TABLE `precio_mercado`
  ADD PRIMARY KEY (`id_precio`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `seguimiento_peso`
--
ALTER TABLE `seguimiento_peso`
  ADD PRIMARY KEY (`id_seguimiento`),
  ADD KEY `id_lote` (`id_lote`);

--
-- Indices de la tabla `tarea`
--
ALTER TABLE `tarea`
  ADD PRIMARY KEY (`id_tarea`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Indices de la tabla `trabajador`
--
ALTER TABLE `trabajador`
  ADD PRIMARY KEY (`id_trabajador`);

--
-- Indices de la tabla `uso_insumo`
--
ALTER TABLE `uso_insumo`
  ADD PRIMARY KEY (`id_uso`),
  ADD KEY `id_tarea` (`id_tarea`),
  ADD KEY `id_insumo` (`id_insumo`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asignacion`
--
ALTER TABLE `asignacion`
  MODIFY `id_asignacion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `categoria_tarea`
--
ALTER TABLE `categoria_tarea`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `compra`
--
ALTER TABLE `compra`
  MODIFY `id_compra` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `distribucion_gasto`
--
ALTER TABLE `distribucion_gasto`
  MODIFY `id_distribucion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `gasto_general`
--
ALTER TABLE `gasto_general`
  MODIFY `id_gasto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `insumo`
--
ALTER TABLE `insumo`
  MODIFY `id_insumo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `lote`
--
ALTER TABLE `lote`
  MODIFY `id_lote` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `lote_tarea`
--
ALTER TABLE `lote_tarea`
  MODIFY `id_lote_tarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `monitoreo_ambiental`
--
ALTER TABLE `monitoreo_ambiental`
  MODIFY `id_monitoreo_amb` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `mortalidad`
--
ALTER TABLE `mortalidad`
  MODIFY `id_mortalidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `precio_mercado`
--
ALTER TABLE `precio_mercado`
  MODIFY `id_precio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `seguimiento_peso`
--
ALTER TABLE `seguimiento_peso`
  MODIFY `id_seguimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `tarea`
--
ALTER TABLE `tarea`
  MODIFY `id_tarea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `trabajador`
--
ALTER TABLE `trabajador`
  MODIFY `id_trabajador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `uso_insumo`
--
ALTER TABLE `uso_insumo`
  MODIFY `id_uso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asignacion`
--
ALTER TABLE `asignacion`
  ADD CONSTRAINT `asignacion_ibfk_1` FOREIGN KEY (`id_trabajador`) REFERENCES `trabajador` (`id_trabajador`),
  ADD CONSTRAINT `asignacion_ibfk_2` FOREIGN KEY (`id_tarea`) REFERENCES `tarea` (`id_tarea`);

--
-- Filtros para la tabla `compra`
--
ALTER TABLE `compra`
  ADD CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedor` (`id_proveedor`),
  ADD CONSTRAINT `compra_ibfk_2` FOREIGN KEY (`id_insumo`) REFERENCES `insumo` (`id_insumo`);

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id_venta`),
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`);

--
-- Filtros para la tabla `distribucion_gasto`
--
ALTER TABLE `distribucion_gasto`
  ADD CONSTRAINT `distribucion_gasto_ibfk_1` FOREIGN KEY (`id_gasto`) REFERENCES `gasto_general` (`id_gasto`),
  ADD CONSTRAINT `distribucion_gasto_ibfk_2` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`);

--
-- Filtros para la tabla `lote_tarea`
--
ALTER TABLE `lote_tarea`
  ADD CONSTRAINT `lote_tarea_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`),
  ADD CONSTRAINT `lote_tarea_ibfk_2` FOREIGN KEY (`id_tarea`) REFERENCES `tarea` (`id_tarea`);

--
-- Filtros para la tabla `monitoreo_ambiental`
--
ALTER TABLE `monitoreo_ambiental`
  ADD CONSTRAINT `monitoreo_ambiental_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`);

--
-- Filtros para la tabla `mortalidad`
--
ALTER TABLE `mortalidad`
  ADD CONSTRAINT `mortalidad_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`);

--
-- Filtros para la tabla `seguimiento_peso`
--
ALTER TABLE `seguimiento_peso`
  ADD CONSTRAINT `seguimiento_peso_ibfk_1` FOREIGN KEY (`id_lote`) REFERENCES `lote` (`id_lote`);

--
-- Filtros para la tabla `tarea`
--
ALTER TABLE `tarea`
  ADD CONSTRAINT `tarea_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categoria_tarea` (`id_categoria`);

--
-- Filtros para la tabla `uso_insumo`
--
ALTER TABLE `uso_insumo`
  ADD CONSTRAINT `uso_insumo_ibfk_1` FOREIGN KEY (`id_tarea`) REFERENCES `tarea` (`id_tarea`),
  ADD CONSTRAINT `uso_insumo_ibfk_2` FOREIGN KEY (`id_insumo`) REFERENCES `insumo` (`id_insumo`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
