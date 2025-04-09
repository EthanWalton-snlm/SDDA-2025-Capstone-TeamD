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

-- Add constraint to set default submission_date to current date/time when claim is created
-- ALTER TABLE claims
-- ADD CONSTRAINT DF_Claims_SubmissionDate DEFAULT (GETDATE()) FOR submission_date;

INSERT INTO users (username, password, first_name, last_name, is_admin)
VALUES
('admin', 'scrypt:32768:8:1$4Ce2JLFzCwuMqtsi$a804f8cda8d67c01dfabd8837936899f3bf80c433577b922dbb9f27997683d1b76d7698e992827118d5bea047495c5e249a39c1d894c266d6bfd133319c25eb1', 'Admin', 'Account', 1);

INSERT INTO policyTypes VALUES ('aFRESH', 'Fresher Plan', 'Covers Theft Protection', 50);
INSERT INTO policyTypes VALUES ('bPERS', 'Personal Plan', 'Covers Theft Protection and Screen Damage Protection', 200);
INSERT INTO policyTypes VALUES ('cBUS', 'Business Plan', 'Covers Theft Protection, Screen Damage Protection and Water Damge Protection', 700);
INSERT INTO policyTypes VALUES ('dPLAT', 'Platinum Plan', 'Covers Theft Protection, Screen Damage Protection, Water Damge Protection and Phone Upgrade Costs', 1000);


INSERT INTO policies VALUES ('123', 100, 'iPhone 13', 'Business Plan', 'Yes', 'Yes', 'No',
    (SELECT username FROM users WHERE username = 'admin'),
    (SELECT policy_type_id FROM policyTypes WHERE policy_type_id='BPLAN'), 'test.jpg');

INSERT INTO claims (claim_id, status, reason, admin_comment, date_of_incident, username, policy_id)
VALUES ('claim1', 'Pending', 'broke my phone', '', '2025-03-15',
    (SELECT username FROM users WHERE username = 'admin'),
    (SELECT policy_id FROM policies WHERE policy_id='123'), 10000, 6000);

SELECT * FROM users;
SELECT * FROM usersToContact;
SELECT * FROM claims;
SELECT * FROM policyTypes;

SELECT * FROM policies;
