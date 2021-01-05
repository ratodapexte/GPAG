CREATE TABLE address (
  id bigserial PRIMARY KEY,
  street varchar(255) NOT NULL,
  house_number int NOT NULL,
  district varchar(255) NOT NULL,
  city varchar(255) NOT NULL,
  estate varchar(255) NOT NULL,
  zipcode varchar(255) NOT NULL
);
CREATE TABLE users (
  id bigserial PRIMARY KEY,
  name varchar(255) NOT NULL,
  username varchar(255) NOT NULL UNIQUE,
  password varchar(255) NOT NULL,
  cpf varchar(255) NOT NULL UNIQUE,
  email varchar(255) NOT NULL UNIQUE,
  phone varchar(255),
  adm boolean DEFAULT 'f',
  employee boolean DEFAULT 'f',
  auth_key text UNIQUE,
  auth_key_init_datetime TIMESTAMP
);
CREATE TABLE bills (
  id bigserial PRIMARY KEY,
  payment NUMERIC NOT NULL,
  registration_date date DEFAULT cast(now() as date),
  due_date date NOT NULL,
  fk_employee_id int REFERENCES users(id),
  payment_authentication_key text UNIQUE,
  fk_user_id int REFERENCES users(id),
  validated boolean DEFAULT 'f'
);
INSERT INTO public.users(
	name, username, password, cpf, email, phone, adm, employee)
	VALUES ('admin', 'admin', 'admin', 0000000000, 'admin@admin', 000000000, true, true);
INSERT INTO public.users(
	name, username, password, cpf, email, phone, adm, employee)
	VALUES ('cliente', 'cliente', 'cliente', 11111111111, 'admin@admin', 111111111, true, true);