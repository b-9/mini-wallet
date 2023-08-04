
## wallets
CREATE TABLE wallets(
id VARCHAR(50) UNIQUE NOT NULL ,
balance NUMERIC,
token VARCHAR(50) UNIQUE NOT NULL,
customer_id VARCHAR(50) UNIQUE NOT NULL,
status VARCHAR(10) NOT NULL default 'disabled',
created_at timestamp without time zone NOT NULL,
enabled_at timestamp without time zone,
updated_at timestamp without time zone
 
);

## transactions
create table transactions(
id VARCHAR(50) UNIQUE NOT NULL,
wallet_id VARCHAR(50) NOT NULL,
created_at timestamp without time zone NOT NULL,
type VARCHAR(12) NOT NULL,
reference_id VARCHAR(50) NOT NULL,
status varchar(10) not null,
amount NUMERIC,
UNIQUE(type,reference_id),
CONSTRAINT fk_wallet
      FOREIGN KEY(wallet_id) 
	  REFERENCES wallets(id)
);