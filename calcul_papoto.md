

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
                    'fd = param * (Cosh((a - x0) / param) - Cosh(x0 / param)) - yd
                    fd = param * ((Exp((a - x0) / param) + Exp(-(a - x0) / param)) / 2 - (Exp(x0 / param) + Exp(-x0 / param)) / 2) - yd
                    'fdev = -Sinh((a - x0) / param) - Sinh(x0 / param)
                    fdev = -(Exp((a - x0) / param) - Exp(-(a - x0) / param)) / 2 - (Exp(x0 / param) - Exp(-x0 / param)) / 2
                    x0 = x0 - fd / fdev
                
                    If k = 15 Then
                        param = 0
                    End If
                    
                    k = k + 1
                Wend
                    
                'f1 = param * (Cosh((x1 - x0) / param) - Cosh(x0 / param)) - y1
                f1 = param * ((Exp((x1 - x0) / param) + Exp(-(x1 - x0) / param)) / 2 - (Exp(x0 / param) + Exp(-x0 / param)) / 2) - y1
                    
                'param = param * (param * (Cosh((x1 - x0) / param) - Cosh(x0 / param)) - yd * x1 / a) / (y1 - yd * x1 / a)
                param = param * (param * ((Exp((x1 - x0) / param) + Exp(-(x1 - x0) / param)) / 2 - (Exp(x0 / param) + Exp(-x0 / param)) / 2) - yd * x1 / a) / (y1 - yd * x1 / a)
                    If j = 15 Then
                        param = 0
                    End If
                    
                j = j + 1
            Wend
            'f2 = param * (Cosh((x2 - x0) / param) - Cosh(x0 / param)) - y2
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


