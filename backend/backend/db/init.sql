CREATE TABLE location
(
    loc_id      BIGSERIAL   NOT NULL,
    latitude    FLOAT       NOT NULL,
    longitude   FLOAT       NOT NULL,
    address     VARCHAR(1024)   DEFAULT 'Address',
    PRIMARY KEY (loc_id),
    UNIQUE      (latitude, longitude, address)
);

CREATE TABLE rider
(
    rider_id    BIGSERIAL   NOT NULL,
    name        VARCHAR(50) NOT NULL DEFAULT 'Rider',
    contact     DECIMAL     NOT NULL DEFAULT 0,
	latitude    FLOAT,
	longitude   FLOAT,
    PRIMARY KEY (rider_id),
    UNIQUE      (contact)
);

CREATE TABLE bag
(
    bag_id      BIGSERIAL   NOT NULL,
    bag_type    BOOL        NOT NULL,
    PRIMARY KEY (bag_id)
);

CREATE TABLE package
(
    object_id       BIGSERIAL   NOT NULL,
    weight          FLOAT       NOT NULL,
    length          FLOAT,
    breadth         FLOAT,
    height          FLOAT,
    delivery_date   TIMESTAMP   NOT NULL,
    delivered_time  TIMESTAMP,   
    delivery_loc    BIGINT      NOT NULL,
    erroneous       BOOL        NOT NULL    DEFAULT true,
    comments        VARCHAR(200),
    obj_type        BOOL        NOT NULL,
    completed       BOOL        NOT NULL    DEFAULT false,
    PRIMARY KEY (object_id),
    FOREIGN KEY (delivery_loc)  REFERENCES location(loc_id)
);

CREATE TABLE tour
(
    tour_id             BIGSERIAL   NOT NULL,
    assigned_rider      BIGINT      NOT NULL,
    assigned_bag        BIGINT      NOT NULL,
    tour_status         INT         NOT NULL,
    PRIMARY KEY (tour_id),
    FOREIGN KEY (assigned_rider)    REFERENCES rider(rider_id), 
    FOREIGN KEY (assigned_bag)      REFERENCES bag(bag_id)
);

CREATE TABLE delivery
(
    id              BIGINT      NOT NULL,
    item            BIGINT      NOT NULL,
    delivery_order  INT         NOT NULL,
    FOREIGN KEY     (item)      REFERENCES package(object_id),
    FOREIGN KEY     (id)        REFERENCES tour(tour_id)
);

CREATE TABLE addresses
(
    id              BIGINT      NOT NULL,
    address VARCHAR(100)
);
