    Sub ouvert_carnet_papoto()


    fichier = Application.GetOpenFilename("Text Files (*.txt), *.txt")
    Repertoire = CurDir(fichier)

        Workbooks.OpenText Filename:= _
            fichier _
            , Origin:=xlWindows, StartRow:=1, DataType:=xlDelimited, TextQualifier _
            :=xlDoubleQuote, ConsecutiveDelimiter:=True, Tab:=True, Semicolon:=False _
            , Comma:=False, Space:=True, Other:=True, OtherChar:="+", FieldInfo:= _
            Array(Array(1, 1), Array(2, 1), Array(3, 1), Array(4, 1), Array(5, 1), Array(6, 1), Array(7 _
            , 1), Array(8, 1), Array(9, 1), Array(10, 1), Array(11, 1), Array(12, 1), Array(13, 1), Array _
            (14, 1), Array(15, 1))
    

        Rows("1:1").Select
        Selection.Insert Shift:=xlDown
        
        Range("A:A,C:C,E:E,G:O").Select
        'Range("G1").Activate
        Selection.Delete Shift:=xlToLeft
        
        Range("A1") = fichier
        Range("A2") = "Matricule"
        Range("B2") = "H"
        Range("C2") = "V"
        
        Range("A1").Select
        
        
        Sheets.Move after:=Workbooks("Papoto.xls").Sheets("Papoto")
        'ActiveSheet.Name = "CARNET Terrain"
        '
        Call extraction_des_donnees
        ActiveSheet.Previous.Select
    End Sub

    Sub extraction_des_donnees()
    nb_cables = Sheets("papoto").Cells(4, 16)
    Cells(3, 16) = nb_cables
    i = 3
    j = 3
    k = 0
    'Cells(1, 4) = "=COUNTA(C[-1])"
    'aeraCount = Cells(1, 4) - 1
    'nb_papoto = aeraCount / nb_cables / 5

    While Cells(i, 2) <> ""
        
        For l = 0 To 4
            
            For k = 0 To nb_cables - 1
                
                If Cells(i, 2) = "" Then
                GoTo line1
                End If
                
                If l = 0 Then
                    Cells(j - 1, 5 + k) = Cells(i + k, 1)
                    Cells(j - 1, 5 + k).Select
                    Selection.Font.Bold = True
                End If
                    
                Cells(j, 5 + k) = Cells(i + k, 2) / 100000
                Cells(j + 1, 5 + k) = Cells(i + k, 3) / 100000
            Next k
            
            i = i + nb_cables
            j = j + 2
        
        Next l
        
        j = j + 2

    Wend

    line1:

    End Sub
