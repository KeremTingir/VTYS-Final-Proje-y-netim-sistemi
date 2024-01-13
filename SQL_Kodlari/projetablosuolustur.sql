-- Projects tablosu
CREATE TABLE Projects (
    ProjeID INT PRIMARY KEY IDENTITY(1,1),
    ProjeAdi NVARCHAR(255) NOT NULL,
    BaslangicTarihi DATE,
    BitisTarihi DATE
);