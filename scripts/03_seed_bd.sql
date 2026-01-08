USE sam_db;

INSERT INTO roles (title, created_at)
VALUES
    ('GUEST', NOW()),
    ('CLIENT', NOW()),
    ('ADMIN', NOW());

-- the password is: passe
INSERT INTO users (email, password, created_at)
VALUES
    ('guest1@test.com', '$argon2id$v=19$m=65536,t=3,p=2$ZWsL2lgAb3immpS2hgowmQ$vZnZnUSk47cyEfb89PuxEPd+elRoFG6sjao2Tri3fJs', NOW()),
    ('guest2@test.com', '$argon2id$v=19$m=65536,t=3,p=2$ZWsL2lgAb3immpS2hgowmQ$vZnZnUSk47cyEfb89PuxEPd+elRoFG6sjao2Tri3fJs', NOW()),
    ('client1@test.com', '$argon2id$v=19$m=65536,t=3,p=2$ZWsL2lgAb3immpS2hgowmQ$vZnZnUSk47cyEfb89PuxEPd+elRoFG6sjao2Tri3fJs', NOW()),
    ('client2@test.com', '$argon2id$v=19$m=65536,t=3,p=2$ZWsL2lgAb3immpS2hgowmQ$vZnZnUSk47cyEfb89PuxEPd+elRoFG6sjao2Tri3fJs', NOW()),
    ('admin@test.com', '$argon2id$v=19$m=65536,t=3,p=2$ZWsL2lgAb3immpS2hgowmQ$vZnZnUSk47cyEfb89PuxEPd+elRoFG6sjao2Tri3fJs', NOW());


INSERT INTO user_role (user_id, role_id)
VALUES
    (1, 1), -- guest1 -> GUEST
    (2, 1), -- guest2 -> GUEST
    (3, 2), -- client1 -> CLIENT
    (4, 2), -- client2 -> CLIENT
    (5, 3); -- admin -> ADMIN