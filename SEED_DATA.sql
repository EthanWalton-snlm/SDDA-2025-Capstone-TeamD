DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS policyTypes;
DROP TABLE IF EXISTS usersToContact;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username NVARCHAR(100) PRIMARY KEY,
    password NVARCHAR(500),
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    email NVARCHAR(50),
    phone_number NVARCHAR(13),
    id_number NVARCHAR(13),
	is_admin INT DEFAULT 0, -- 1 = True
	profile_pic NVARCHAR(500) NULL
);

CREATE TABLE usersToContact (
    id_number NVARCHAR(13) PRIMARY KEY,
    name NVARCHAR(50),
    surname NVARCHAR(50),
    email NVARCHAR(50),
    phone_number NVARCHAR(13),
    method_of_contact NVARCHAR(50),
    message NVARCHAR(max)
);

CREATE TABLE policyTypes (
    policy_type_id NVARCHAR(50) PRIMARY KEY,
    name NVARCHAR(100),
    summary NVARCHAR(500),
	start_price FLOAT
);

CREATE TABLE policies (
    policy_id NVARCHAR(50) PRIMARY KEY,
    premium FLOAT,
    phone_name NVARCHAR(50),
    policy_name NVARCHAR(50),
    phone_case NVARCHAR(50),
    screen_protector NVARCHAR(50),
    waterproof_phone NVARCHAR(50),
    username NVARCHAR(100) REFERENCES users(username),
    policy_type_id NVARCHAR(50) REFERENCES policyTypes(policy_type_id),
    image_link NVARCHAR(500) NULL
);

CREATE TABLE claims (
    claim_id NVARCHAR(50) PRIMARY KEY,
    status NVARCHAR(25),
    reason NVARCHAR(500),
    admin_comment NVARCHAR(500),
    affidavit_link NVARCHAR(MAX),
    image_link NVARCHAR(MAX),
    quotation_link NVARCHAR(MAX),
    approved_by NVARCHAR(100),  -- column to store the admin who approved the claim
    rejected_by NVARCHAR(100),  -- column to store the admin who rejected the claim
    submission_date DATETIME NOT NULL DEFAULT GETDATE(), -- date when claim is submitted
    date_of_incident DATE NOT NULL, -- date when the incident happened
    username NVARCHAR(100) REFERENCES users(username),
    policy_id NVARCHAR(50) REFERENCES policies(policy_id),
	claim_amount FLOAT,
	amount_approved FLOAT
);

INSERT INTO users (username, password, first_name, last_name, is_admin, profile_pic)
VALUES
('john545', 'scrypt:32768:8:1$XX4iX48LUzwzHRST$b51014d60219704eccda5766b47dc760430333aa17e8848da5650f52e4427b71c6bbf2cb4ba0a6cd931c64a8173d9a5f6dfc0ab49f9d20820876009a17f97dd1', 'John', 'Steven', 0, 'static/Image/user_uploads/policy-2025-04-09-john545.png'); -- password: admin

INSERT INTO users (username, password, first_name, last_name, is_admin)
VALUES
('admin', 'scrypt:32768:8:1$XX4iX48LUzwzHRST$b51014d60219704eccda5766b47dc760430333aa17e8848da5650f52e4427b71c6bbf2cb4ba0a6cd931c64a8173d9a5f6dfc0ab49f9d20820876009a17f97dd1', 'Admin', 'Control', 1); -- password: admin

INSERT INTO policyTypes VALUES ('aFRESH', 'Fresher Plan', 'Covers Theft Protection', 50);
INSERT INTO policyTypes VALUES ('bPERS', 'Personal Plan', 'Covers Theft Protection and Screen Damage Protection', 200);
INSERT INTO policyTypes VALUES ('cBUS', 'Business Plan', 'Covers Theft Protection, Screen Damage Protection and Water Damge Protection', 700);
INSERT INTO policyTypes VALUES ('dPLAT', 'Platinum Plan', 'Covers Theft Protection, Screen Damage Protection, Water Damge Protection and Phone Upgrade Costs', 1000);


INSERT INTO policies VALUES ('e6b4e44d-6838-4f44-bab8-03f2a075709b', 100, 'iPhone 13', 'Business Plan', 'Yes', 'Yes', 'No',
    (SELECT username FROM users WHERE username = 'john545'),
    (SELECT policy_type_id FROM policyTypes WHERE policy_type_id='cBUS'), 'static/Image/user_uploads/policy-2025-04-09-john545.png');


INSERT INTO claims (claim_id, status, reason, admin_comment, date_of_incident, username, policy_id, claim_amount, amount_approved)
VALUES ('e50ce2f4-a338-43c9-b09c-84525bc16929', 'Pending', 'broke my phone', '', '2025-03-15',
    (SELECT username FROM users WHERE username = 'e6b4e44d-6838-4f44-bab8-03f2a075709b'),
    (SELECT policy_id FROM policies WHERE policy_id='123'), 10000, 6000);

SELECT * FROM users;
SELECT * FROM policies;
SELECT * FROM usersToContact;
SELECT * FROM claims;
SELECT * FROM policyTypes;
