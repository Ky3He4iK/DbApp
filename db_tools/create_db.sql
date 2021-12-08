drop database plate_manufacturing;
create database plate_manufacturing;

use plate_manufacturing;
CREATE TABLE Worker
(
    WorkerId INTEGER     NOT NULL,
    Name     VARCHAR(63) NOT NULL,
    Status   VARCHAR(63) NOT NULL,
    PRIMARY KEY (WorkerId)
);
CREATE TABLE ZoneInfo
(
    ZoneId      INTEGER      NOT NULL,
    Status      VARCHAR(63)  NOT NULL,
    Location    VARCHAR(31)  NOT NULL,
    Description VARCHAR(255) NOT NULL,
    PRIMARY KEY (ZoneId)
);
CREATE TABLE Machine
(
    MachineId INTEGER     NOT NULL,
    Name      VARCHAR(63) NOT NULL,
    Status    VARCHAR(15) NOT NULL,
    ZoneId    INTEGER     NOT NULL,
    WorkerId  INTEGER     NULL,
    PRIMARY KEY (MachineId),
    FOREIGN KEY R_15 (ZoneId) REFERENCES ZoneInfo (ZoneId),
    FOREIGN KEY R_16 (WorkerId) REFERENCES Worker (WorkerId)
);
CREATE TABLE Customer
(
    CustomerId     INTEGER      NOT NULL,
    AdditionalInfo VARCHAR(255) NULL,
    Mail           VARCHAR(63)  NOT NULL,
    Phone          NUMERIC(11)  NOT NULL,
    PRIMARY KEY (CustomerId)
);
CREATE TABLE OrderInfo
(
    OrderId         INTEGER      NOT NULL,
    CustomerId      INTEGER      NOT NULL,
    DeliveryAddress VARCHAR(255) NOT NULL,
    Price           INTEGER      NOT NULL,
    Status          VARCHAR(31)  NOT NULL,
    PlateCount      INTEGER      NOT NULL,
    Notes           VARCHAR(511) NULL,
    PRIMARY KEY (OrderId),
    FOREIGN KEY R_13 (CustomerId) REFERENCES Customer (CustomerId)
);
CREATE TABLE FactManufactoring
(
    OrderId        INTEGER   NOT NULL UNIQUE,
    AcceptedPlates INTEGER   NOT NULL,
    RejectedPlates INTEGER   NOT NULL,
    StartTime      TIMESTAMP NOT NULL,
    EndTime        TIMESTAMP NOT NULL,
    FactId         INTEGER   NOT NULL,
    PRIMARY KEY (FactId),
    FOREIGN KEY R_4 (OrderId) REFERENCES OrderInfo (OrderId)
);
CREATE TABLE PlateStorage
(
    OrderId       INTEGER NOT NULL,
    PlateId       INTEGER NOT NULL,
    NumberInOrder INTEGER NOT NULL,
    PRIMARY KEY (PlateId, OrderId),
    FOREIGN KEY R_3 (OrderId) REFERENCES OrderInfo (OrderId)
);
CREATE TABLE PlateStatus
(
    PlateId             INTEGER     NOT NULL,
    InstalledComponents INTEGER     NOT NULL,
    Status              VARCHAR(31) NOT NULL,
    OrderId             INTEGER     NOT NULL,
    MachineId           INTEGER     NULL,
    PRIMARY KEY (OrderId, PlateId),
    FOREIGN KEY R_5 (PlateId, OrderId) REFERENCES PlateStorage (PlateId, OrderId),
    FOREIGN KEY R_17 (MachineId) REFERENCES Machine (MachineId)
);
CREATE TABLE Components
(
    ComponentId INTEGER      NOT NULL,
    Count       INTEGER      NOT NULL,
    Name        VARCHAR(127) NOT NULL,
    PRIMARY KEY (ComponentId)
);
CREATE TABLE PlateConfiguration
(
    PlateId   INTEGER     NOT NULL,
    Height    INTEGER     NOT NULL,
    Width     INTEGER     NOT NULL,
    Layers    INTEGER     NOT NULL,
    Material  VARCHAR(31) NOT NULL,
    Thickness FLOAT       NOT NULL,
    OrderId   INTEGER     NOT NULL,
    PRIMARY KEY (OrderId, PlateId),
    FOREIGN KEY R_7 (PlateId, OrderId) REFERENCES PlateStorage (PlateId, OrderId)
);

CREATE TABLE ComponentInfo
(
    InstalledOrder INTEGER NOT NULL,
    posX           FLOAT   NOT NULL,
    posY           FLOAT   NOT NULL,
    PlateId        INTEGER NOT NULL,
    OrderId        INTEGER NOT NULL,
    ComponentId    INTEGER NOT NULL,
    PRIMARY KEY (PlateId, OrderId, InstalledOrder),
    FOREIGN KEY R_6 (PlateId, OrderId) REFERENCES PlateStorage (PlateId, OrderId),
    FOREIGN KEY R_14 (ComponentId) REFERENCES Components (ComponentId)
);

CREATE TRIGGER insert_order_plates
    after INSERT
    on OrderInfo
    FOR EACH ROW
begin
    CALL add_plates(NEW.OrderId, NEW.PlateCount);
end;

CREATE TRIGGER update_order_plates
    after UPDATE
    on OrderInfo
    FOR EACH ROW
begin
    DECLARE diff INT Default NEW.PlateCount - OLD.PlateCount;
    IF diff > 0 AND NEW.OrderId = OLD.OrderId THEN
        CALL add_plates(NEW.OrderId, diff);
    end if;
end;

DELIMITER $$
CREATE PROCEDURE add_plates(
    IN OrderId INTEGER,
    IN Count INTEGER
)
BEGIN
    DECLARE i INT Default 0;
    DECLARE PlateIdStart INT Default 0;
    DECLARE PlateNumberStart INT Default 0;

    SELECT IFNULL(MAX(PlateId), 0) FROM PlateStorage PL WHERE PL.OrderId = OrderId into PlateIdStart;
    SELECT IFNULL(MAX(NumberInOrder), 0) FROM PlateStorage PL WHERE PL.OrderId = OrderId INTO PlateNumberStart;

    simple_loop:
    LOOP
        SET i = i + 1;
        select i into i;
        IF i > Count THEN
            LEAVE simple_loop;
        END IF;
        INSERT INTO PlateStorage VALUE (OrderId, PlateIdStart + i, PlateNumberStart + i);
        INSERT INTO PlateStatus VALUE (PlateIdStart + i, 0, 'Preparing', OrderId, NULL);
        INSERT INTO PlateConfiguration VALUE (PlateIdStart + i, 0, 1, 0, 'Default', 0, OrderId);
    END LOOP simple_loop;
END;
$$

CREATE OR REPLACE VIEW plates_dashboard AS
SELECT OI.OrderId,
       Status,
       Notes,
       DeliveryAddress,
       Phone,
       AdditionalInfo,
       StartTime,
       EndTime
FROM OrderInfo OI
         LEFT JOIN FactManufactoring FM on OI.OrderId = FM.OrderId
         LEFT JOIN Customer C on C.CustomerId = OI.CustomerId
WHERE Status != 'Done';
