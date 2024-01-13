-- Employees tablosu
CREATE TABLE Employees (
    CalisanID INT PRIMARY KEY IDENTITY(1,1),
    Ad NVARCHAR(50) NOT NULL,
    Soyad NVARCHAR(50) NOT NULL,
    Pozisyon NVARCHAR(50)
);