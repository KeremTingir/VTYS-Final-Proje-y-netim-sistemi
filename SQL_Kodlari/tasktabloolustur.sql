-- Tasks tablosu
CREATE TABLE Tasks (
    GorevID INT PRIMARY KEY IDENTITY(1,1),
    ProjeID INT,
    CalisanID INT,
    BaslangicTarihi DATE,
    AdamGunDegeri INT,
    BitisTarihi DATE,
    DurumID INT,
    FOREIGN KEY (ProjeID) REFERENCES Projects(ProjeID),
    FOREIGN KEY (CalisanID) REFERENCES Employees(CalisanID),
    FOREIGN KEY (DurumID) REFERENCES TaskStatus(DurumID)
);