-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 20, 2026 at 05:01 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_rapor_anisa`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_absensi_anisa`
--

CREATE TABLE `tb_absensi_anisa` (
  `id_absensi` varchar(10) NOT NULL,
  `nis` varchar(15) NOT NULL,
  `tanggal` date NOT NULL,
  `sakit` int(11) NOT NULL,
  `izin` int(11) NOT NULL,
  `alfa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_absensi_anisa`
--

INSERT INTO `tb_absensi_anisa` (`id_absensi`, `nis`, `tanggal`, `sakit`, `izin`, `alfa`) VALUES
('ABS001', '10243207', '2026-01-01', 1, 2, 0),
('ABS002', '10243285', '2026-01-02', 3, 0, 2),
('ABS003', '10243287', '2026-01-03', 5, 2, 1),
('ABS004', '10243289', '2026-01-04', 1, 1, 1),
('ABS005', '10243290', '2026-01-05', 5, 2, 3);

-- --------------------------------------------------------

--
-- Table structure for table `tb_kelas_anisa`
--

CREATE TABLE `tb_kelas_anisa` (
  `id_kelas` varchar(10) NOT NULL,
  `nama_kelas` varchar(50) NOT NULL,
  `wali_kelas` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_kelas_anisa`
--

INSERT INTO `tb_kelas_anisa` (`id_kelas`, `nama_kelas`, `wali_kelas`) VALUES
('KLS001', 'XI MEKA D', 'anisa zahra'),
('KLS002', 'XI KIMIA C', 'arif kusuma'),
('KLS003', 'XI RPL A', 'naisya aurelia'),
('KLS004', 'XI RPL B', 'ratna sartika'),
('KLS005', 'XI ANIMASI A', 'aldo najar');

-- --------------------------------------------------------

--
-- Table structure for table `tb_mapel_anisa`
--

CREATE TABLE `tb_mapel_anisa` (
  `id_mapel` varchar(10) NOT NULL,
  `nama_mapel` varchar(50) NOT NULL,
  `kkm` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_mapel_anisa`
--

INSERT INTO `tb_mapel_anisa` (`id_mapel`, `nama_mapel`, `kkm`) VALUES
('MPL001', 'Matematika', 75),
('MPL002', 'B.Inggris', 70),
('MPL003', 'B.Jepang', 78),
('MPL004', 'Sejarah', 75),
('MPL005', 'B.Indonesia', 70);

-- --------------------------------------------------------

--
-- Table structure for table `tb_nilai_anisa`
--

CREATE TABLE `tb_nilai_anisa` (
  `id_nilai` varchar(10) NOT NULL,
  `nis` varchar(15) NOT NULL,
  `id_mapel` varchar(10) NOT NULL,
  `nilai_tugas` int(11) NOT NULL,
  `nilai_uts` int(11) NOT NULL,
  `nilai_uas` int(11) NOT NULL,
  `deskripsi` text NOT NULL,
  `semester` varchar(20) NOT NULL,
  `tahun_ajaran` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_nilai_anisa`
--

INSERT INTO `tb_nilai_anisa` (`id_nilai`, `nis`, `id_mapel`, `nilai_tugas`, `nilai_uts`, `nilai_uas`, `deskripsi`, `semester`, `tahun_ajaran`) VALUES
('NLI001', '10243207', 'MPL001', 90, 95, 80, 'ananda sangat baik dalam mempelajari tugas tugas nya', 'semestar 1', 2025),
('NLI002', '10243285', 'MPL002', 80, 90, 85, 'ananda sangat amat bagus dalam mempelajari bahasa nya', 'semester 1', 2025),
('NLI003', '10243287', 'MPL003', 90, 98, 97, 'ananda sangat baik dalam mencerna pelajaran nya', 'semester 1', 2025),
('NLI004', '10243289', 'MPL004', 90, 78, 89, 'ananda sangat baik dalam mempelajari nya', 'semester 1', 2025),
('NLI005', '10243290', 'MPL005', 90, 98, 96, 'ananda sangat baik dalam mempelajari segala hal', 'semester 1', 2025);

-- --------------------------------------------------------

--
-- Table structure for table `tb_siswa_anisa`
--

CREATE TABLE `tb_siswa_anisa` (
  `nis` varchar(15) NOT NULL,
  `nama_siswa` varchar(50) NOT NULL,
  `tempat_lahir` varchar(50) NOT NULL,
  `tgl_lahir` date NOT NULL,
  `alamat` text NOT NULL,
  `id_kelas` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_siswa_anisa`
--

INSERT INTO `tb_siswa_anisa` (`nis`, `nama_siswa`, `tempat_lahir`, `tgl_lahir`, `alamat`, `id_kelas`) VALUES
('10243207', 'Novi Ropiah', 'Bandung', '2016-01-28', 'JL.Suka Jadi No 70', 'KLS005'),
('10243285', 'ahkam lisanul mizan', 'Cimahi', '2016-01-04', 'JL.Mawar No 90', 'KLS001'),
('10243287', 'anisa jaya lestari', 'Cimahi', '2016-01-13', 'JL.Kamarung NO 70', 'KLS002'),
('10243289', 'anisa celia febriana', 'Cimahi', '2016-01-05', 'KP.Nyalindung No 56', 'KLS003'),
('10243290', 'exchel dwi', 'Bandung', '2016-01-03', 'JL.Anggrek No 89', 'KLS004');

-- --------------------------------------------------------

--
-- Table structure for table `tb_user_anisa`
--

CREATE TABLE `tb_user_anisa` (
  `id_user` varchar(10) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `role` enum('admin','guru','walikelas') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_user_anisa`
--

INSERT INTO `tb_user_anisa` (`id_user`, `username`, `password`, `role`) VALUES
('USR001', 'admin sekola', 'admin123', 'admin'),
('USR002', 'farhan junaedi', 'farhan123', 'guru'),
('USR003', 'siti aminah', 'siti123', 'walikelas'),
('USR004', 'cantika kirana', 'cantika', 'walikelas'),
('USR005', 'andika krisna', 'andika123', 'walikelas');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_absensi_anisa`
--
ALTER TABLE `tb_absensi_anisa`
  ADD PRIMARY KEY (`id_absensi`),
  ADD KEY `nis` (`nis`);

--
-- Indexes for table `tb_kelas_anisa`
--
ALTER TABLE `tb_kelas_anisa`
  ADD PRIMARY KEY (`id_kelas`);

--
-- Indexes for table `tb_mapel_anisa`
--
ALTER TABLE `tb_mapel_anisa`
  ADD PRIMARY KEY (`id_mapel`);

--
-- Indexes for table `tb_nilai_anisa`
--
ALTER TABLE `tb_nilai_anisa`
  ADD PRIMARY KEY (`id_nilai`),
  ADD KEY `nis` (`nis`,`id_mapel`),
  ADD KEY `id_mapel` (`id_mapel`);

--
-- Indexes for table `tb_siswa_anisa`
--
ALTER TABLE `tb_siswa_anisa`
  ADD PRIMARY KEY (`nis`),
  ADD KEY `id_kelas` (`id_kelas`);

--
-- Indexes for table `tb_user_anisa`
--
ALTER TABLE `tb_user_anisa`
  ADD PRIMARY KEY (`id_user`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_absensi_anisa`
--
ALTER TABLE `tb_absensi_anisa`
  ADD CONSTRAINT `tb_absensi_anisa_ibfk_1` FOREIGN KEY (`nis`) REFERENCES `tb_siswa_anisa` (`nis`);

--
-- Constraints for table `tb_nilai_anisa`
--
ALTER TABLE `tb_nilai_anisa`
  ADD CONSTRAINT `tb_nilai_anisa_ibfk_1` FOREIGN KEY (`id_mapel`) REFERENCES `tb_mapel_anisa` (`id_mapel`),
  ADD CONSTRAINT `tb_nilai_anisa_ibfk_2` FOREIGN KEY (`nis`) REFERENCES `tb_siswa_anisa` (`nis`);

--
-- Constraints for table `tb_siswa_anisa`
--
ALTER TABLE `tb_siswa_anisa`
  ADD CONSTRAINT `tb_siswa_anisa_ibfk_1` FOREIGN KEY (`id_kelas`) REFERENCES `tb_kelas_anisa` (`id_kelas`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
