-- Drop existing tables

DROP TABLE IF EXISTS claims;
DROP TABLE IF EXISTS policies;
DROP TABLE IF EXISTS policyTypes;
DROP TABLE IF EXISTS usersToContact;
DROP TABLE IF EXISTS users;


-- Create tables

CREATE TABLE users (
    username NVARCHAR(100) PRIMARY KEY,
    password NVARCHAR(500),
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    email NVARCHAR(50),
    phone_number NVARCHAR(13),
    id_number NVARCHAR(13),
    is_admin INT DEFAULT 0, -- 1 = True
    profile_pic NVARCHAR(500),

	claims_made INT DEFAULT 0,
	claims_approved INT DEFAULT 0,
	claims_rejected INT DEFAULT 0,
	claims_pending INT DEFAULT 0
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
    phone_case INT,
    screen_protector INT,
    waterproof_phone INT,
    username NVARCHAR(100) REFERENCES users(username),
    policy_type_id NVARCHAR(50) REFERENCES policyTypes(policy_type_id),
    image_link NVARCHAR(500) NULL
);

CREATE TABLE claims (
    claim_id NVARCHAR(50) PRIMARY KEY,
    status NVARCHAR(25),
    reason NVARCHAR(500),
    admin_comment NVARCHAR(500),
    affidavit_link NVARCHAR(500),
    image_link NVARCHAR(500),
    quotation_link NVARCHAR(500),
    approved_by NVARCHAR(100),  -- column to store the admin who approved the claim
    rejected_by NVARCHAR(100),  -- column to store the admin who rejected the claim
    submission_date DATETIME NOT NULL DEFAULT GETDATE(), -- date when claim is submitted
    date_of_incident DATE NOT NULL, -- date when the incident happened
    username NVARCHAR(100) REFERENCES users(username),
    policy_id NVARCHAR(50) REFERENCES policies(policy_id),
	claim_amount FLOAT,
	amount_approved FLOAT
);


-- Insert Dummy Users

INSERT INTO users (username, password, first_name, last_name, is_admin, profile_pic)
VALUES
('admin', 'scrypt:32768:8:1$4Ce2JLFzCwuMqtsi$a804f8cda8d67c01dfabd8837936899f3bf80c433577b922dbb9f27997683d1b76d7698e992827118d5bea047495c5e249a39c1d894c266d6bfd133319c25eb1', 'Admin', 'Account', 1, 'static/Image/user_uploads/admin-pfp.jpg');

INSERT INTO users (username, password, first_name, last_name, is_admin, profile_pic, email, phone_number, id_number, claims_made, claims_pending)
VALUES
('john545',
'scrypt:32768:8:1$4Ce2JLFzCwuMqtsi$a804f8cda8d67c01dfabd8837936899f3bf80c433577b922dbb9f27997683d1b76d7698e992827118d5bea047495c5e249a39c1d894c266d6bfd133319c25eb1',
'John', 'Steven', 0, 'static/Image/user_uploads/policy-2025-04-09-john545.png', 'john@steve.com', '0713457593', '9908356789589', 1, 1);


-- Insert Dummy Policy Types

INSERT INTO policyTypes VALUES ('aFRESH', 'Fresher Plan', 'Covers Theft Protection', 50);
INSERT INTO policyTypes VALUES ('bPERS', 'Personal Plan', 'Covers Theft Protection and Screen Damage Protection', 200);
INSERT INTO policyTypes VALUES ('cBUS', 'Business Plan', 'Covers Theft Protection, Screen Damage Protection and Water Damge Protection', 700);
INSERT INTO policyTypes VALUES ('dPLAT', 'Platinum Plan', 'Covers Theft Protection, Screen Damage Protection, Water Damge Protection and Phone Upgrade Costs', 1000);


-- Insert Dummy Policies

INSERT INTO policies VALUES ('df781ac6-b6ca-40ff-921b-330e78d41ab2', 100, 'iPhone 13', 'Business Plan', 1, 1, 0,
    (SELECT username FROM users WHERE username = 'john545'),
    (SELECT policy_type_id FROM policyTypes WHERE policy_type_id='bPERS'), 'static/Image/user_uploads/policy-2025-04-09-john545.png');


-- Insert Dummy Claims

INSERT INTO claims (claim_id, status, reason, admin_comment, date_of_incident, username, policy_id, claim_amount, affidavit_link, quotation_link, image_link)
VALUES ('ab1d9cc8-4531-46ac-9177-1053bac4b419', 'Pending', 'I dropped my phone.', '', '2025-04-01',
    (SELECT username FROM users WHERE username = 'john545'),
    (SELECT policy_id FROM policies WHERE policy_id='df781ac6-b6ca-40ff-921b-330e78d41ab2'), 10000, 'https://docs.google.com/document/d/1GiFhnbCby9gl3ZLHVGGRCxTy225CUEalv6RGjIzksjw/edit?usp=sharing', 'https://docs.google.com/document/d/1LqAU_adI2F6owms8HqOjvrVD4F4Qp-8WfuJ2qTd1SBY/edit?usp=sharing', 'https://www.gizchina.com/wp-content/uploads/images/2021/09/iPhone-13-Pro-a.jpg');


-- View Data

SELECT * FROM users;
SELECT * FROM usersToContact;
SELECT * FROM claims;
SELECT * FROM policyTypes;
SELECT * FROM policies;
