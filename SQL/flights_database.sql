CREATE database flights_db;
USE flights_db;

DROP TABLE IF EXISTS class_name;

CREATE TABLE class_name (
    class_id int PRIMARY KEY,
    class_name VARCHAR(255)
);

DROP TABLE IF EXISTS flight_number;

CREATE TABLE flight_number (
    flight_number_id int PRIMARY KEY,
    flight_number VARCHAR(255)
);

DROP TABLE IF EXISTS airline;

CREATE TABLE airline (
    airline_name_id int PRIMARY KEY,
    airline_name VARCHAR(255)
);

DROP TABLE IF EXISTS origin;

CREATE TABLE origin (
    origin_id int PRIMARY KEY,
    origin VARCHAR(255)
);

DROP TABLE IF EXISTS destination;

CREATE TABLE destination (
    destination_id int PRIMARY KEY,
    destination VARCHAR(255)
);

DROP TABLE IF EXISTS stops;

CREATE TABLE stops (
    stops_id int PRIMARY KEY,
    stops VARCHAR(255)
);

DROP TABLE IF EXISTS itinerary;

CREATE TABLE itinerary (
    itinerary_id int PRIMARY KEY,
    origin_id int NOT NULL,
    destination_id int NOT NULL,
    CONSTRAINT fk_origin
        FOREIGN KEY (origin_id) REFERENCES origin(origin_id),
    CONSTRAINT fk_destination
        FOREIGN KEY (destination_id) REFERENCES destination(destination_id)
);

DROP TABLE IF EXISTS ticket;

CREATE TABLE ticket (
    ticket_id int PRIMARY KEY,
    price DECIMAL(10,2),
    class_id int NOT NULL,
    flight_number_id int NOT NULL,
    airline_name_id int NOT NULL,
    CONSTRAINT fk_class
        FOREIGN KEY (class_id) REFERENCES class_name(class_id),
    CONSTRAINT fk_flight_number
        FOREIGN KEY (flight_number_id) REFERENCES flight_number(flight_number_id),
	CONSTRAINT fk_airline_name
        FOREIGN KEY (airline_name_id) REFERENCES airline(airline_name_id)
);

DROP TABLE IF EXISTS schedule;

CREATE TABLE schedule (
    schedule_id int PRIMARY KEY,
    arrival_time TIME,
    departure_time TIME,
    duration TIME,
    stops_id int NOT NULL,
    CONSTRAINT fk_stops
        FOREIGN KEY (stops_id) REFERENCES stops(stops_id)
);

DROP TABLE IF EXISTS flight;

CREATE TABLE flight (
    flight_id int PRIMARY KEY,
    ticket_id int NOT NULL,
    schedule_id int NOT NULL,
    itinerary_id int NOT NULL,
    CONSTRAINT fk_ticket
        FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id),
    CONSTRAINT fk_schedule
        FOREIGN KEY (schedule_id) REFERENCES schedule(schedule_id),
	CONSTRAINT fk_itinerary
        FOREIGN KEY (itinerary_id) REFERENCES itinerary(itinerary_id)
);