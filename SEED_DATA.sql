CREATE TABLE users (
    username NVARCHAR(100) PRIMARY KEY,
    password NVARCHAR(50),
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    email NVARCHAR(50),
    phone_number NVARCHAR(13),
    id_number NVARCHAR(13),
    is_admin INT DEFAULT 0 -- 1 = True
);


CREATE TABLE policyTypes (
    policy_type_id NVARCHAR(50) PRIMARY KEY,
    name NVARCHAR(100),
    summary NVARCHAR(500)
);


CREATE TABLE policies (
    policy_id NVARCHAR(50) PRIMARY KEY,
    premium FLOAT,
);

ALTER TABLE policies
ADD username NVARCHAR(100)
REFERENCES users(username);

ALTER TABLE policies
ADD policy_type_id NVARCHAR(50)
REFERENCES policyTypes(policy_type_id);


CREATE TABLE claims (
    claim_id NVARCHAR(50) PRIMARY KEY,
    status NVARCHAR(25),
    reason NVARCHAR(500),
	admin_comment NVARCHAR(500)
);

ALTER TABLE claims
ADD username NVARCHAR(100)
REFERENCES users(username);

ALTER TABLE claims
ADD policy_type_id NVARCHAR(50)
REFERENCES policyTypes(policy_type_id);



INSERT INTO claims (claim_id, status, reason, username, policy_id)
VALUES ('claim1', 'pending', 'broke my phone', (SELECT username FROM users WHERE username = 'wewe'), (SELECT policy_type_id FROM PolicyTypes WHERE policy_type_id='BPLAN'));


INSERT INTO users (username, password, first_name, last_name, is_admin)
VALUES
('admin', 'admin', 'Admin', 'Account', 1);


INSERT INTO policyTypes VALUES ('BPLAN', 'Business Plan', 'For business people')


INSERT INTO claims SET username = (SELECT 1 FROM users), policy_id = (SELECT 1 FROM PolicyTypes);
