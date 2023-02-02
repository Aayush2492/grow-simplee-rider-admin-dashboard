CREATE TABLE location
(
    loc_id      BIGSERIAL   NOT NULL,
    latitude    FLOAT       NOT NULL,
    longitude   FLOAT       NOT NULL,
    PRIMARY KEY (loc_id),
    UNIQUE      (latitude, longitude)
);

CREATE TABLE rider
(
    rider_id    BIGSERIAL   NOT NULL,
    name        VARCHAR(50) NOT NULL,
    contact     DECIMAL     NOT NULL,
    PRIMARY KEY (rider_id),
    UNIQUE      (contact)
);

CREATE TABLE bag
(
    bag_id      BIGSERIAL   NOT NULL,
    type        BOOL        NOT NULL,
    PRIMARY KEY (bag_id)
);

CREATE TABLE package
(
    object_id       BIGSERIAL   NOT NULL,
    weight          FLOAT       NOT NULL,
    length          FLOAT,
    breadth         FLOAT,
    height          FLOAT,
    delivery_date   TIMESTAMP    NOT NULL,
    delivery_loc    BIGINT      NOT NULL,
    erroneous       BOOL        NOT NULL    DEFAULT true,
    comments        VARCHAR(200),
    type            BOOL        NOT NULL,
    completed       BOOL        NOT NULL    DEFAULT false,
    PRIMARY KEY (object_id),
    FOREIGN KEY (delivery_loc)  REFERENCES location(loc_id)
);

CREATE TABLE tour
(
    tour_id             BIGSERIAL   NOT NULL,
    assigned_rider      BIGINT      NOT NULL,
    assigned_bag        BIGINT      NOT NULL,
    delivery            BIGINT[]    NOT NULL,
    delivery_order      INT[]       NOT NULL,
    PRIMARY KEY (tour_id),
    FOREIGN KEY (assigned_rider)            REFERENCES rider(rider_id), 
    FOREIGN KEY (assigned_bag)              REFERENCES bag(bag_id)
);