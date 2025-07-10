SET SQL_SAFE_UPDATES = 0;


SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

DELETE FROM `user_competition_roles` ;
DELETE FROM `user_competition_moderators` ;
DELETE FROM `votes` ;
DELETE FROM `announcements` ;
DELETE FROM `competitors` ;
DELETE FROM `events` ;
DELETE FROM `charities` ;
DELETE FROM `competitions` ;
DELETE FROM `applications` ;
DELETE FROM `users` ;
DELETE FROM `messages` ;
DELETE FROM `replies` ;
DELETE FROM `donation_receipts` ;
DELETE FROM `bans`;
DELETE FROM `appeals`;
DELETE FROM `site_wide_ban_appeals`; 
DELETE FROM `site_wide_bans` ;
DELETE FROM `instant_messages` ;
DELETE FROM `user_last_message` ;
DELETE FROM `themes` ;
DELETE FROM `gallery_themes`;


SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;


-- Insert Voters 
INSERT INTO users (user_id, username, first_name, last_name, `description`, password_hash, email, is_active)
VALUES 
(1, 'voter1', 'Charlotte', 'Murphy', 'Yes! The first voter!', 'e38aa44b84afe8889f8e74eacaeb304a5c0aecc0e10eaf92032c5109e9b4a7b6', 'voter1@vms.com', TRUE),
(2, 'voter2', 'Bob', 'Kelly', '', '825a0492d22c9f2e5ee53156f640a1d989568af03ae8fbbdf5546cc64ba534d3', 'voter2@vms.com', TRUE),
(3, 'voter3', 'Amelia', 'Robinson', '', 'ed8a0afc92a9271e4a05d32e9539b615160e331e6ff933e5da82aa1b08814ab2', 'voter3@vms.com', TRUE),
(4, 'voter4', 'Oliver', 'Ryan', '', '5b40b602fc24c218b3f491d84ee510794af6f317bbcd203a33edafc19a759759', 'voter4@vms.com', TRUE),
(5, 'voter5', 'Isla', 'Lee', 'I signed up because of John Oliver', '197f26331bb601e7abedeaf206a0dc86d4faef9697c50dc72514c0f6bc032d1c', 'voter5@vms.com', TRUE),
(6, 'voter6', 'Luca', 'Harris', '', 'fe087610cfb6d8cdaa4346842bef8ff116d50fda9eb9851ba1de3e2a362ef501', 'voter6@vms.com', TRUE),
(7, 'voter7', 'Olivia', 'Walker', '', '97e4fc9a3484122b2cc673dcd3aa26fa40c3bb52fd6f6f3ea93d910fe41a4f6e', 'voter7@vms.com', TRUE),
(8, 'voter8', 'Jack', 'Turner', '', 'bf13eb0f593d7e62868a34ed37efc3102e0eee4aa0e58f931ded32605bb72570', 'voter8@vms.com', TRUE),
(9, 'voter9', '', '', 'Not John Oliver', '7bc24f05ea5e53273098ba77a050d47cfe657bd230523ad4dcb118a11106a213', 'voter9@vms.com', TRUE),
(10, 'voter10', 'Harper', 'Nguyen', '', '42d536b2f049a94f862432417d78d41ec993180c705e7247e0e4233432e87d16', 'voter10@vms.com', TRUE),
(11, 'voter11', 'Leo', 'Thompson', '', 'df6eb982e28230d6c8d59495d6a72a88a8d8d8216c5a162576d9650f8e3c2242', 'voter11@vms.com', TRUE),
(12, 'voter12', 'Willow', 'Singh', '', '80703d285ce71381f396267980d440f4116408091417aa2a18a3b7924d1c0081', 'voter12@vms.com', TRUE),
(13, 'voter13', 'Theodore', 'Martin', 'My name is Ted Martin. I am not John Oliver.', '6f7b8a97091fe1ad732028235b3e1e9259e06e25cfd3c57d71e01cbd056d6913', 'voter13@vms.com', TRUE),
(14, 'voter14', '', '', '', '5892c98de990afb58e49083ad1b2e5399949b0244426e5af51f62c8b4cc002d2', 'voter14@vms.com', TRUE),
(15, 'voter15', '', '', 'Here for the trees', '976d657d2a0d1edd0cd7de83238dd257c3dbf4c03aab6adcb54c1c5b79b29ca8', 'voter15@vms.com', TRUE),
(16, 'voter16', 'Lily', 'White', '', 'cb3ab38e832c8c1d6058949e7eb44b81627b0fef70afc0efa6a3409a06854748', 'voter16@vms.com', TRUE),
(17, 'voter17', '', '', '', '95d2ca6432cecb06ec48cfaca899b5e09c90557245b0691ae97e15bc60c837f4', 'voter17@vms.com', TRUE),
(18, 'voter18', '', '', '', 'cee033f348472bf042b44410e16ff5e100552d25ea4d9c9dd0c6d07e43e5da79', 'voter18@vms.com', TRUE),
(19, 'voter19', 'George', 'Johnson', '', '762460975b50ce267b1fef115aca947be09b142dc0f2d65e203683a9286d76e0', 'voter19@vms.com', TRUE),
(20, 'voter20', 'Ava', 'Taylor', '', '884611a667d45a29ea860bea0393ba46b1c11a0e0ca93334c7fd576fbb3feaf7', 'voter20@vms.com', TRUE),
(21, 'voter21', 'Henry', 'Wilson', 'Bee crazy!', '809d2c05be2185e3802a6737f481fd0072fa93ca7c5e3c5b7f369927f74fab7d', 'voter21@vms.com', TRUE),
(22, 'voter22', 'Ella', 'Brown', "I am a long-time conservation worker. We lose so many species each year. It's time the Government properly funded conservation work, and competitions like these make a big difference for raising awareness.", 'ae9af85e0197d4b5484a58bf9d807eee3d51a7c024007a64cea80d21df02ff98', 'voter22@vms.com', TRUE),
(23, 'voter23', '', '', '', 'b7180c5a651da99a89cdbd83e160c12934efce18bcd4ad5c83313be110288b42', 'voter23@vms.com', TRUE),
(24, 'voter24', '', '', '', 'fc6a1e485acdb85924562c6b0830f1dc858d0539ba6440410f29a443306e8071', 'voter24@vms.com', TRUE),
(25, 'voter25', 'Charlie', 'Williams', 'My favourite competitions are:\n\n1. Insect of the Year\n\n2. Rock of the Year\n\n3. Butterfly of the Year', 'd0b30dd061d063173aac76c8b41a4fbcbeb8d167438c8b457e293089e752a075', 'voter25@vms.com', TRUE),
(26, 'voter26', '', '', '', '69b71d15619febb4d972a3a37658f9429a3af37a1627f8c27bb64cb14726b4d6', 'voter26@vms.com', TRUE),
(27, 'Crested Grebe rocks!', 'John', 'Oliver', "The Lord of the Wings. One bird to rule them all. It's got to be the puteketeke, which is magnificent and charming. Who wouldn't love it with it's unique looks, adorable parenting style, bizarre mating ritual, and propensity for eating feathers and puking", 'da0f9a103e55a8c7fad03ea54809b53d4e95a449a83d689b06faed2951eb3971', 'voter27@vms.com', TRUE),
(28, 'voter28', '', '', '', '22997eb91eaa42931c8d287e99f79a2d1774a6f93ec7fc866a21e7372bc677e5', 'voter28@vms.com', TRUE),
(29, 'voter29', 'Hudson', 'Smith', '', '3ae5a9fc0ab3eda54feefdc061f68357127500ab8de6bba6990b9c7161c89ce0', 'voter29@vms.com', TRUE),
(30, 'voter30', 'Mila', 'Singh', '', '9010ebef7d180b92ad506d0915c4851ea2bab00842ca1507e417a99b9189d39a', 'voter30@vms.com', TRUE);



-- Insert 5 Scrutineers
INSERT INTO users (user_id, username, first_name, last_name, password_hash, email, is_active)
VALUES 
(31, 'scrutineer1', 'Arthur', 'Smith', 'eac0254a27f5069d1cee6a3ba4ba8b690a7e385e52945ef8c05c02c3066dce92', 'scrutineer1@vms.com', TRUE),
(32, 'scrutineer2', '', '', 'dd8f7d6806e916459ee7a9559a836625e3ed9e4aa01b9f5c2aaccffd10456c8f', 'scrutineer2@vms.com', TRUE),
(33, 'scrutineer3', 'Evelyn', 'Kaur', '1aa7b634e1e25ae6fa9225d4984aa82165f7f631e9d9ec2406551187d885abd9', 'scrutineer3@vms.com', TRUE),
(34, 'scrutineer4', 'Arlo', 'Williams', '0bdf3648481c7c2db490ee0a9913da66c385224ca24982ebacac87e7fabbc273', 'scrutineer4@vms.com', TRUE),
(35, 'scrutineer5', 'Mia', 'Patel', 'dcaced30f9188282cd4c1b3d484e5554a790a31c16563d00ba6260f705aa919b', 'scrutineer5@vms.com', TRUE);


-- Insert 2 Administrators
INSERT INTO users (user_id, username, first_name, last_name, password_hash, email, is_active) VALUES 
(36, 'admin1', 'William', 'Wilson', '6b73a82d598a1e1e3713f707563670dc86b1077b30f47f8ef49e870bf2e259ae', 'admin1@vms.com', TRUE),
(37, 'admin2', 'Sophie', 'Brown', '4ed2ee320afb5dc527c35e6cc11c7b7258c1918aa43d84af742a2098dc251db2', 'admin2@vms.com', TRUE);

-- Insert 2 Site Admin

INSERT INTO users (user_id, username, password_hash, email, profile_image, is_active, site_role) VALUES 
(38, 'site_admin1', '2a38a4d1219011ec16a1b20082fd103c4177bb85aef3cbb5c131731d80d996fa', 'site_admin1@vms.com', '018c0730-0372-4a55-85fc-251c9665030a.png', TRUE, 'Site Admin');


-- Make some profile information visible
UPDATE users SET first_name_visible = 1 WHERE user_id IN (1, 2, 3, 5, 8, 13, 21);
UPDATE users SET last_name_visible = 1 WHERE user_id IN (1, 4, 9, 25, 3, 8, 21);
UPDATE users SET email_visible = 1 WHERE user_id IN (1, 5, 10, 15, 20, 25, 30, 35);
UPDATE users SET location_visible = 1, `location` = 'Canterbury' WHERE user_id IN (1, 5, 10, 15, 20, 25, 30, 35);
UPDATE users SET description_visible = 1 WHERE user_id IN (1, 2, 12, 22, 32);
UPDATE users SET publicly_visible = 0 WHERE user_id IN (10, 11, 12, 13);

-- Add profile images by storing image names for many users and then updating the users table with those names
DROP TABLE IF EXISTS temp;
CREATE TEMPORARY TABLE temp SELECT user_id, profile_image FROM users LIMIT 0;
INSERT INTO temp (user_id, profile_image)
VALUES
(1, '5e4b88a9-231b-41c5-8f35-e8409df26067.png'),
(2, '4fd44939-5f86-45b0-a7ed-65422cf0f083.png'),
(3, 'db2bbf14-311d-4d7b-a8b8-919805e16cb6.png'),
(21, '33029eae-c4ea-4ce8-b344-6da46d114220.png'),
(5, 'e1c9f285-4fe9-4070-b118-5863dc1cb6ae.png'),
(6, 'd37024f2-5a7e-40df-ba6d-7ccef0a4ca75.jpeg'),
(7, '82990a74-c761-40ea-8cc7-b6bde0d177a8.jpeg'),
(25, '02377d85-79ca-4709-80cb-774fc5ea6c8b.jpeg'),
(9, 'e87ac5b9-5d51-4d96-b2a8-84eeb9979c6e.png'),
(26, '6e745a27-cd27-4767-9210-b6044c94e436.png'),
(22, '3293d20a-2f9b-4bd7-877e-7f014bac14d2.png'),
(23, '46294338-b003-4636-a84d-33060638a72c.png'),
(12, '6f33613b-4767-4969-a011-80a454fb03cd.jpeg'),
(27, 'a6b9b409-817b-4214-9557-cea6a4e95446.png'),
(36, '553ce472-b987-42c6-a6d5-2d01bfdeae28.jpeg'),
(38, '018c0730-0372-4a55-85fc-251c9665030a.png'),
(39, 'default.jpg'),
(40, '8e2d1929-6bdc-4656-9a41-f84069a222b3.jpg');
UPDATE users JOIN temp ON users.user_id = temp.user_id SET users.profile_image = temp.profile_image;

-- Insert competitions
INSERT INTO competitions (competition_id, name, description) VALUES
(1, 'NZ Tree of the Year', 'Vote for your favorite native tree species in New Zealand'),
(2, 'NZ Bird of the Year', 'Vote for your favorite native bird species in New Zealand'),
(3, 'NZ Rock of the Year', 'Vote for your favorite native rock species in New Zealand'),
(4, 'NZ Walkway of the Year', 'Vote for your favorite walkway')
;

-- Insert events
INSERT INTO events (event_id, competition_id, name, description, start_date, end_date, is_visible, status) VALUES
(1, 1, 'NZ Tree of the Year 2023', 'Vote for your favorite native tree species in New Zealand', '2023-08-15', '2023-09-30', TRUE, 'finalised'),
(2, 1, 'NZ Tree of the Year 2024', 'Vote for your favorite native tree species in New Zealand', '2024-08-15', '2024-09-30', TRUE, 'active'),
(3, 1, 'NZ Tree of the Year 2025', 'Vote for your favorite native tree species in New Zealand', '2025-08-15', '2025-09-30', TRUE, 'active'),
(4, 4, 'NZ Walkway of the Year 2024', 'Vote for your favourite walkway 2024', '2024-08-15', '2024-11-30', TRUE, 'active'),
(5, 4, 'NZ Walkway of the Year 2025', 'Vote for your favourite walkway 2025', '2025-08-15', '2025-11-30', TRUE, 'active'),
(6, 4, 'NZ Walkway of the Year 2023', 'Vote for your favourite walkway 2023', '2023-08-15', '2023-11-30', TRUE, 'finalised'),
(7, 2, 'NZ Bird of the Year 2024', 'Vote for your favourite bird in 2024', '2024-08-15', '2024-11-30', TRUE, 'active'),
(8, 1, 'NZ Tree of the Year 2022', 'Vote for your favorite native tree species in New Zealand', '2022-08-15', '2022-09-30', TRUE, 'finalised')
;
 

-- Insert competitors
INSERT INTO competitors (competitor_id, event_id, name, description, image) VALUES
(1, 1, 'Tī Kōuka', 'Commonly known as the cabbage tree, with sword-like leaves', '756afdf9-eb4b-443b-87a1-3d73195aa95b.png'),
(2, 1, 'Nīkau', 'The only native palm in New Zealand, often found in coastal forests', '108eda84-2885-497b-8a31-9262f50d6445.png'),
(3, 1, 'Pōhutukawa', 'Often called the New Zealand Christmas tree, famous for its bright red flowers', '1e1d0ff9-38d6-4830-955b-6a9ab15041e4.png'),
(4, 2, 'Kauri', 'A large New Zealand native tree known for its towering height and longevity', 'f11197d9-570f-45e3-9ae7-e8dd5619a2c8.png'),
(5, 2, 'Rimu', 'An evergreen coniferous tree valued for its beautiful timber', '7a2e6aac-a6bf-42ca-a8a7-34c61acf18c5.png'),
(6, 2, 'Tōtara', 'A tall native tree of New Zealand, historically significant to Māori for carving and building', '6c61526e-3d07-44cb-8a8e-185e0d574cd8.png'),
(7, 2, 'Kōwhai', 'Known for its brilliant yellow flowers that attract birds like the tūī', '7d22af03-96a3-42bf-9951-406743175fd5.png'),
(8, 2, 'Pōhutukawa', 'Often called the New Zealand Christmas tree, famous for its bright red flowers', '342b3358-cdf1-42ea-b216-1376a9b40146.png'),
(9, 2, 'Mānuka', 'Famous for its honey, with small white or pink flowers', '3180d0d5-de73-4459-9c03-690533321348.png'),
(10, 2, 'Kahikatea', 'The tallest native tree in New Zealand, often found in swampy forests', '5b182a60-ffe5-4370-9132-35fed6abc3a5.png'),
(11, 2, 'Mātai', 'A large native tree with distinctive black bark and edible berries', '194021de-e5d1-4e27-a1a6-4fb218d5047c.png'),
(12, 2, 'Pūriri', 'Known for its hardwood and medicinal properties', 'c6a7b80e-a5b2-423c-8406-83b4c8abcb0a.png'),
(13, 2, 'Nīkau', 'The only native palm in New Zealand, often found in coastal forests', 'c4e3f902-f858-40dc-9f05-08894b388aa3.png'),
(14, 2, 'Pūkātea', 'A tree of swampy areas with buttressed roots', '47f12131-772c-4791-b032-a5bfa901a5aa.jpg'),
(15, 2, 'Rewarewa', 'Also known as the New Zealand honeysuckle, with reddish-brown flowers', '30ec8d70-703b-4d94-b003-7156360874f3.png'),
(16, 2, 'Tawa', 'A large forest tree with purple-black berries', 'dbe99966-53be-4cb2-add4-030a78e44923.png'),
(17, 2, 'Miro', 'A tree with red berries, which are a favorite of the native kererū', 'c973bc53-c737-4a25-9f13-709f4779295c.png'),
(18, 2, 'Karaka', 'A tree with large orange fruit, significant in Māori culture', 'd7b73f5e-fef6-4495-afc9-5fb202c81981.png'),
(19, 2, 'Silver beech', 'A tall tree with smooth grey bark, common in southern forests', 'b4ad8335-bb37-49d9-b381-e73c1f277e8a.png'),
(20, 2, 'Rātā', 'Known for its vibrant red flowers, similar to the pōhutukawa', 'e7abb3c3-f90a-4868-a64d-9e13a5106fe8.png'),
(21, 2, 'Whau', 'A tree with large heart-shaped leaves and light wood, used for making floats', '500a2a81-5a17-475f-95f2-8b4029ad1155.jpg'),
(22, 2, 'Tī Kōuka', 'Commonly known as the cabbage tree, with sword-like leaves', '85f8733b-d483-4887-8249-93c7ca4017dd.png'),
(23, 2, 'Horoeka', 'Also known as lancewood, a unique, small tree with lance-like foliage that changes dramatically as the tree matures', 'cd74aaa2-2992-4bf3-b479-9d3a376d3ad1.jpg'),
(24, 4, 'Milford Track', 'A 53.5 km hike in Fiordland National Park, New Zealand, renowned for its stunning waterfalls and valleys.', '9cb0fc28-ec35-4aac-86c3-5352adc629ca.jpg'),
(25, 4, 'Heaphy Track', 'The Heaphy Track is a 78.4 km hiking trail in Kahurangi National Park, South Island, featuring diverse landscapes, including rainforests, mountains, and beaches,
 including rainforests, mountains, and beaches.', '153cb0ab-1374-49a2-ac00-dde5644fd0c8.jpg'),
(26, 4, 'Routeburn Track', 'A 33 km alpine trail in New Zealand, connecting Fiordland and Mount Aspiring National Parks, with spectacular mountain views', 'ac9f284b-9ee7-4ece-bddc-a4847c6d9f0b.jpg'),
(27, 5, 'Heaphy Track', 'The Heaphy Track is a 78.4 km hiking trail in Kahurangi National Park, South Island, featuring diverse landscapes, including rainforests, mountains, and beaches,
 including rainforests, mountains, and beaches.', 'd2727b9a-d1d8-414b-9eb4-5917b62459a8.jpg'),
(28, 6, 'Heaphy Track', 'The Heaphy Track is a 78.4 km hiking trail in Kahurangi National Park, South Island, featuring diverse landscapes, including rainforests, mountains, and beaches,
 including rainforests, mountains, and beaches.', '2ca5dd06-210d-4ef4-9b90-ab9adc1fb1ea.jpg'),
(29, 6, 'Routeburn Track', 'A 33 km alpine trail in New Zealand, connecting Fiordland and Mount Aspiring National Parks, with spectacular mountain views', 'f6f51f7a-4722-4ad7-a48e-0fce310978d4.jpg'),
(30, 3, 'Whau', 'A tree with large heart-shaped leaves and light wood, used for making floats', '523ac817-dadd-4992-89a7-a2abcc994d48.jpg'),
(31, 3, 'Tī Kōuka', 'Commonly known as the cabbage tree, with sword-like leaves', '6a2f72ed-c225-42ff-b4db-9a9a9d4dd92f.png'),
(32, 3, 'Horoeka', 'Also known as lancewood, a unique, small tree with lance-like foliage that changes dramatically as the tree matures', 'd6e107cb-c454-4bf0-adb0-cae3da46c876.jpg'),
(33, 7, 'Kiwi', 'Recovering', '243d1102-261e-4423-8d29-77945fe53d20.png'),
(34, 7, 'Kakapo', 'Endangered', '4947f0a0-0ece-401f-9671-c227c1cb30a9.png'),
(35, 7, 'Puteketeke', 'Known for its distinctive plumage', '02d9414f-1061-49d7-9ed4-a5e3597829ac.png'),
(36, 8, 'Kauri', 'A large New Zealand native tree known for its towering height and longevity', 'a4de98ae-4769-45e3-a7b9-a214034b3a78.png'),
(37, 8, 'Rimu', 'An evergreen coniferous tree valued for its beautiful timber', '619344b9-235d-4733-b02a-c78138b16fc3.png'),
(38, 8, 'Tōtara', 'A tall native tree of New Zealand, historically significant to Māori for carving and building', '403032a5-7b2e-4a88-8630-f5495fa47c2d.png'),
(39, 8, 'Kōwhai', 'Known for its brilliant yellow flowers that attract birds like the tūī', '910eb9a8-ae69-4b89-aed6-83d37d568df7.png'),
(40, 8, 'Pōhutukawa', 'Often called the New Zealand Christmas tree, famous for its bright red flowers', 'ef8a40d0-5ab8-42fc-8966-e21389963284.png')
;

-- Insert votes for previous event
INSERT INTO votes (user_id, event_id, competitor_id, ip_address, vote_time) VALUES
(1, 1, 1, '192.168.1.1', '2023-08-15 10:00:00'),
(2, 1, 1, '192.168.1.2', '2023-08-15 11:15:00'),
(3, 1, 1, '192.168.1.3', '2023-08-15 12:30:00'),
(4, 1, 1, '192.168.1.4', '2023-08-15 13:45:00'),
(5, 1, 1, '192.168.1.5', '2023-08-15 14:00:00'),
(6, 1, 1, '192.168.1.6', '2023-08-16 09:30:00'),
(7, 1, 1, '192.168.1.7', '2023-08-16 10:45:00'),
(8, 1, 1, '192.168.1.8', '2023-08-16 11:00:00'),
(9, 1, 1, '192.168.1.9', '2023-08-17 15:20:00'),
(10, 1, 2, '192.168.1.10', '2023-08-17 16:30:00'),
(11, 1, 2, '192.168.1.11', '2023-08-30 17:45:00'),
(12, 1, 2, '192.168.1.12', '2023-08-18 08:00:00'),
(13, 1, 2, '192.168.1.13', '2023-08-18 09:15:00'),
(14, 1, 2, '192.168.1.14', '2023-09-18 10:30:00'),
(15, 1, 2, '192.168.1.15', '2023-08-18 11:45:00'),
(16, 1, 2, '192.168.1.16', '2023-08-18 12:00:00'),
(17, 1, 3, '192.168.1.17', '2023-08-18 13:00:00'),
(18, 1, 3, '192.168.1.18', '2023-08-18 14:15:00'),
(19, 1, 3, '192.168.1.19', '2023-08-18 15:30:00'),
(20, 1, 3, '192.168.1.20', '2023-08-23 16:45:00'),
(20, 6, 28, '192.168.1.20', '2023-08-23 16:45:00'),
(21, 6, 28, '192.168.1.20', '2023-08-23 16:45:00'),
(7, 8, 40, '192.168.1.7', '2022-08-17 10:45:00'),
(8, 8, 40, '192.168.1.8', '2022-08-18 11:00:00'),
(9, 8, 39, '192.168.1.9', '2022-08-26 15:20:00');

-- Insert for Walkway of the Year 2024
INSERT INTO votes (user_id, event_id, competitor_id, ip_address, vote_time) VALUES
(1, 4, 24, '192.168.1.1', '2023-08-15 10:00:00'),
(2, 4, 25, '192.168.1.2', '2023-08-15 11:15:00'),
(3, 4, 25, '192.168.1.3', '2023-08-15 12:30:00'),
(4, 4, 26, '192.168.1.4', '2023-08-15 13:45:00'),
(5, 4, 24, '192.168.1.5', '2023-08-15 14:00:00'),
(6, 4, 24, '192.168.1.6', '2023-08-16 09:30:00'),
(7, 4, 26, '192.168.1.7', '2023-08-16 10:45:00'),
(8, 4, 26, '192.168.1.8', '2023-08-16 11:00:00'),
(9, 4, 24, '192.168.1.9', '2023-08-17 15:20:00'),
(10, 4, 25, '192.168.1.10', '2023-08-17 16:30:00'),
(11, 4, 25, '192.168.1.11', '2023-08-30 17:45:00'),
(12, 4, 24, '192.168.1.12', '2023-08-18 08:00:00'),
(13, 4, 25, '192.168.1.13', '2023-08-18 09:15:00'),
(14, 4, 24, '192.168.1.14', '2023-09-18 10:30:00'),
(15, 4, 26, '192.168.1.15', '2023-08-18 11:45:00'),
(16, 4, 25, '192.168.1.16', '2023-08-18 12:00:00'),
(17, 4, 24, '192.168.1.17', '2023-08-18 13:00:00'),
(18, 4, 24, '192.168.1.18', '2023-08-18 14:15:00'),
(19, 4, 24, '192.168.1.19', '2023-08-18 15:30:00'),
(20, 4, 26, '192.168.1.20', '2023-08-23 16:45:00');

-- Insert votes for current event (including anomalies with multiple votes from one IP address)
INSERT INTO votes (user_id, event_id, competitor_id, ip_address, vote_time)
VALUES
(1, 2, 4, '192.168.1.1', '2024-08-16 08:00:00'),
(2, 2, 5, '192.168.1.2', '2024-08-16 09:00:00'),
(3, 2, 6, '192.168.1.3', '2024-08-16 10:05:00'),
(4, 2, 7, '192.168.1.4', '2024-08-16 11:00:00'),
(5, 2, 8, '192.168.1.5', '2024-08-16 14:09:00'),
(6, 2, 9, '192.168.1.6', '2024-08-16 17:00:00'),
(7, 2, 10, '192.168.1.7', '2024-08-16 14:00:00'),
(8, 2, 11, '192.168.1.8', '2024-08-16 15:00:00'),
(9, 2, 12, '192.168.1.9', '2024-08-16 16:00:00'),
(10, 2, 13, '192.168.1.10', '2024-08-16 17:00:00'),
(11, 2, 14, '192.168.1.11', '2024-08-16 18:00:00'),
(12, 2, 15, '192.168.1.12', '2024-08-16 17:50:00'),
(13, 2, 16, '192.168.1.13', '2024-08-16 20:09:00'),
(14, 2, 17, '192.168.1.16', '2024-08-16 13:20:00'),
(15, 2, 18, '192.168.1.15', '2024-08-16 22:00:00'),
(16, 2, 19, '192.168.1.14', '2024-08-17 08:30:00'),
(17, 2, 20, '192.168.1.17', '2024-08-17 09:00:00'),
(18, 2, 21, '192.168.1.18', '2024-08-17 10:00:00'),
(19, 2, 22, '192.168.1.19', '2024-08-17 11:40:00'),
(20, 2, 23, '192.168.1.20', '2024-08-17 12:50:00'),
(21, 2, 22, '192.168.1.20', '2024-08-17 12:51:00'), -- Anomaly
(22, 2, 5, '192.168.1.1', '2024-08-18 08:00:00'),  -- Anomaly
(23, 2, 6, '192.168.1.1', '2024-08-18 09:00:00'),  -- Anomaly
(24, 2, 7, '192.168.1.2', '2024-08-18 10:00:00'),  -- Anomaly
(25, 2, 7, '192.168.1.2', '2024-08-18 10:00:00'),  -- Anomaly
(26, 2, 8, '192.168.1.2', '2024-08-18 11:00:00');  -- Anomaly

-- Insert votes for recent voters (for Bird of Year, and one vote for walkway of the year)
INSERT INTO votes (user_id, event_id, competitor_id, ip_address, vote_time)
VALUES
(21, 7, 33, '192.168.1.1', SUBTIME(CURRENT_TIMESTAMP(), "5:22:10.00001")),
(22, 7, 35, '192.168.1.2', SUBTIME(CURRENT_TIMESTAMP(), "5:21:44.00001")),
(23, 7, 35, '192.168.1.3', SUBTIME(CURRENT_TIMESTAMP(), "5:20:16.00001")),
(25, 7, 33, '192.168.1.4', SUBTIME(CURRENT_TIMESTAMP(), "6:18:38.00001")),
(26, 4, 25, '192.168.1.5', SUBTIME(CURRENT_TIMESTAMP(), "9:28:1.00001")),
(26, 7, 34, '192.168.1.5', SUBTIME(CURRENT_TIMESTAMP(), "23:44:47.00001")),
(27, 7, 35, '192.168.1.5', SUBTIME(CURRENT_TIMESTAMP(), "5:22:48.00001"));

-- Insert charities
INSERT INTO charities (charity_id, competition_id, name, services_registration, bank_account_number, ird_number, official_stamp, authorisor_name, authorisor_designation, authorisor_signature) VALUES
(1, 1, 'Save the Trees', '123456', '01-0123-0123456-00', '123-456-789', 0, 'Bob Smith', 'Treasurer', 0);


-- Insert user_competition_roles
INSERT INTO user_competition_roles (user_id, competition_id, role) VALUES
(31, 1, 'scrutineer'),
(32, 1, 'scrutineer'),
(33, 1, 'scrutineer'),
(34, 1, 'scrutineer'),
(35, 1, 'scrutineer'),
(36, 1, 'admin'),
(37, 1, 'admin'),
(37, 4, 'admin'),
(35, 2, 'scrutineer'),
(35, 4, 'scrutineer');

-- Insert user_competition_moderators
INSERT INTO user_competition_moderators (user_id, competition_id) VALUES
(35, 1);

-- Insert applications
INSERT INTO applications (application_id, application_by_user, name, description, visible, application_time, status, reason) VALUES
(1, 36, 'NZ Rock of the Year', 'Vote for rocks', TRUE, '2023-08-15 10:00:00', 'pending', ""),
(2, 36, 'NZ Beach of the Year', 'Vote for your favourite beach', TRUE, '2023-08-15 11:00:00', 'pending', ""),
(3, 36, 'NZ Fish of the Year', 'Vote for your favourite fish', TRUE, '2023-08-15 12:00:00', 'pending', ""),
(4, 37, 'NZ Insect of the Year', 'Vote for your favourite insect', TRUE, '2023-08-14 13:00:00', 'pending', ""),
(5, 37, 'NZ Car of the Year', 'Vote for your favourite car', TRUE, '2023-08-15 14:00:00', 'rejected', "not to do with conservation"),
(6, 1, 'NZ Plant of the Year', 'Vote for your favourite plant', TRUE, '2023-08-17 14:00:00', 'pending', ""),
(7, 1, 'NZ Bird of the Year', 'Vote for your favourite bird', TRUE, '2023-08-17 15:00:00', 'pending',"" ),
(8, 1, 'NZ Mammal of the Year', 'Vote for your favourite mammal', TRUE, '2023-08-17 16:00:00', 'rejected', "not enough public interest"),
(9, 2, 'NZ Lake of the Year', 'Vote for your favourite lake', TRUE, '2023-08-18 09:00:00', 'approved', ""),
(10, 2, 'NZ Desert of the Year', 'Vote for your favourite desert', TRUE, '2023-08-18 10:00:00', 'rejected', "not relevant"),
(11, 2, 'NZ Volcano of the Year', 'Vote for your favourite volcano', TRUE, '2023-08-18 11:00:00', 'pending', ""),
(12, 3, 'NZ Reptile of the Year', 'Vote for your favourite reptile', TRUE, '2023-08-19 09:00:00', 'pending', ""),
(13, 3, 'NZ Amphibian of the Year', 'Vote for your favourite amphibian', TRUE, '2023-08-19 10:00:00', 'rejected', "lack of public interest"),
(14, 3, 'NZ Invertebrate of the Year', 'Vote for your favourite invertebrate', TRUE, '2023-08-19 11:00:00', 'pending', "");

-- Insert donations
INSERT INTO donation_receipts (user_id, charity_id, amount, donation_date, donor_full_name, pay_provider_confirmation, cancelled) VALUES
(1, 1, 100.00, '2023-08-15 10:00:00', 'John Doe', 'fdsf32423', 0),
(1, 1, 200.00, '2023-08-15 11:00:00', 'John Doe', 'fdfae23423', 0),
(2, 1, 300.00, '2023-08-15 12:00:00', 'Jane Doe', 'fadfadf32423', 0),
(2, 1, 400.00, '2023-08-15 13:00:00', 'Jane Doe', 'fdafse32342', 0),
(3, 1, 500.00, '2023-08-15 14:00:00', 'Bob Smith', 'fafdfwre23423', 1),
(3, 1, 600.00, '2023-08-15 15:00:00', 'Bob Smith', 'dawrqe2342', 0),
(4, 1, 700.00, '2023-08-15 16:00:00', 'Michelle Smith', 'zcvdsf3423', 0),
(4, 1, 800.00, '2023-08-15 17:00:00', 'Michelle Smith', 'zxcvc23423', 0),
(5, 1, 900.00, '2023-08-15 18:00:00', 'Rachel Smith', 'zcvdb34123', 0),
(5, 1, 1000.00, '2023-08-15 19:00:00', 'Rachel Smith', 'cvzxc332432', 0);


-- Insert Bans
INSERT INTO bans (ban_id, user_id, competition_id, ban_date, reason) VALUES
(1, 1, 1, NOW(), 'Inappropriate behavior'),
(2, 2, 1, NOW(), 'Cheating in competition'),
(3, 3, 1, NOW(), 'Repeated violations of rules'),
(4, 1, 2, NOW(), 'Spamming'),
(5, 2, 2, NOW(), 'Abusive language'),
(6, 3, 4, NOW(), 'Unauthorised access'), -- No appeal for this ban
(7, 1, 3, NOW(), 'Cheating detected');  -- No appeal for this ban


-- Insert Appeals
INSERT INTO appeals (appeal_id, ban_id, competition_id, appeal_date, status, reason, response, response_date) VALUES

(1, 1, 1, NOW(), 'denied', 'I was wrongfully banned.', 'Appeal denied due to inappropriate behavior.', NOW()),  -- Denied appeal
(2, 2, 1, NOW(), 'pending', 'This was a misunderstanding.', NULL, NULL),  -- Accepted appeal, ban revoked
(3, 4, 2, NOW(), 'pending', 'I did not spam.', NULL, NULL);  -- Pending appeal for User 1


-- Insert sitewide bans
INSERT INTO site_wide_bans (site_wide_ban_id, user_id, reason) VALUES
(1, 1, 'Violation of community guidelines'),
(2, 7, 'Spamming multiple accounts'),
(3, 6, 'Abusive behavior towards other users'),
(4, 4, 'Inappropriate content'),    -- no appeal for this ban
(5, 5, 'Fraudulent activity');   -- no appeal for this ban

-- Insert sitewide ban appeals
INSERT INTO site_wide_ban_appeals (site_wide_ban_id, reason, status, response, response_date) VALUES
(1, 'I believe the ban was unjustified.', 'pending', NULL, NULL),         -- User 1 has a pending appeal

(2, 'I have changed my behavior and request reconsideration.', 'pending', 'Your appeal has been denied.', NOW()),  
(3, 'I was not aware of the rules regarding account creation.', 'pending', 'Your appeal has been accepted.', NOW());

INSERT INTO messages (message_id,competition_id,user_id,title,content,created_at) VALUES
(1,2,1,"All things Puteketeke","This post is for discussing the best bird in the world, the Puteketeke!","2024-10-07 22:58:45"),
(2,4,1,"More competitors","Would the admin please add more competitors this year? It would be way better if there were more than three competitors.","2024-10-07 23:08:57");


INSERT INTO `instant_messages` (`to_user`, `from_user`, `message`, `sent`) VALUES
(2, 1, 'Hi, I’m Voter 1! How are you?', '2024-10-10 10:00:00'),
(1, 2, 'Hey Voter 1! I’m good, thanks! How about you?', '2024-10-10 10:05:00'),
(1, 3, 'I just voted for the Bird of the Year! Did you?', '2024-10-11 11:00:00'),
(3, 1, 'Not yet! I’m still thinking about it. Any favorites?', '2024-10-11 11:10:00'),
(3, 4, 'Hi there, Voter 3! Who did you vote for in the competition?', '2024-10-12 12:00:00'),
(4, 3, 'Hey! I went with the Kiwi. It’s such a cool bird!', '2024-10-12 12:05:00'),
(5, 1, 'Hello, Voter 5! What do you think about the Bird of the Year this time?', '2024-10-13 12:00:00'),
(1, 5, 'hi Voter 1, I’m really enjoying the competition! So many interesting birds this year.', '2024-10-13 12:02:00'),
(2, 3, 'Have you checked out the profiles of the birds? They’re fascinating!', '2024-10-13 12:05:00'),
(3, 2, 'Yes! I love learning about them. Makes the voting more fun!', '2024-10-13 12:10:00');

INSERT INTO replies (reply_id,message_id,user_id,content,created_at) VALUES
(1,1,1,"I hope everyone is voting for the Puteketeke this year.","2024-10-07 23:03:34"),
(2,1,10,"You really want to vote for a bird that pukes and can't walk on land?","2024-10-07 23:05:35"),
(3,1,1,"Who needs to walk on land when you can paddle on a giant lake?","2024-10-07 23:07:24"),
(4,2,37,"Yes, we're working on it.","2024-10-07 23:15:02"),
(5,2,1,"Oh good","2024-10-07 23:15:30");



INSERT INTO themes (style_id, competition_id, theme_name, background_color, 
    topic_text_color, topic_font_size, main_text_color, main_font_size
) VALUES

(1, 1, 'Classic White', '#FFFFFF', '#000000', '2rem', '#000000', '1.25rem'),
(2, 2, 'Classic White', '#FFFFFF', '#000000', '2rem', '#000000', '1.25rem'),
(3, 3, 'Classic White', '#FFFFFF', '#000000', '2rem', '#000000', '1.25rem'),
(4, 4, 'Classic White', '#FFFFFF', '#000000', '2rem', '#000000', '1.25rem');


INSERT INTO gallery_themes (competition_id, theme_name, screenshot_path, background_color, topic_text_color, topic_font_size, main_text_color, main_font_size)
VALUES
-- Competition 1 Themes
(0, 'Classic White', 'theme_screenshots/16af776d-a081-45a4-a453-e57c6d6cd5f8.png', '#FFFFFF', '#000000', '2rem', '#000000', '1rem'),
(0, 'Forest Green', 'theme_screenshots/1000a78c-fdd3-4ab5-9b0d-e8154471b5ba.png', '#2E8B57', '#FFFFFF', '2.5rem', '#FFFFFF', '1.5rem'),
(0, 'Sunny Beach', 'theme_screenshots/d05cfa9b-d67b-4237-a438-633352d455d2.png', '#FFD700', '#1E90FF', '3rem', '#1E90FF', '1.75rem'),

-- Competition 2 Themes
(0, 'Autumn Orange', 'theme_screenshots/0aceb0fa-81b6-496d-95b4-361ca9daf87c.png', '#FFA500', '#8B0000', '2rem', '#8B0000', '1.5rem'),
(0, 'Ocean Blue', 'theme_screenshots/e91d10f7-39a4-4802-b725-a3412ae00f8d.png', '#1E90FF', '#FFFFFF', '2.5rem', '#FFFFFF', '1.75rem'),
(0, 'Lavender Purple', 'theme_screenshots/6613095d-16f0-4280-ae7a-226e654fd3d0.png', '#E6E6FA', '#4B0082', '3rem', '#4B0082', '2rem'),

-- Competition 3 Themes
(0, 'Moss Green', 'theme_screenshots/4e04e334-5ab3-4011-845c-bd844183c8ed.png', '#8FBC8F', '#2F4F4F', '2rem', '#2F4F4F', '1.5rem'),
(0, 'Desert Sand', 'theme_screenshots/10750452-68e0-41ce-9f3b-7d6789f6648d.png', '#EDC9AF', '#8B4513', '2.5rem', '#8B4513', '1.75rem'),
(0, 'Ice Blue', 'theme_screenshots/8ee5ebed-72d5-4de6-8dbe-ee53d746d5df.png', '#B0E0E6', '#00008B', '3rem', '#00008B', '2rem'),

-- Competition 4 Themes
(0, 'Sunset Red', 'theme_screenshots/e1b6b2de-0d62-450a-81ca-389135fc7852.png', '#FF4500', '#FFFFFF', '2rem', '#FFFFFF', '1.5rem'),
(0, 'Spring Yellow', 'theme_screenshots/5e8f366c-84d8-4c38-aa2e-7d127482f8ee.png', '#FFFFE0', '#FFD700', '2.5rem', '#FFD700', '1.75rem'),
(0, 'Night Sky', 'theme_screenshots/58fa2645-70c9-41ae-9307-3b1dd29708a0.png', '#000033', '#FFFFFF', '3rem', '#FFFFFF', '2rem');


