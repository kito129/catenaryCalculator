    Sub Macro1()
    '
    ' Macro1 Macro
    ' Macro enregistrée le 30/12/2002 par ghislain
    '

    '
        Range("D1").Select
        ActiveCell.FormulaR1C1 = "=COUNTA(C[-1])"
        Range("D2").Select
    End Sub
    Sub Macro2()
    '
    ' Macro2 Macro
    ' Macro enregistrée le 30/12/2002 par ghislain
    '

    '
        Columns("D:D").Select
    End Sub
    Sub Macro3()
    '
    ' Macro3 Macro
    ' Macro enregistrée le 30/12/2002 par ghislain
    '

    '
        Sheets("CARNET papoto").Select
        Sheets("CARNET papoto").Name = "CARNET Terrain"
    End Sub
    Sub Macro4()
    '
    ' Macro4 Macro
    ' Macro enregistrée le 30/12/2002 par ghislain
    '

    '
        Range("A:A,C:C,E:E,G:G").Select
        Range("G1").Activate
        Selection.Delete Shift:=xlToLeft
    End Sub
    Sub Macro5()
    '
    ' Macro5 Macro
    ' Macro enregistrée le 30/12/2002 par ghislain
    '

    '
        Range("E2").Select
        Selection.Font.Bold = True
    End Sub
    Sub Macro6()
    '
    ' Macro6 Macro
    ' Macro enregistrée le 30/12/2002 par ghislain
    '

    '
        Selection.Font.Bold = True
    End Sub
