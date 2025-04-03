CREATE TABLE users (
    username NVARCHAR(100) PRIMARY KEY,
    password NVARCHAR(500),
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
ADD phone_name NVARCHAR(50);

ALTER TABLE policies
ADD policy_name NVARCHAR(50);

ALTER TABLE policies
ADD phone_case NVARCHAR(50);

ALTER TABLE policies
ADD screen_protector NVARCHAR(50);

ALTER TABLE policies
ADD waterproof_phone NVARCHAR(50);


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
ADD policy_id NVARCHAR(50)
REFERENCES policies(policy_id);



INSERT INTO policies VALUES ('123', 100, (SELECT username FROM users WHERE username = 'admin'), (SELECT policy_type_id FROM PolicyTypes WHERE policy_type_id='BPLAN'));


INSERT INTO claims (claim_id, status, reason, username, policy_id)
VALUES ('claim1', 'Pending', 'broke my phone', (SELECT username FROM users WHERE username = 'admin'), (SELECT policy_id FROM policies WHERE policy_id='123'));


INSERT INTO users (username, password, first_name, last_name, is_admin)
VALUES
('admin', 'admin', 'Admin', 'Account', 1);


INSERT INTO policyTypes VALUES ('BPLAN', 'Business Plan', 'For business people');

SELECT * FROM users;
select * from policies;
