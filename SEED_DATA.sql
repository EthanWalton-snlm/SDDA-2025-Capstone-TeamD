CREATE TABLE policies (
    policy_id NVARCHAR(50) PRIMARY KEY,
    premium FLOAT,
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (policy_type_id) REFERENCES policyTypes(policy_type_id)
);

CREATE TABLE users (
    username NVARCHAR(100) PRIMARY KEY,
    password NVARCHAR(255),
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

CREATE TABLE claims (
    claim_id NVARCHAR(50) PRIMARY KEY,
    status NVARCHAR(25),
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);

INSERT INTO users (username, password, first_name, last_name, is_admin)
VALUES
('admin', 'admin', 'Admin', 'Account', 1);
