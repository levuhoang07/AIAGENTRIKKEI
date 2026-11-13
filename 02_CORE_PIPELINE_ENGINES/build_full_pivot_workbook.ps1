$ErrorActionPreference = "Stop"

try {
    Write-Host "Starting Excel Application via COM..."
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    
    $workspaceRoot = (Resolve-Path "$PSScriptRoot\..").Path
    $rawPath = Join-Path $workspaceRoot 'AI301_De04_Master_1000_Leads.xlsx'
    $finalPath = Join-Path $workspaceRoot 'AI301_De04_Du_Lieu_Mau_1000_Leads_Cleaned.xlsx'
    
    $wb = $excel.Workbooks.Open($rawPath)
    Write-Host "Opened workbook: $($wb.Name)"
    
    # 1. Sheet Dữ liệu nguồn
    $srcSheet = $wb.Sheets.Item(1)
    $srcSheet.Name = "Dữ liệu nguồn "
    $lastRow = $srcSheet.UsedRange.Rows.Count
    $lastCol = $srcSheet.UsedRange.Columns.Count
    Write-Host "Source data: $lastRow rows, $lastCol cols"
    
    # Font Aptos Narrow or Segoe UI
    $srcSheet.Range("A1").Resize($lastRow, $lastCol).Font.Name = "Segoe UI"
    $srcSheet.Range("A1").Resize($lastRow, $lastCol).Font.Size = 10
    
    # Header format
    $headerRange = $srcSheet.Range("A1").Resize(1, $lastCol)
    $headerRange.Font.Bold = $true
    $headerRange.Font.Color = 0xFFFFFF # White
    $headerRange.Interior.Color = 0x5D361B # Deep Navy (BGR: 1B 36 5D -> 0x5D361B)
    $headerRange.RowHeight = 28
    
    # Currency formatting: Col 9 (Doanh thu), Col 12 (Ngân sách)
    $vndFmt = '_-* #,##0\ [$₫-42A]_-;\-* #,##0\ [$₫-42A]_-;_-* "-"\\ [$₫-42A]_-;_-@_-'
    $srcSheet.Range("I2").Resize($lastRow - 1, 1).NumberFormat = $vndFmt
    $srcSheet.Range("L2").Resize($lastRow - 1, 1).NumberFormat = $vndFmt
    # Integer format: Col 7 (Cửa hàng), Col 8 (Kho)
    $srcSheet.Range("G2").Resize($lastRow - 1, 2).NumberFormat = "#,##0"
    
    # Convert to Excel Table (ListObject) Table1
    $dataRange = $srcSheet.Range("A1").Resize($lastRow, $lastCol)
    try {
        $tbl = $srcSheet.ListObjects.Add(1, $dataRange, [Type]::Missing, 1) # xlSrcRange = 1, xlYes = 1
        $tbl.Name = "Table1"
        $tbl.TableStyle = "TableStyleLight1"
        Write-Host "Converted source data to Excel Table 'Table1'."
    } catch {
        Write-Host "Table1 note: $($_.Exception.Message)"
    }
    
    # Create Unified PivotCache (xlDatabase = 1)
    # Using Table1 Range
    $pivotCache = $wb.PivotCaches().Create(1, $srcSheet.Range("A1").Resize($lastRow, $lastCol), 5) # 5 = xlPivotTableVersion15
    Write-Host "Created PivotCache successfully."

    # -----------------------------------------------------------------
    # Function to create clean sheet
    # -----------------------------------------------------------------
    function Add-CleanSheet($name) {
        try {
            $existing = $wb.Sheets.Item($name)
            $existing.Delete()
        } catch {}
        $s = $wb.Sheets.Add([Type]::Missing, $wb.Sheets.Item($wb.Sheets.Count))
        $s.Name = $name
        $s.Cells.Font.Name = "Segoe UI"
        $s.Cells.Font.Size = 10
        return $s
    }

    # -----------------------------------------------------------------
    # SHEET 2: Theo Địa Bàn
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Theo Địa Bàn'..."
    $wsDB = Add-CleanSheet("Theo Địa Bàn")
    $wsDB.Range("A1").Value2 = "PHÂN TÍCH TỔNG HỢP THEO 4 ĐỊA BÀN MỞ RỘNG (PIVOT TABLE)"
    $wsDB.Range("A1").Font.Size = 13
    $wsDB.Range("A1").Font.Bold = $true
    $wsDB.Range("A1").Font.Color = 0x5D361B
    
    $ptDB = $pivotCache.CreatePivotTable($wsDB.Range("B4"), "PT_DiaBan")
    $ptDB.TableStyle2 = "PivotStyleMedium9"
    
    # Row Fields: Mã Địa Bàn (Col 2), Tên Địa Bàn (Col 3)
    $fDB1 = $ptDB.PivotFields(2)
    $fDB1.Orientation = 1
    $fDB1.Position = 1
    
    $fDB2 = $ptDB.PivotFields(3)
    $fDB2.Orientation = 1
    $fDB2.Position = 2
    
    # Data Fields:
    # Count of Leads (Col 1: Mã Hồ Sơ)
    $df1 = $ptDB.AddDataField($ptDB.PivotFields(1), "Số Lượng Leads", -4112) # xlCount = -4112
    $df1.NumberFormat = "#,##0"
    
    # Sum of Ngân Sách (Col 12)
    $df2 = $ptDB.AddDataField($ptDB.PivotFields(12), "Tổng Ngân Sách Dự Kiến (VND)", -4157) # xlSum = -4157
    $df2.NumberFormat = $vndFmt
    
    # Sum of Doanh Thu (Col 9)
    $df3 = $ptDB.AddDataField($ptDB.PivotFields(9), "Tổng Doanh Thu Chuỗi (VND)", -4157)
    $df3.NumberFormat = $vndFmt
    
    # Average of Cửa Hàng (Col 7)
    $df4 = $ptDB.AddDataField($ptDB.PivotFields(7), "TB Cửa Hàng/Chuỗi", -4106) # xlAverage = -4106
    $df4.NumberFormat = "0.0"
    
    # Create PivotChart
    $chartShapeDB = $wsDB.Shapes.AddChart2(201, 51, 550, 40, 480, 260) # 51 = xlColumnClustered
    $chartShapeDB.Chart.SetSourceData($ptDB.TableRange1)
    $chartShapeDB.Chart.HasTitle = $true
    $chartShapeDB.Chart.ChartTitle.Text = "So Sánh Quy Mô Ngân Sách & Số Leads Theo Địa Bàn"
    Write-Host "Sheet 'Theo Địa Bàn' created."

    # -----------------------------------------------------------------
    # SHEET 3: Sàng Lọc Gating
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Sàng Lọc Gating'..."
    $wsGate = Add-CleanSheet("Sàng Lọc Gating")
    $wsGate.Range("A1").Value2 = "KẾT QUẢ SÀNG LỌC NGƯỠNG KHẢ THI VẬN HÀNH (GATING FILTER PIVOT)"
    $wsGate.Range("A1").Font.Size = 13
    $wsGate.Range("A1").Font.Bold = $true
    $wsGate.Range("A1").Font.Color = 0x5D361B
    
    $ptGate = $pivotCache.CreatePivotTable($wsGate.Range("B4"), "PT_Gating")
    $ptGate.TableStyle2 = "PivotStyleMedium2"
    
    # Row Field: Tên Địa Bàn (Col 3)
    $fG1 = $ptGate.PivotFields(3)
    $fG1.Orientation = 1
    $fG1.Position = 1
    
    # Col Field: Kết Luận Đánh Giá (Col 26)
    $fG2 = $ptGate.PivotFields(26)
    $fG2.Orientation = 2 # xlColumnField = 2
    $fG2.Position = 1
    
    # Data Field: Count of Leads (Col 1)
    $dfG = $ptGate.AddDataField($ptGate.PivotFields(1), "Số Hồ Sơ", -4112)
    $dfG.NumberFormat = "#,##0"
    
    # PivotChart: 100% Stacked Bar (xlBarStacked100 = 59)
    $chartShapeGate = $wsGate.Shapes.AddChart2(201, 59, 580, 40, 520, 260)
    $chartShapeGate.Chart.SetSourceData($ptGate.TableRange1)
    $chartShapeGate.Chart.HasTitle = $true
    $chartShapeGate.Chart.ChartTitle.Text = "Tỷ Lệ Đạt Tiêu Chuẩn vs Loại Bỏ Theo Địa Bàn (100% Stacked)"
    Write-Host "Sheet 'Sàng Lọc Gating' created."

    # -----------------------------------------------------------------
    # SHEET 4: Theo Mô Hình Bán Lẻ
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Theo Mô Hình Bán Lẻ'..."
    $wsRet = Add-CleanSheet("Theo Mô Hình Bán Lẻ")
    $wsRet.Range("A1").Value2 = "PHÂN TÍCH NHU CẦU & NGÂN SÁCH THEO 16 MÔ HÌNH BÁN LẺ (PIVOT TABLE)"
    $wsRet.Range("A1").Font.Size = 13
    $wsRet.Range("A1").Font.Bold = $true
    $wsRet.Range("A1").Font.Color = 0x5D361B
    
    $ptRet = $pivotCache.CreatePivotTable($wsRet.Range("B4"), "PT_MoHinh")
    $ptRet.TableStyle2 = "PivotStyleMedium9"
    
    # Row Field: Mô Hình Bán Lẻ (Col 6)
    $fR1 = $ptRet.PivotFields(6)
    $fR1.Orientation = 1
    $fR1.Position = 1
    
    # Data Fields:
    $dfR1 = $ptRet.AddDataField($ptRet.PivotFields(1), "Số Lượng Leads", -4112)
    $dfR1.NumberFormat = "#,##0"
    
    $dfR2 = $ptRet.AddDataField($ptRet.PivotFields(12), "Tổng Ngân Sách (VND)", -4157)
    $dfR2.NumberFormat = $vndFmt
    
    $dfR3 = $ptRet.AddDataField($ptRet.PivotFields(7), "TB Cửa Hàng", -4106)
    $dfR3.NumberFormat = "0.0"
    
    # PivotChart Bar (xlBarClustered = 57)
    $chartShapeRet = $wsRet.Shapes.AddChart2(201, 57, 560, 40, 500, 320)
    $chartShapeRet.Chart.SetSourceData($ptRet.TableRange1)
    $chartShapeRet.Chart.HasTitle = $true
    $chartShapeRet.Chart.ChartTitle.Text = "Xếp Hạng Ngân Sách Dự Kiến Theo Mô Hình Bán Lẻ"
    Write-Host "Sheet 'Theo Mô Hình Bán Lẻ' created."

    # -----------------------------------------------------------------
    # SHEET 5: Theo Giải Pháp WMS
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Theo Giải Pháp WMS'..."
    $wsSol = Add-CleanSheet("Theo Giải Pháp WMS")
    $wsSol.Range("A1").Value2 = "CƠ CẤU NHU CẦU GIẢI PHÁP WMS (PIVOT TABLE)"
    $wsSol.Range("A1").Font.Size = 13
    $wsSol.Range("A1").Font.Bold = $true
    $wsSol.Range("A1").Font.Color = 0x5D361B
    
    $ptSol = $pivotCache.CreatePivotTable($wsSol.Range("B4"), "PT_GiaiPhap")
    $ptSol.TableStyle2 = "PivotStyleMedium9"
    
    # Row Field: Giải Pháp Đang Tìm Hiểu (Col 10)
    $fS1 = $ptSol.PivotFields(10)
    $fS1.Orientation = 1
    $fS1.Position = 1
    
    $dfS1 = $ptSol.AddDataField($ptSol.PivotFields(1), "Số Doanh Nghiệp Quan Tâm", -4112)
    $dfS1.NumberFormat = "#,##0"
    
    $dfS2 = $ptSol.AddDataField($ptSol.PivotFields(12), "Tổng Ngân Sách (VND)", -4157)
    $dfS2.NumberFormat = $vndFmt
    
    # PivotChart Pie (xlPie = 5)
    $chartShapeSol = $wsSol.Shapes.AddChart2(201, 5, 520, 40, 450, 260)
    $chartShapeSol.Chart.SetSourceData($ptSol.TableRange1)
    $chartShapeSol.Chart.HasTitle = $true
    $chartShapeSol.Chart.ChartTitle.Text = "Cơ Cấu Số Lượng Doanh Nghiệp Theo Giải Pháp WMS"
    Write-Host "Sheet 'Theo Giải Pháp WMS' created."

    # -----------------------------------------------------------------
    # SHEET 6: Kiểm Toán Dữ Liệu
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Kiểm Toán Dữ Liệu'..."
    $wsAudit = Add-CleanSheet("Kiểm Toán Dữ Liệu")
    $wsAudit.Range("A1").Value2 = "BẢNG KIỂM TOÁN CHẤT LƯỢNG DỮ LIỆU & NGUỒN (PIVOT AUDIT LOG)"
    $wsAudit.Range("A1").Font.Size = 13
    $wsAudit.Range("A1").Font.Bold = $true
    $wsAudit.Range("A1").Font.Color = 0x5D361B
    
    $ptAudit = $pivotCache.CreatePivotTable($wsAudit.Range("B4"), "PT_Audit")
    $ptAudit.TableStyle2 = "PivotStyleMedium2"
    
    $fA1 = $ptAudit.PivotFields(17) # Kỳ Thống Kê
    $fA1.Orientation = 1
    $fA1.Position = 1
    
    $fA2 = $ptAudit.PivotFields(18) # Trùng Lặp Nguồn
    $fA2.Orientation = 2
    $fA2.Position = 1
    
    $dfA1 = $ptAudit.AddDataField($ptAudit.PivotFields(1), "Số Hồ Sơ Ghi Nhận", -4112)
    $dfA1.NumberFormat = "#,##0"
    Write-Host "Sheet 'Kiểm Toán Dữ Liệu' created."

    # -----------------------------------------------------------------
    # SHEET 7: Tổng hợp Chỉ số (KPI Pivot)
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Tổng hợp Chỉ số'..."
    $wsKPI = Add-CleanSheet("Tổng hợp Chỉ số")
    $wsKPI.Range("A1").Value2 = "BẢNG CHỈ SỐ KPI TỔNG THỂ HỆ THỐNG (PIVOT SUMMARY)"
    $wsKPI.Range("A1").Font.Size = 13
    $wsKPI.Range("A1").Font.Bold = $true
    $wsKPI.Range("A1").Font.Color = 0x5D361B
    
    $ptKPI = $pivotCache.CreatePivotTable($wsKPI.Range("B4"), "PT_KPI")
    $ptKPI.TableStyle2 = "PivotStyleMedium9"
    
    $dfK1 = $ptKPI.AddDataField($ptKPI.PivotFields(1), "Tổng Số Hồ Sơ Khảo Sát", -4112)
    $dfK1.NumberFormat = "#,##0"
    
    $dfK2 = $ptKPI.AddDataField($ptKPI.PivotFields(12), "Tổng Ngân Sách Dự Kiến (VND)", -4157)
    $dfK2.NumberFormat = $vndFmt
    
    $dfK3 = $ptKPI.AddDataField($ptKPI.PivotFields(9), "Tổng Doanh Thu Chuỗi (VND)", -4157)
    $dfK3.NumberFormat = $vndFmt
    
    $dfK4 = $ptKPI.AddDataField($ptKPI.PivotFields(7), "TB Số Cửa Hàng", -4106)
    $dfK4.NumberFormat = "0.0"
    
    $dfK5 = $ptKPI.AddDataField($ptKPI.PivotFields(8), "TB Số Kho Vận Hành", -4106)
    $dfK5.NumberFormat = "0.0"
    Write-Host "Sheet 'Tổng hợp Chỉ số' created."

    # -----------------------------------------------------------------
    # SHEET 8: Ma Trận MCDA
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Ma Trận MCDA'..."
    $wsMCDA = Add-CleanSheet("Ma Trận MCDA")
    $wsMCDA.Range("A1:H1").Merge()
    $wsMCDA.Range("A1").Value2 = "MA TRẬN CHẤM ĐIỂM ĐÁNH GIÁ ĐA TIÊU CHÍ (MCDA SCORING MATRIX) - BƯỚC 3"
    $wsMCDA.Range("A1").Font.Size = 13
    $wsMCDA.Range("A1").Font.Bold = $true
    $wsMCDA.Range("A1").Font.Color = 0xFFFFFF
    $wsMCDA.Range("A1").Interior.Color = 0x5D361B
    $wsMCDA.Range("A1").HorizontalAlignment = -4108
    $wsMCDA.Range("A1").RowHeight = 30
    
    $mcdaCols = @("Mã Địa Bàn", "Tên Địa Bàn Khảo Sát", "Độ Khớp Nhu Cầu & WMS (35%)", "Khả Năng Triển Khai Thực Tế (30%)", "Áp Lực Cạnh Tranh & Rào Cản (20%)", "Quy Mô Chuỗi & Mở Rộng (15%)", "Tổng Điểm MCDA", "Xếp Hạng & Quyết Định Chiến Lược")
    for ($i = 0; $i -lt $mcdaCols.Count; $i++) {
        $c = $wsMCDA.Cells.Item(3, $i + 1)
        $c.Value2 = $mcdaCols[$i]
        $c.Font.Bold = $true
        $c.Font.Color = 0xFFFFFF
        $c.Interior.Color = 0x885B2E # Medium Slate
        $c.HorizontalAlignment = -4108
        $c.VerticalAlignment = -4108
        $c.WrapText = $true
    }
    $wsMCDA.Range("A3:H3").RowHeight = 28
    
    # Explicit rows for MCDA without nested array flattening
    $wsMCDA.Range("A4").Value2 = "DB-01"
    $wsMCDA.Range("B4").Value2 = "Đông Nam Bộ mở rộng (Bình Dương - Đồng Nai - BRVT)"
    $wsMCDA.Range("C4").Value2 = 5.0
    $wsMCDA.Range("D4").Value2 = 5.0
    $wsMCDA.Range("E4").Value2 = 3.5
    $wsMCDA.Range("F4").Value2 = 5.0
    $wsMCDA.Range("G4").Formula = "=C4*0.35 + D4*0.30 + E4*0.20 + F4*0.15"
    $wsMCDA.Range("H4").Value2 = "HẠNG 1 - ƯU TIÊN SỐ 1 MỞ RỘNG (Top 1)"

    $wsMCDA.Range("A5").Value2 = "DB-02"
    $wsMCDA.Range("B5").Value2 = "Đồng bằng Sông Cửu Long (Cần Thơ - Tiền Giang - An Giang)"
    $wsMCDA.Range("C5").Value2 = 4.5
    $wsMCDA.Range("D5").Value2 = 4.0
    $wsMCDA.Range("E5").Value2 = 4.5
    $wsMCDA.Range("F5").Value2 = 4.0
    $wsMCDA.Range("G5").Formula = "=C5*0.35 + D5*0.30 + E5*0.20 + F5*0.15"
    $wsMCDA.Range("H5").Value2 = "HẠNG 2 - ƯU TIÊN SỐ 2 MỞ RỘNG (Top 2)"

    $wsMCDA.Range("A6").Value2 = "DB-03"
    $wsMCDA.Range("B6").Value2 = "Duyên hải Nam Trung Bộ (Đà Nẵng - Quảng Nam - Khánh Hòa)"
    $wsMCDA.Range("C6").Value2 = 3.0
    $wsMCDA.Range("D6").Value2 = 1.5
    $wsMCDA.Range("E6").Value2 = 3.0
    $wsMCDA.Range("F6").Value2 = 3.5
    $wsMCDA.Range("G6").Formula = "=C6*0.35 + D6*0.30 + E6*0.20 + F6*0.15"
    $wsMCDA.Range("H6").Value2 = "LOẠI BỎ (Không đạt ngưỡng hỗ trợ on-site SLA <= 2h)"

    $wsMCDA.Range("A7").Value2 = "DB-04"
    $wsMCDA.Range("B7").Value2 = "Tây Nguyên (Đắk Lắk - Gia Lai - Lâm Đồng)"
    $wsMCDA.Range("C7").Value2 = 1.0
    $wsMCDA.Range("D7").Value2 = 1.0
    $wsMCDA.Range("E7").Value2 = 4.0
    $wsMCDA.Range("F7").Value2 = 1.0
    $wsMCDA.Range("G7").Formula = "=C7*0.35 + D7*0.30 + E7*0.20 + F7*0.15"
    $wsMCDA.Range("H7").Value2 = "LOẠI BỎ (Không đạt ngưỡng độ khớp giải pháp WMS)"

    $wsMCDA.Range("A4:H7").Borders.LineStyle = 1
    $wsMCDA.Range("C4:F7").NumberFormat = "0.0"
    $wsMCDA.Range("G4:G7").NumberFormat = "0.00"
    $wsMCDA.Range("G4:G7").Font.Bold = $true
    $wsMCDA.Range("A4:A7").RowHeight = 24
    Write-Host "Sheet 'Ma Trận MCDA' created."

    # -----------------------------------------------------------------
    # SHEET 9: Kế Hoạch Khảo Sát
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Kế Hoạch Khảo Sát'..."
    $wsPlan = Add-CleanSheet("Kế Hoạch Khảo Sát")
    $wsPlan.Range("A1:H1").Merge()
    $wsPlan.Range("A1").Value2 = "DANH SÁCH 20 CHUỖI BÁN LẺ HẠT NHÂN THAM GIA KHẢO SÁT THỰC ĐỊA (BƯỚC 4)"
    $wsPlan.Range("A1").Font.Size = 13
    $wsPlan.Range("A1").Font.Bold = $true
    $wsPlan.Range("A1").Font.Color = 0xFFFFFF
    $wsPlan.Range("A1").Interior.Color = 0x5D361B
    $wsPlan.Range("A1").HorizontalAlignment = -4108
    $wsPlan.Range("A1").RowHeight = 30
    
    $planCols = @("Mã Hồ Sơ", "Mã ĐB", "Tên Doanh Nghiệp Khảo Sát", "Mô Hình Bán Lẻ", "Số Cửa Hàng", "Doanh Thu Năm (VNĐ)", "Giải Pháp Lựa Chọn", "Người Đại Diện / Chức Danh")
    for ($i = 0; $i -lt $planCols.Count; $i++) {
        $c = $wsPlan.Cells.Item(3, $i + 1)
        $c.Value2 = $planCols[$i]
        $c.Font.Bold = $true
        $c.Font.Color = 0xFFFFFF
        $c.Interior.Color = 0x885B2E
        $c.HorizontalAlignment = -4108
        $c.VerticalAlignment = -4108
    }
    $wsPlan.Range("A3:H3").RowHeight = 26

    # Copy sample 20 rows directly from Source Sheet
    $srcSheet.Range("A2:H21").Copy($wsPlan.Range("A4"))
    $wsPlan.Range("A4:H21").Borders.LineStyle = 1
    $wsPlan.Range("A4:H21").RowHeight = 20
    Write-Host "Sheet 'Kế Hoạch Khảo Sát' created."

    # -----------------------------------------------------------------
    # SHEET 10: Dash Board
    # -----------------------------------------------------------------
    Write-Host "Creating Sheet 'Dash Board'..."
    $wsDash = Add-CleanSheet("Dash Board")
    # Move Dash Board to First position
    $wsDash.Move($wb.Sheets.Item(1))
    
    $wsDash.Range("A1:P2").Merge()
    $wsDash.Range("A1").Value2 = "EXECUTIVE DASHBOARD - BÁO CÁO THẨM ĐỊNH & LỰA CHỌN ĐỊA BÀN MỞ RỘNG (HƯNG PHÁT WMS)"
    $wsDash.Range("A1").Font.Size = 14
    $wsDash.Range("A1").Font.Bold = $true
    $wsDash.Range("A1").Font.Color = 0xFFFFFF
    $wsDash.Range("A1").Interior.Color = 0x5D361B
    $wsDash.Range("A1").HorizontalAlignment = -4108
    $wsDash.Range("A1").VerticalAlignment = -4108
    $wsDash.Range("A1:A2").RowHeight = 22

    # KPI Cards
    function Make-Card($ws, $topRange, $valRange, $title, $valText) {
        $ws.Range($topRange).Merge()
        $t = $ws.Range($topRange)
        $t.Value2 = $title
        $t.Font.Size = 9
        $t.Font.Bold = $true
        $t.Font.Color = 0xFFFFFF
        $t.Interior.Color = 0x885B2E
        $t.HorizontalAlignment = -4108
        $t.VerticalAlignment = -4108
        
        $ws.Range($valRange).Merge()
        $v = $ws.Range($valRange)
        $v.Value2 = $valText
        $v.Font.Size = 12
        $v.Font.Bold = $true
        $v.Font.Color = 0x5D361B
        $v.Interior.Color = 0xFFF6F0 # Ice Blue
        $v.HorizontalAlignment = -4108
        $v.VerticalAlignment = -4108
        $v.WrapText = $true
        $ws.Range($topRange).Borders.LineStyle = 1
        $ws.Range($valRange).Borders.LineStyle = 1
    }

    Make-Card $wsDash "B4:D4" "B5:D6" "TỔNG SỐ HỒ SƠ KHẢO SÁT" "1,000`n(4 Địa Bàn)"
    Make-Card $wsDash "E4:G4" "E5:G6" "TỶ LỆ ĐẠT TIÊU CHUẨN GATING" "59.80%`n(598 Leads Hợp Lệ)"
    Make-Card $wsDash "H4:J4" "H5:J6" "NGÂN SÁCH KHẢ DỤNG THỰC TẾ" "147.57 Tỷ ₫`n(Sẵn Sàng Chi Trả WMS)"
    Make-Card $wsDash "K4:M4" "K5:M6" "ĐỊA BÀN ƯU TIÊN SỐ 1" "ĐÔNG NAM BỘ (DB-01)`n(Điểm MCDA: 4.70/5.0)"
    Make-Card $wsDash "N4:P4" "N5:P6" "ĐỊA BÀN ƯU TIÊN SỐ 2" "ĐBSCL (DB-02)`n(Điểm MCDA: 4.28/5.0)"
    
    $wsDash.Range("A4").RowHeight = 18
    $wsDash.Range("A5:A6").RowHeight = 22

    # Embed PivotTable on Dashboard: Summary of 4 Regions
    Write-Host "Embedding Summary Pivot Table on Dashboard..."
    $ptDash = $pivotCache.CreatePivotTable($wsDash.Range("B8"), "PT_Dashboard")
    $ptDash.TableStyle2 = "PivotStyleMedium9"
    
    $fD1 = $ptDash.PivotFields(2) # Mã Địa Bàn
    $fD1.Orientation = 1
    $fD1.Position = 1
    
    $fD2 = $ptDash.PivotFields(3) # Tên Địa Bàn
    $fD2.Orientation = 1
    $fD2.Position = 2
    
    $dfDash1 = $ptDash.AddDataField($ptDash.PivotFields(1), "Số Leads", -4112)
    $dfDash1.NumberFormat = "#,##0"
    
    $dfDash2 = $ptDash.AddDataField($ptDash.PivotFields(12), "Tổng Ngân Sách (VND)", -4157)
    $dfDash2.NumberFormat = $vndFmt

    # Create Charts on Dashboard
    Write-Host "Creating Pivot Charts on Dashboard..."
    $chartDash1 = $wsDash.Shapes.AddChart2(201, 51, 30, 310, 420, 260) # Clustered Column
    $chartDash1.Chart.SetSourceData($ptDash.TableRange1)
    $chartDash1.Chart.HasTitle = $true
    $chartDash1.Chart.ChartTitle.Text = "Tổng Ngân Sách Dự Kiến Theo 4 Địa Bàn"
    
    $chartDash2 = $wsDash.Shapes.AddChart2(201, 5, 470, 310, 380, 260) # Pie
    $chartDash2.Chart.SetSourceData($ptSol.TableRange1)
    $chartDash2.Chart.HasTitle = $true
    $chartDash2.Chart.ChartTitle.Text = "Cơ Cấu Nhu Cầu Giải Pháp WMS"

    # -----------------------------------------------------------------
    # Add Interactive Slicers connected across PivotTables!
    # -----------------------------------------------------------------
    Write-Host "Creating Interactive Slicers..."
    try {
        # Slicer 1: Tên Địa Bàn (Col 3)
        $fSlicerDB = $ptDash.PivotFields(3)
        $scDB = $wb.SlicerCaches.Add2($ptDash, $fSlicerDB)
        $slicer1 = $scDB.Slicers.Add($wsDash, [Type]::Missing, "Slicer_DiaBan", "Bộ Lọc Địa Bàn", 580, 150, 180, 140)
        
        # Connect to other Pivot Tables!
        $scDB.PivotTables.AddPivotTable($ptDB)
        $scDB.PivotTables.AddPivotTable($ptGate)
        $scDB.PivotTables.AddPivotTable($ptRet)
        Write-Host "Connected Slicer 1 to PT_DiaBan, PT_Gating, PT_MoHinh!"
        
        # Slicer 2: Kết Luận Đánh Giá (Col 26)
        $fSlicerRes = $ptDash.PivotFields(26)
        $scRes = $wb.SlicerCaches.Add2($ptDash, $fSlicerRes)
        $slicer2 = $scRes.Slicers.Add($wsDash, [Type]::Missing, "Slicer_KetLuan", "Trạng Thái Thẩm Định", 780, 150, 220, 140)
        $scRes.PivotTables.AddPivotTable($ptDB)
        $scRes.PivotTables.AddPivotTable($ptGate)
        Write-Host "Connected Slicer 2 across PivotTables!"
    } catch {
        Write-Host "Slicer creation notice: $($_.Exception.Message)"
    }

    # AutoFit all sheets
    Write-Host "Auto-fitting columns across all sheets..."
    foreach ($sh in $wb.Sheets) {
        $sh.Columns.AutoFit() | Out-Null
    }

    Write-Host "Saving finalized workbook to $finalPath..."
    $wb.SaveAs($finalPath)
    $wb.Close($false)
    $excel.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
    Write-Host "SUCCESS: Generated complete Pivot Table & Dashboard Workbook!"

} catch {
    Write-Host "FATAL ERROR: $($_.Exception.ToString())"
    if ($excel) {
        $excel.Quit()
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
}
