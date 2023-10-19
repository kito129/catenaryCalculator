    
    Sub calcul()
        ActiveSheet.Unprotect
            
            Range("D41:K48").Select
            Selection.ClearContents
            Range("B21").Select
            
        i = 4
        Call Cable_i(i)
        i = 5
        Call Cable_i(i)
        i = 6
        Call Cable_i(i)
        i = 7
        Call Cable_i(i)
        i = 8
        Call Cable_i(i)
        i = 9
        Call Cable_i(i)

        i = 10
        Call Cable_i(i)
        i = 11
        Call Cable_i(i)

        ActiveSheet.Protect DrawingObjects:=True, Contents:=True, Scenarios:=True

    End Sub

    Sub Cable_i(i)

        // check if the cable is present, not empty
        If Cells(30, i) = "" Or Cells(31, i) = "" Or Cells(32, i) = "" Or Cells(33, i) = "" Or Cells(34, i) = "" Or Cells(35, i) = "" Or Cells(36, i) = "" Or Cells(37, i) = "" Or Cells(38, i) = "" Or Cells(39, i) = "" Or Cells(40, i) = "" Then
            GoTo line1
            End If

        // get parameters   
        a = Cells(30, i)

        hg = Cells(31, i)
        vg = Cells(32, i)

        h1 = Cells(33, i)
        v1 = Cells(34, i)

        h2 = Cells(35, i)
        v2 = Cells(36, i)

        h3 = Cells(37, i)
        v3 = Cells(38, i)

        hd = Cells(39, i)
        vd = Cells(40, i)


        // calculate
        Call general(a, hg, vg, v1, h1, h2, v2, h3, v3, hd, vd, param12, param13, param23)


        // calculate the value 1-2
        Cells(41, i) = param12
        Cells(42, i) = Cells(30, i) * (Cells(30, i) ^ 2 + Cells(29, i) ^ 2) ^ 0.5 / (8 * Cells(41, i))
        // param12 = a * (a ^ 2 + b ^ 2) ^ 0.5 / (8 * param)

        // calculate the value 2-3
        Cells(43, i) = param23
        Cells(44, i) = Cells(30, i) * (Cells(30, i) ^ 2 + Cells(29, i) ^ 2) ^ 0.5 / (8 * Cells(43, i))
        // param23 = a * (a ^ 2 + b ^ 2) ^ 0.5 / (8 * param)

        // calculate the value 1-3
        Cells(45, i) = param13
        Cells(46, i) = Cells(30, i) * (Cells(30, i) ^ 2 + Cells(29, i) ^ 2) ^ 0.5 / (8 * Cells(45, i))
        // param13 = a * (a ^ 2 + b ^ 2) ^ 0.5 / (8 * param)

        
        // calculate the average
        ecart_type = Sqr((3 * (Cells(41, i) ^ 2 + Cells(43, i) ^ 2 + Cells(45, i) ^ 2) - (Cells(41, i) + Cells(43, i) + Cells(45, i)) ^ 2) / (3 * (3 - 1)))
        // ecart_type = Sqr((3 * (param12 ^ 2 + param23 ^ 2 + param13 ^ 2) - (param12 + param23 + param13) ^ 2) / (3 * (3 - 1)))

        // check for error
        If ecart_type > 1000 Then
            Cells(47, i) = "Papoto"
            Cells(48, i) = "Erroné"
            Else // no error, write the average
            
            // MEDIA - PARAMETRO
            Cells(47, i) = (param12 + param13 + param23) / 3
            // mediaParametro = (param12 + param13 + param23) / 3
            
            // MEDIA - FRECCIA
            Cells(48, i) = Cells(30, i) * (Cells(30, i) ^ 2 + Cells(29, i) ^ 2) ^ 0.5 / (8 * Cells(47, i))
            // mediaFreccia = a * (a ^ 2 + b ^ 2) ^ 0.5 / (8 * mediaParametro)
        End If


        line1:
    End Sub


// calculator functions


    Sub general(a, hg, vg, v1, h1, h2, v2, h3, v3, hd, vd, param12, param13, param23)
        pi = 3.14159265358979
        'a = Cells(1, 2)

        'hg = Cells(3, 2)
        'vg = Cells(4, 2)
        '
        'h1 = Cells(5, 2)
        'v1 = Cells(6, 2)
        '
        'h2 = Cells(7, 2)
        'v2 = Cells(8, 2)
        '
        'h3 = Cells(9, 2)
        'v3 = Cells(10, 2)
        '
        'hd = Cells(11, 2)
        'vd = Cells(12, 2)


        hgr = 0
        vgr = pi / 2 - pi / 200 * vg

        If hd < hg Then
            hdr = pi / 200 * (400 + hd - hg)
            Else
            hdr = pi / 200 * (hd - hg)
        End If

        vdr = pi / 2 - pi / 200 * vd

        If h1 < hg Then
            h1r = pi / 200 * (400 + h1 - hg)
            Else
            h1r = pi / 200 * (h1 - hg)
        End If

        v1r = pi / 2 - pi / 200 * v1

        If h2 < hg Then
            h2r = pi / 200 * (400 + h2 - hg)
            Else
            h2r = pi / 200 * (h2 - hg)
        End If

        v2r = pi / 2 - pi / 200 * v2

        Call papoto(hgr, vgr, h1r, v1r, h2r, v2r, hdr, vdr, param, fd, a, pi)
        param12 = param



        If h3 < hg Then
            h2r = pi / 200 * (400 + h3 - hg)
            Else
            h2r = pi / 200 * (h3 - hg)
        End If

        v2r = pi / 2 - pi / 200 * v3

        Call papoto(hgr, vgr, h1r, v1r, h2r, v2r, hdr, vdr, param, fd, a, pi)
        param13 = param


        If h2 < hg Then
            h1r = pi / 200 * (400 + h2 - hg)
            Else
            h1r = pi / 200 * (h2 - hg)
        End If

        v1r = pi / 2 - pi / 200 * v2

        Call papoto(hgr, vgr, h1r, v1r, h2r, v2r, hdr, vdr, param, fd, a, pi)
        param23 = param

        'Cells(14, 2) = param12
        'Cells(15, 2) = param13
        'Cells(16, 2) = param23
        'Cells(18, 2) = (param12 + param13 + param23) / 3
    End Sub


    Sub papoto(hgr, vgr, h1r, v1r, h2r, v2r, hdr, vdr, param, fd, a, pi)
        alpha = (pi - hdr + hgr) / 2
        iteralpha = (pi - hdr + hgr) / 4
        param = 1000
        f2 = 1
        i = 1

        While Abs(iteralpha) > 0.00000157       'iteration à 0.001 gr
            ag = a * Sin(pi - hdr - alpha) / Sin(hdr)
            ad = a * Sin(alpha) / Sin(hdr)
            yd = ad * Tan(vdr) - ag * Tan(vgr)
            x1 = ag * Sin(h1r) / Sin(pi - h1r - alpha)
            a1 = x1 * Sin(alpha) / Sin(h1r)
            y1 = a1 * Tan(v1r) - ag * Tan(vgr)
            x2 = ag * Sin(h2r) / Sin(pi - h2r - alpha)
            a2 = x2 * Sin(alpha) / Sin(h2r)
            y2 = a2 * Tan(v2r) - ag * Tan(vgr)
            f1 = 1
            j = 1
        
            While Abs(f1) > 0.005
                x0 = a / 2
                fd = 1
                k = 1
                
                While Abs(fd) > 0.05
                    
                    fd = param * ((Exp((a - x0) / param) + Exp(-(a - x0) / param)) / 2 - (Exp(x0 / param) + Exp(-x0 / param)) / 2) - yd
                    
                    
                    fdev = -(Exp((a - x0) / param) - Exp(-(a - x0) / param)) / 2 - (Exp(x0 / param) - Exp(-x0 / param)) / 2
                    x0 = x0 - fd / fdev
                
                    If k = 15 Then
                        param = 0
                    End If
                    
                    k = k + 1
                Wend
                    
                f1 = param * ((Exp((x1 - x0) / param) + Exp(-(x1 - x0) / param)) / 2 - (Exp(x0 / param) + Exp(-x0 / param)) / 2) - y1
                    
                param = param * (param * ((Exp((x1 - x0) / param) + Exp(-(x1 - x0) / param)) / 2 - (Exp(x0 / param) + Exp(-x0 / param)) / 2) - yd * x1 / a) / (y1 - yd * x1 / a)
                    If j = 15 Then
                        param = 0
                    End If
                    
                j = j + 1
            Wend
            
            f2 = param * ((Exp((x2 - x0) / param) + Exp(-(x2 - x0) / param)) / 2 - (Exp(x0 / param) + Exp(-x0 / param)) / 2) - y2
            
            If f2 > 0 Then
                alpha = alpha + iteralpha
                Else
                alpha = alpha - iteralpha
            End If
            If i = 20 Then
            param = 0
            End If
            iteralpha = iteralpha / 2
        Wend

    End Sub