SELECT 
    fc.Sucursal,
    fc.Tipo AS Doc,
    CONCAT(LPAD(CONVERT(fc.PuntoVta, CHAR), 4, '0'), '-', LPAD(CONVERT(fc.Numero, CHAR), 8, '0')) AS Documento,
    fc.Emision AS Fecha,
    fc.Hora AS Hora,
    op.Codigo AS Usuario,
    
    -- Efectivo
    SUM(
        COALESCE(
            (SELECT IF(fc.Tipo = 'NC', Importe * -1, Importe)
             FROM factpagos
             WHERE IDComprobante = fc.IDComprobante AND idmediodepago IN (1)), 
        0)
    ) AS Efectivo,
    
    -- Cuenta Corriente
    SUM(
        COALESCE(
            (SELECT SUM(ImporteCtaCte)
             FROM factlineas
             WHERE IDComprobante = fc.IDComprobante), 
        0)
    ) AS CtaCte,
    
    -- Obra Social
    IF(fc.Tipo = 'NC', fc.TotalCobertura * -1, fc.TotalCobertura) AS OSocial,
    (SELECT obsociales.Descripcio
     FROM factcoberturas, obsociales
     WHERE factcoberturas.IDObSoc = obsociales.CodObSoc
       AND factcoberturas.IDComprobante = fc.IDComprobante
     LIMIT 1) AS Obra Social Detalle,
    
    -- Tarjetas
    SUM(
        COALESCE(
            (SELECT SUM(IF(fc.Tipo = 'NC', Importe * -1, Importe))
             FROM factpagos
             WHERE IDComprobante = fc.IDComprobante AND idmediodepago IN (3, 5)), 
        0)
    ) AS Tarjeta,
    
    -- Otros Medios de Pago
    SUM(
        COALESCE(
            (SELECT SUM(IF(fc.Tipo = 'NC', Importe * -1, Importe))
             FROM factpagos
             WHERE IDComprobante = fc.IDComprobante AND idmediodepago NOT IN (1, 3, 5)), 
        0)
    ) AS OtrosMP,
    
    -- Detalle de Tarjeta
    (SELECT tarjetas.tarjeta
     FROM factpagos, tarjetas
     WHERE factpagos.IDTarjeta = tarjetas.IDTarjeta
       AND factpagos.IDComprobante = fc.IDComprobante
     LIMIT 1) AS Tarjeta Detalle,
    
    -- Total Comprobante
    IF(fc.Tipo = 'NC', fc.TotalComprobante * -1, fc.TotalComprobante) AS Total,
    
    -- Cliente
    c.Nombre AS Apellido y nombre/Razón Social,
    c.Documento AS DNI,
    c.Cuit AS CUIT

FROM factcabecera fc
LEFT JOIN clientes c ON fc.IDCliente = c.CodCliente
INNER JOIN Operadores op ON fc.IDUsuario = op.IDOperador

WHERE 
    fc.Emision BETWEEN %s AND %s
    AND fc.Tipo IN ('FV', 'TK', 'TF', 'NC', 'ND', 'TZ')
    AND fc.TipoIVA <> 'XX'

GROUP BY 
    fc.Tipo, fc.PuntoVta, fc.Numero

ORDER BY 
    fc.Emision, fc.Tipo, fc.PuntoVta, fc.Numero;
