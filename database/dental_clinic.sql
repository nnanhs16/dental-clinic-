-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 26, 2026 at 10:27 PM
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
-- Database: `dental_clinic`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` bigint(20) NOT NULL,
  `service_name` varchar(150) NOT NULL,
  `appointment_datetime` datetime(6) NOT NULL,
  `reason` longtext NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `doctor_id` bigint(20) NOT NULL,
  `patient_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `service_name`, `appointment_datetime`, `reason`, `status`, `created_at`, `updated_at`, `doctor_id`, `patient_id`) VALUES
(1, 'Khám răng tổng quát', '2026-12-22 03:00:00.000000', 'Kiểm tra sức khỏe răng miệng', 'CANCELLED', '2026-11-24 15:40:34.100609', '2026-11-24 15:43:00.338900', 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add Tài khoản', 6, 'add_user'),
(22, 'Can change Tài khoản', 6, 'change_user'),
(23, 'Can delete Tài khoản', 6, 'delete_user'),
(24, 'Can view Tài khoản', 6, 'view_user'),
(25, 'Can add Bệnh nhân', 7, 'add_patient'),
(26, 'Can change Bệnh nhân', 7, 'change_patient'),
(27, 'Can delete Bệnh nhân', 7, 'delete_patient'),
(28, 'Can view Bệnh nhân', 7, 'view_patient'),
(29, 'Can add Lịch hẹn', 8, 'add_appointment'),
(30, 'Can change Lịch hẹn', 8, 'change_appointment'),
(31, 'Can delete Lịch hẹn', 8, 'delete_appointment'),
(32, 'Can view Lịch hẹn', 8, 'view_appointment'),
(33, 'Can add Dịch vụ', 9, 'add_service'),
(34, 'Can change Dịch vụ', 9, 'change_service'),
(35, 'Can delete Dịch vụ', 9, 'delete_service'),
(36, 'Can view Dịch vụ', 9, 'view_service'),
(37, 'Can add Hồ sơ khám bệnh', 10, 'add_medicalrecord'),
(38, 'Can change Hồ sơ khám bệnh', 10, 'change_medicalrecord'),
(39, 'Can delete Hồ sơ khám bệnh', 10, 'delete_medicalrecord'),
(40, 'Can view Hồ sơ khám bệnh', 10, 'view_medicalrecord'),
(41, 'Can add Đánh giá dịch vụ', 11, 'add_review'),
(42, 'Can change Đánh giá dịch vụ', 11, 'change_review'),
(43, 'Can delete Đánh giá dịch vụ', 11, 'delete_review'),
(44, 'Can view Đánh giá dịch vụ', 11, 'view_review');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2026-11-24 14:28:10.033761', '1', 'admin - Quản trị hệ thống', 2, '[{\"changed\": {\"fields\": [\"Vai tr\\u00f2\"]}}]', 6, 1),
(2, '2026-11-24 15:37:42.204707', '3', 'doctor01 - Bác sĩ', 1, '[{\"added\": {}}]', 6, 1),
(3, '2026-11-24 15:49:03.954593', '1', 'Khám răng tổng quát', 1, '[{\"added\": {}}]', 9, 1),
(4, '2026-11-24 15:49:34.725670', '2', 'Lấy cao răng', 1, '[{\"added\": {}}]', 9, 1),
(5, '2026-11-24 15:50:29.399619', '3', 'Tẩy trắng răng', 1, '[{\"added\": {}}]', 9, 1),
(6, '2026-11-24 16:02:07.539993', '1', 'Nguyen Van An Updated - 2026-11-24 10:00:00+00:00', 1, '[{\"added\": {}}]', 10, 1),
(7, '2026-11-24 16:42:59.154354', '2', 'patient01 - Bệnh nhân', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(8, '2026-11-24 16:43:28.221163', '2', 'patient01 - Bệnh nhân', 2, '[]', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(6, 'accounts', 'user'),
(1, 'admin', 'logentry'),
(8, 'appointments', 'appointment'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(10, 'medical_records', 'medicalrecord'),
(7, 'patients', 'patient'),
(11, 'reviews', 'review'),
(9, 'services', 'service'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-11-24 14:07:50.393352'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-11-24 14:07:50.443391'),
(3, 'auth', '0001_initial', '2026-11-24 14:07:50.639755'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-11-24 14:07:50.686791'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-11-24 14:07:50.690541'),
(6, 'auth', '0004_alter_user_username_opts', '2026-11-24 14:07:50.694574'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-11-24 14:07:50.698325'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-11-24 14:07:50.699825'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-11-24 14:07:50.704339'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-11-24 14:07:50.708838'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-11-24 14:07:50.713338'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-11-24 14:07:50.723095'),
(13, 'auth', '0011_update_proxy_permissions', '2026-11-24 14:07:50.730594'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-11-24 14:07:50.736847'),
(15, 'accounts', '0001_initial', '2026-11-24 14:07:51.102611'),
(16, 'admin', '0001_initial', '2026-11-24 14:07:51.226498'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-11-24 14:07:51.232528'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-11-24 14:07:51.237254'),
(19, 'sessions', '0001_initial', '2026-11-24 14:07:51.269367'),
(20, 'patients', '0001_initial', '2026-11-24 15:01:20.251709'),
(21, 'patients', '0002_alter_patient_id', '2026-11-24 15:06:37.394309'),
(22, 'appointments', '0001_initial', '2026-11-24 15:24:44.637572'),
(23, 'services', '0001_initial', '2026-11-24 15:45:35.630051'),
(24, 'medical_records', '0001_initial', '2026-11-24 15:53:12.819590'),
(25, 'reviews', '0001_initial', '2026-11-24 16:05:47.570354');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('ebuajewq0epv1dbwq6w8eu4s9hvztuxd', '.eJxVjDsOwjAQBe_iGlnxNzIlPWewdr1rHEC2FCdVxN1JpBTQvpl5m4iwLiWunec4kbgKJS6_G0J6cT0APaE-mkytLvOE8lDkSbu8N-L37XT_Dgr0steWKeTg0diUlMFg0YODbBUPlIwhv0NQQYOH7IDRjXqkwZugWAXSXny-_U04NA:1xVtbf:PXQ_R9NyPmc1r1OiE1rIdraVSo_cgBa9AVOAHdMqZKU', '2026-12-08 16:42:59.177433');

-- --------------------------------------------------------

--
-- Table structure for table `medical_records`
--

CREATE TABLE `medical_records` (
  `id` bigint(20) NOT NULL,
  `examination_date` datetime(6) NOT NULL,
  `service_name` varchar(150) NOT NULL,
  `diagnosis` longtext NOT NULL,
  `result` longtext NOT NULL,
  `treatment` longtext NOT NULL,
  `follow_up_date` date DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `appointment_id` bigint(20) DEFAULT NULL,
  `doctor_id` bigint(20) NOT NULL,
  `patient_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `medical_records`
--

INSERT INTO `medical_records` (`id`, `examination_date`, `service_name`, `diagnosis`, `result`, `treatment`, `follow_up_date`, `created_at`, `appointment_id`, `doctor_id`, `patient_id`) VALUES
(1, '2026-11-24 10:00:00.000000', 'Khám răng tổng quát', 'Răng có mảng bám', 'Chưa phát hiện vấn đề nghiêm trọng', 'Vệ sinh răng miệng định kỳ', '2027-01-24', '2026-11-24 16:02:07.538491', 1, 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `id` bigint(20) NOT NULL,
  `patient_code` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `gender` varchar(10) NOT NULL,
  `address` longtext NOT NULL,
  `occupation` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`id`, `patient_code`, `full_name`, `date_of_birth`, `gender`, `address`, `occupation`, `created_at`, `updated_at`, `user_id`) VALUES
(1, 'BN740A77EEAA', 'Nguyen Van An Updated', '2000-05-15', 'MALE', 'Cam Le, Da Nang', 'Nhan vien', '2026-11-24 15:12:01.466379', '2026-11-24 15:21:31.494815', 2);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` bigint(20) NOT NULL,
  `rating` smallint(5) UNSIGNED NOT NULL CHECK (`rating` >= 0),
  `comment` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `patient_id` bigint(20) NOT NULL,
  `service_id` bigint(20) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` bigint(20) NOT NULL,
  `name` varchar(150) NOT NULL,
  `category` varchar(30) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(12,0) NOT NULL,
  `duration` int(10) UNSIGNED NOT NULL CHECK (`duration` >= 0),
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `name`, `category`, `description`, `price`, `duration`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Khám răng tổng quát', 'GENERAL', 'Kiểm tra tổng quát tình trạng răng và nướu.', 100000, 30, 1, '2026-11-24 15:49:03.952817', '2026-11-24 15:49:03.952817'),
(2, 'Lấy cao răng', 'CLEANING', 'Làm sạch mảng bám và cao răng.', 200000, 30, 1, '2026-11-24 15:49:34.724935', '2026-11-24 15:49:34.724935'),
(3, 'Tẩy trắng răng', 'COSMETIC', 'Dịch vụ cải thiện màu sắc răng.', 1500000, 60, 1, '2026-11-24 15:50:29.398867', '2026-11-24 15:50:29.398867');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(30) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `phone_number`, `created_at`, `updated_at`) VALUES
(1, 'pbkdf2_sha256$720000$qmgpz9hf7JdtAfVdGqpobg$hx04jtfZ+pOdgRaTSjaqCN46ly2n02Jee6pnrsnhmvE=', '2026-11-24 14:09:59.000000', 1, 'admin', '', '', 'nnanhs22@gmail.com', 1, 1, '2026-11-24 14:08:53.000000', 'SYSTEM_ADMIN', NULL, '2026-11-24 14:08:53.939046', '2026-11-24 14:28:10.028542'),
(2, 'pbkdf2_sha256$720000$SdAnFotIdApVuRi66Xhwwm$Zq+Y6xWtokRNlCm9/vZA30TVqFf9Ik/kTCKWnr7S7hQ=', NULL, 0, 'patient01', '', '', 'patient01@gmail.com', 0, 1, '2026-11-24 15:12:01.000000', 'PATIENT', '0912345678', '2026-11-24 15:12:01.451952', '2026-11-24 16:43:28.218164'),
(3, 'pbkdf2_sha256$720000$ptfg49GxTLe5uko3CI1MaR$7Eb4iORZO5Hncu/+wV13N/94EtmmZ53yUp2/+2y9mCI=', NULL, 0, 'doctor01', 'B', 'Nguyễn Văn', 'nnanhs21@gmail.com', 0, 1, '2026-11-24 15:37:41.776788', 'DOCTOR', '0123456789', '2026-11-24 15:37:42.202431', '2026-11-24 15:37:42.202431');

-- --------------------------------------------------------

--
-- Table structure for table `users_groups`
--

CREATE TABLE `users_groups` (
  `id` int(11) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users_user_permissions`
--

CREATE TABLE `users_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `appointments_doctor_id_96635781_fk_users_id` (`doctor_id`),
  ADD KEY `appointments_patient_id_b2db55d3_fk_patients_id` (`patient_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `medical_records`
--
ALTER TABLE `medical_records`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `appointment_id` (`appointment_id`),
  ADD KEY `medical_records_doctor_id_eac1d872_fk_users_id` (`doctor_id`),
  ADD KEY `medical_records_patient_id_a9bed619_fk_patients_id` (`patient_id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `patient_code` (`patient_code`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_patient_service_review` (`patient_id`,`service_id`),
  ADD KEY `reviews_service_id_00992c02_fk_services_id` (`service_id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `users_groups`
--
ALTER TABLE `users_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_groups_user_id_group_id_fc7788e8_uniq` (`user_id`,`group_id`),
  ADD KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `users_user_permissions`
--
ALTER TABLE `users_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` (`user_id`,`permission_id`),
  ADD KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `medical_records`
--
ALTER TABLE `medical_records`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users_groups`
--
ALTER TABLE `users_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users_user_permissions`
--
ALTER TABLE `users_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_doctor_id_96635781_fk_users_id` FOREIGN KEY (`doctor_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `appointments_patient_id_b2db55d3_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `medical_records`
--
ALTER TABLE `medical_records`
  ADD CONSTRAINT `medical_records_appointment_id_3d2abcab_fk_appointments_id` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`id`),
  ADD CONSTRAINT `medical_records_doctor_id_eac1d872_fk_users_id` FOREIGN KEY (`doctor_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `medical_records_patient_id_a9bed619_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`);

--
-- Constraints for table `patients`
--
ALTER TABLE `patients`
  ADD CONSTRAINT `patients_user_id_11c42fa7_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_patient_id_0223ebbf_fk_patients_id` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`),
  ADD CONSTRAINT `reviews_service_id_00992c02_fk_services_id` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`);

--
-- Constraints for table `users_groups`
--
ALTER TABLE `users_groups`
  ADD CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `users_user_permissions`
--
ALTER TABLE `users_user_permissions`
  ADD CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
